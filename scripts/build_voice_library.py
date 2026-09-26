#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_voice_library.py —— 由剧情文本库重建「角色语音风格库」（skill_11）。

产出结构（每个角色一节）
------------------------
    ### 【角色名】  台词 745 句
    - 句式：平均 18.9 字/句；短句为主（≤15 字占 62%）；极少反问
    - 标点：省略号 12%、破折号 4%、问号 9%、感叹号 3%
    - 高频词：乳牙、孩子、牙齿……
    - 称谓：称维尔汀为「维尔汀小姐」
    - 样本（按章节均匀抽样 N 句，逐字）
      - [活动·绿湖噩梦·GLN-01] 我的旅行计划有些变动。……

分层
----
    T1 ≥ 300 句   抽 60 句
    T2 100~299    抽 28 句
    T3 30~99      抽 14 句
    T4 10~29      抽 6 句
    T5 < 10       只进末尾附录表（名字 + 句数）

用法
----
    python build_voice_library.py --root <语料库> --out <输出.md> [--dry-run]
    python build_voice_library.py --root <语料库> --index <输出.json>
"""

import argparse
import json
import os
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from extract_story_dialogue import collect, DIR_KINDS  # noqa: E402

# 中文常用停用字/词（只用于高频词统计，避免把"我/你/的"排到前面）
STOP = set("""
我 你 他 她 它 我们 你们 他们 她们 这 那 这个 那个 这里 那里 是 的 了 在 有 和 与 就 都 也 还 又
不 没 没有 会 要 能 可以 什么 怎么 为什么 一个 一样 一样 已经 因为 所以 但是 如果 然后 现在 时候
自己 他们 大家 人们 一点 一些 这样 那样 不是 就是 只是 还是 或者 而且 不过 其实 真的 好像 觉得
知道 应该 可能 需要 想要 必须 一定 非常 特别 十分 有点 一点 出来 起来 过来 下去 上来 一下
""".split())

RE_CALL_SUFFIX = "小姐|先生|女士|大人|教员|队长|司辰|同志|老师"
# 占位标签：这些不是"角色"，而是尚未揭示身份的说话人（或群像），不能当一个人统计
PLACEHOLDER = re.compile(r"^[？?]+$|^[×]+$|^(未知|不明|旁白|众人|众|群众|路人)$")


def make_call_re(known_names):
    """只用语料里真实出现过的说话人标签来识别称谓，避免「一位肃穆的女士」这类误报。"""
    names = sorted((n for n in known_names if n and not PLACEHOLDER.match(n)),
                   key=len, reverse=True)
    if not names:
        return None
    pat = "(" + "|".join(re.escape(n) for n in names) + ")(" + RE_CALL_SUFFIX + ")"
    return re.compile(pat)


def fenced(t: str) -> str:
    return t.replace("\n", " ").strip()


def stats_for(lines, call_re=None):
    n = len(lines)
    lens = [len(re.findall(r"[\u4e00-\u9fff]", t)) for t in lines]
    short = sum(1 for x in lens if x <= 15)
    ell = sum(1 for t in lines if "……" in t or "..." in t)
    dash = sum(1 for t in lines if "——" in t or "—" in t)
    q = sum(1 for t in lines if "？" in t or "?" in t)
    ex = sum(1 for t in lines if "！" in t or "!" in t)
    # 高频实词：切 2 字滑窗太糙，这里用 2~4 字词粗筛 + 停用词过滤
    words = Counter()
    for t in lines:
        for w in re.findall(r"[\u4e00-\u9fff]{2,4}", t):
            if w in STOP:
                continue
            words[w] += 1
    calls = Counter()
    if call_re is not None:
        for t in lines:
            for m in call_re.finditer(t):
                calls[m.group(1) + m.group(2)] += 1
    return {
        "n": n,
        "avg": (sum(lens) / n) if n else 0,
        "short_pct": (short / n * 100) if n else 0,
        "ell_pct": (ell / n * 100) if n else 0,
        "dash_pct": (dash / n * 100) if n else 0,
        "q_pct": (q / n * 100) if n else 0,
        "ex_pct": (ex / n * 100) if n else 0,
        "top_words": words.most_common(8),
        "calls": calls.most_common(4),
    }


def even_sample(rows, k):
    """按章节顺序均匀抽样，保证跨版本分布，不集中在开头。"""
    if len(rows) <= k:
        return rows
    step = len(rows) / k
    return [rows[min(int(i * step), len(rows) - 1)] for i in range(k)]


def tier_of(n):
    """分层与抽样条数。目标是：主要角色保足样本，次要角色保统计，长尾只列名。"""
    if n >= 300:
        return 1, 24
    if n >= 100:
        return 2, 12
    if n >= 30:
        return 3, 4
    if n >= 10:
        return 4, 2
    return 5, 0


def build(root: Path, langs, min_main=10, max_main=None):
    rows = collect(root, langs)
    by = {}
    for r in rows:
        by.setdefault(r["who"], []).append(r)
    # 占位标签（？？？ 等）单独归档：它是"尚未揭示身份的说话人"的合集，不是一个人
    placeholder = {k: v for k, v in by.items() if PLACEHOLDER.match(k)}
    real = {k: v for k, v in by.items() if not PLACEHOLDER.match(k)}
    ranked = sorted(real.items(), key=lambda kv: -len(kv[1]))
    main = [(k, v) for k, v in ranked
            if len(v) >= min_main and (max_main is None or len(v) <= max_main)]
    tail = [(k, v) for k, v in ranked if len(v) < min_main]
    return rows, ranked, main, tail, placeholder


def render(ranked, main, tail, total, langs, src_note, min_main=10, placeholder=None, call_re=None,
           title="角色语音风格库（语料重建版）"):
    placeholder = placeholder or {}
    out = []
    w = out.append
    ph_n = sum(len(v) for v in placeholder.values())
    w(f"# {title}")
    w("")
    w("> 本文件由剧情文本库自动重建：**统计（句式／标点／高频词／称谓）＋ 逐字台词抽样**。")
    w(f"> 语料：{src_note}｜语言：{', '.join(langs)}｜台词总行数：{total:,}｜"
      f"说话人标签：{len(ranked) + len(placeholder):,}（其中角色 {len(ranked):,}＋占位 {len(placeholder):,}）")
    w("> 样本按章节顺序**均匀抽样**（不是取开头），每条标注 类别·章节·节号，可回原文逐字核对。")
    w("> 分层：T1 ≥300 句抽 24；T2 ≥100 抽 12；T3 ≥30 抽 4；T4 ≥10 抽 2；T5 <10 只列名。")
    if placeholder:
        names = "、".join(f"{k}({len(v)})" for k, v in sorted(placeholder.items(), key=lambda kv: -len(kv[1])))
        w(f"> **占位标签已排除**（{ph_n:,} 行，{names}）：这些是「尚未揭示身份的说话人」的合集，")
        w("> 把它们当成一个角色统计会得出错误结论（例如把某封信里重复 70 次的句子当成某个人的口头禅）。")
    w("")
    w("---")
    w("")

    for name, rows in main:
        st = stats_for([r["text"] for r in rows], call_re)
        tier, k = tier_of(len(rows))
        kinds = Counter(r["kind"] for r in rows)
        kind_str = "／".join(f"{k_}{v}" for k_, v in kinds.most_common(3))
        w(f"## 【{name}】　{st['n']} 句　<span>T{tier}</span>")
        w("")
        w(f"- **分布**：{kind_str}")
        shape = "短句为主" if st["short_pct"] >= 55 else ("长短句混合" if st["short_pct"] >= 35 else "长句为主")
        tone = []
        if st["ell_pct"] >= 15: tone.append("爱用省略号")
        if st["dash_pct"] >= 8: tone.append("常用破折号打断")
        if st["q_pct"] >= 20: tone.append("多反问")
        if st["ex_pct"] >= 15: tone.append("多感叹")
        w(f"- **句式**：平均 {st['avg']:.1f} 字/句；{shape}（≤15 字占 {st['short_pct']:.0f}%）"
          + ("；" + "、".join(tone) if tone else ""))
        w(f"- **标点**：省略号 {st['ell_pct']:.0f}%｜破折号 {st['dash_pct']:.0f}%｜"
          f"问号 {st['q_pct']:.0f}%｜感叹号 {st['ex_pct']:.0f}%")
        if st["top_words"]:
            w("- **高频词**：" + "、".join(f"{x}({c})" for x, c in st["top_words"]))
        if st["calls"]:
            w("- **称谓**：" + "、".join(f"「{x}」×{c}" for x, c in st["calls"]))
        w("")
        w("**样本台词**")
        w("")
        for r in even_sample(rows, k):
            w(f"- `[{r['kind']}·{r['chapter']}·{r['section']}]`　{fenced(r['text'])}")
        w("")

    w("---")
    w("")
    w(f"## 附录：低频说话人（1~{min_main - 1} 句，共 {len(tail)} 个标签）")
    w("")
    w("> 这类标签多为群像／路人（学生Ⅰ、教员、报童、船员……），台词不足以立起「声音」，")
    w("> 但可用于判断某个场景里都有谁在场。完整清单见同目录 `角色索引.json`。")
    w("")
    chunks = [f"{n}({len(rows)})" for n, rows in tail]
    for i in range(0, len(chunks), 12):
        w("- " + "　".join(chunks[i:i + 12]))
    w("")
    return "\n".join(out)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=os.environ.get("STORY_TEXT_ROOT"))
    ap.add_argument("--lang", default="zh-CN")
    ap.add_argument("--out")
    ap.add_argument("--index", help="同时导出 JSON 索引（角色→句数→章节分布）")
    ap.add_argument("--min", type=int, default=10, help="进入正文的最小句数（默认 10）")
    ap.add_argument("--max", type=int, default=None, help="进入正文的最大句数（用于拆出配角分册）")
    ap.add_argument("--title", default="角色语音风格库（语料重建版）", help="产物标题")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    if not args.root:
        print("错误：需要 --root", file=sys.stderr)
        return 2
    root = Path(args.root).expanduser().resolve()
    langs = [s.strip() for s in args.lang.split(",") if s.strip()]
    rows, ranked, main, tail, placeholder = build(root, langs, args.min, args.max)
    call_re = make_call_re({k for k, _ in ranked})

    print(f"台词行数      : {len(rows):,}")
    print(f"角色标签      : {len(ranked):,}（另有占位标签 {len(placeholder):,}，共 {sum(len(v) for v in placeholder.values()):,} 行已排除）")
    print(f"进入正文(T1~T4): {len(main):,}")
    print(f"进入附录(T5)  : {len(tail):,}")
    dist = Counter()
    for _, v in ranked:
        dist[tier_of(len(v))[0]] += 1
    print("分层分布      : " + "  ".join(f"T{k}={v}" for k, v in sorted(dist.items())))

    if args.index:
        idx = {n: {"n": len(v),
                   "kinds": dict(Counter(r["kind"] for r in v)),
                   "chapters": sorted({r["chapter"] for r in v}),
                   "tier": tier_of(len(v))[0]} for n, v in ranked}
        p = Path(args.index)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(idx, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"索引已写出    : {p}  ({p.stat().st_size/1024:.0f} KB)")

    if args.out:
        src = f"{root.name}"
        md = render(ranked, main, tail, len(rows), langs, src, args.min, placeholder, call_re, args.title)
        p = Path(args.out)
        p.parent.mkdir(parents=True, exist_ok=True)
        if args.dry_run:
            print(f"[dry-run] 将写出 {p}  {len(md)/1024:.0f} KB（未写盘）")
        else:
            p.write_text(md, encoding="utf-8", newline="\n")
            print(f"已写出        : {p}  ({len(md)/1024:.0f} KB, {md.count(chr(10)):,} 行)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
