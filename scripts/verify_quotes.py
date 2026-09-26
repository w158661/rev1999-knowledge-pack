#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_quotes.py —— 把技能包里的引文逐条回语料库核对（服务 N29「考据不落地病」）

做什么
------
扫描包内 Markdown，抽出带引号的引文，去剧情语料库里找原文：
    --claimed  只查"声称是原文"的那些（所在行含「原文」「出处：」等标记）——这些**必须命中**
    默认       全量引文（含档案、衣着、语音、公告等非剧情文本的引用）——未命中只作提示

为什么要区分
------------
语料库只收**剧情台词**。而本包里的引文还来自衣着说明、造像、语音库、公告、签到等非剧情文本，
它们本来就不在语料库里。所以"未命中"不等于错，只说明**需要换一个来源核对**。
真正要卡死的是标了「原文」的那些。

用法
----
    python verify_quotes.py --root <语料库> --pack . --claimed
    python verify_quotes.py --root <语料库> --pack . --report out.md --max-miss 200
    python verify_quotes.py --root <语料库> --pack . --only data/扩充/15_反AI写作病清单.md
"""

import argparse
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from extract_story_dialogue import iter_files, parse_file  # noqa: E402

# 引号：本包混用「」『』“”""
RE_QUOTE = re.compile(r'[「『“"]([^「」『』“”"\n]{6,300})[」』”"]')
# "声称是原文"的两种真实写法（不能用"行内出现『原文』二字"当判据，那会命中大量普通引号）
RE_CLAIM_A = re.compile(r'原文\s*[：:]\s*[「『“"]([^「」『』“”"\n]{6,300})[」』”"]')
RE_CLAIM_B = re.compile(r'[「『“"]([^「」『』“”"\n]{6,300})[」』”"]\s*（出处\s*[：:]')
# 引文后跟一个**剧情节号**的引用（最强判据：既然标了 3RD-06，就必须能在 3RD-06 里逐字找到）
RE_CITED = re.compile(r'[「『“"]([^「」『』“”"\n]{6,300})[」』”"][^\n]{0,40}?'
                      r'(?:\d{1,2}(?:ST|ND|RD|TH|SP)-\d{1,3}|CH\d{4,})', re.I)
# 省略式引用的切分符：引文里出现这些，说明原文并不相邻，必须逐段核对
RE_GAP = re.compile(r'(?:…{2,}|\.{3,}|—{2,}|-{2,})')
KEEP = re.compile(r'[\u4e00-\u9fffA-Za-z0-9]')


def norm(s: str) -> str:
    """归一化：只留中英文数字，去标点/空白/引号内换行。"""
    return "".join(KEEP.findall(s))


def segments(q: str):
    """把省略式引用切成若干段，返回非空且长度达标的段。"""
    return [p for p in (norm(x) for x in RE_GAP.split(q)) if len(p) >= 6]


def locate(seg: str, where: dict):
    """给一个（已归一化的）段找它在语料里的位置：先精确命中整行，再退化为包含它的行。"""
    if seg in where:
        return where[seg]
    for n, loc in where.items():
        if seg and seg in n:
            return loc + "（行内片段）"
    return None


def explain(q: str, big: str, where: dict):
    """逐段说明：每段命中与否、命中的落在哪一节。"""
    segs = segments(q) or [norm(q)]
    rows = []
    for s in segs:
        if s in big:
            rows.append((s, True, locate(s, where)))
        else:
            rows.append((s, False, None))
    return rows


def judge(q: str, big: str):
    """返回 ('hit'|'partial'|'miss', 段数, 命中段数)"""
    segs = segments(q) or [norm(q)]
    ok = [s for s in segs if s in big]
    if len(ok) == len(segs):
        return "hit", len(segs), len(ok)
    if ok:
        return "partial", len(segs), len(ok)
    return "miss", len(segs), 0


def build_corpus(root: Path, langs):
    """返回 (归一化大串, 逐行集合, 行数, 段→位置索引)"""
    lines = []
    where = {}
    for lang, kind_en, kind_cn, f in iter_files(root, langs):
        for chapter, section, who, text in parse_file(f):
            n = norm(text)
            lines.append((n, lang, kind_cn, chapter, section, who, text))
            if n and n not in where:
                where[n] = f"{kind_cn}·{chapter}·{section}·{who}"
    big = "".join(x[0] for x in lines)
    return big, lines, where


def iter_pack_files(pack: Path, only=None):
    if only:
        p = Path(only)
        yield p if p.is_absolute() else pack / p
        return
    for pat in ("data/*.md", "data/*/*.md", "skills/*/SKILL.md", "README.md", "CHANGELOG.md"):
        for p in sorted(pack.glob(pat)):
            if p.is_file():
                yield p


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=os.environ.get("STORY_TEXT_ROOT"))
    ap.add_argument("--pack", default=os.environ.get("REV1999_PACK", "."))
    ap.add_argument("--lang", default="zh-CN")
    ap.add_argument("--claimed", action="store_true", help="只核对声称是原文的引文")
    ap.add_argument("--cited", action="store_true",
                    help="只核对『引文 + 剧情节号』的引用（最强判据，必须命中）")
    ap.add_argument("--only", help="只扫某一个文件（相对 --pack）")
    ap.add_argument("--report", help="输出 Markdown 报告")
    ap.add_argument("--max-miss", type=int, default=80, help="报告里最多列多少条未命中")
    ap.add_argument("--detail", action="store_true",
                    help="对非「全部段命中」的引文逐段定位（复核拼接引用用）")
    ap.add_argument("--only-partial", action="store_true", help="只输出「部分命中」的引文")
    args = ap.parse_args(argv)

    if not args.root:
        print("错误：需要 --root（语料库路径）", file=sys.stderr)
        return 2
    root = Path(args.root).expanduser().resolve()
    pack = Path(args.pack).expanduser().resolve()
    langs = [s.strip() for s in args.lang.split(",") if s.strip()]

    big, corpus, where = build_corpus(root, langs)
    print(f"语料库：{len(corpus):,} 行台词，归一化后 {len(big):,} 字符（{root.name}，{','.join(langs)}）")

    total = hit = partial = 0
    miss = []
    per_file = {}
    for fp in iter_pack_files(pack, args.only):
        try:
            txt = fp.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        f_total = f_hit = 0
        for i, line in enumerate(txt.splitlines(), 1):
            if args.cited:
                cands = [m.group(1) for m in RE_CITED.finditer(line)]
            elif args.claimed:
                cands = [m.group(1) for m in RE_CLAIM_A.finditer(line)] + \
                        [m.group(1) for m in RE_CLAIM_B.finditer(line)]
            else:
                cands = [m.group(1) for m in RE_QUOTE.finditer(line)]
            for q in cands:
                if len(norm(q)) < 8:
                    continue
                # 排除明显不是引文的"引号内内容"：文件名、Markdown 标记、书名号/方括号结构
                if ".md" in q or "**" in q or "__" in q or "【" in q or "http" in q:
                    continue
                f_total += 1
                verdict, nseg, nok = judge(q, big)
                if verdict == "hit":
                    f_hit += 1
                else:
                    if verdict == "partial":
                        partial += 1
                    miss.append((fp.relative_to(pack).as_posix(), i, verdict,
                                 f"{nok}/{nseg}", q[:90], line.strip()[:70]))
        if f_total:
            per_file[fp.relative_to(pack).as_posix()] = (f_hit, f_total)
            total += f_total
            hit += f_hit

    print(f"引文：{total:,} 条，全部段命中 {hit:,}（{hit/total*100 if total else 0:.1f}%），"
          f"部分命中 {partial:,}，完全未命中 {total-hit-partial:,}")
    print("\n-- 按文件 --")
    for k, (h, t) in sorted(per_file.items(), key=lambda kv: kv[1][1] - kv[1][0], reverse=True)[:25]:
        flag = "" if h == t else ("  ← 全部命中" if h == t else "")
        print(f"  {h:>4}/{t:<4}  {k}{flag}")

    if miss:
        shown = [m for m in miss if (m[2] == "partial" or not args.only_partial)]
        print(f"\n-- 未命中示例（最多 {args.max_miss} 条）--")
        for f, ln, verdict, segs, q, ctx in shown[:args.max_miss]:
            tag = "部分命中" if verdict == "partial" else "未命中"
            print(f"  [{tag} {segs}] {f}:{ln}\n    引文：{q}\n    上下文：{ctx}")
            if args.detail:
                for s, ok, loc in explain(q, big, where):
                    mark = "✓" if ok else "✗"
                    print(f"      {mark} {s[:60]}" + (f"   ← {loc}" if loc else ""))

    if args.report:
        rp = Path(args.report)
        rp.parent.mkdir(parents=True, exist_ok=True)
        L = [f"# 引文校验报告（{'仅声称原文' if args.claimed else '全量'}）", "",
             f"- 语料库：`{root.name}`（{len(corpus):,} 行台词）",
             f"- 扫描包：`{pack}`",
             f"- 引文 {total:,} 条；**全部段命中 {hit:,}**（{hit/total*100 if total else 0:.1f}%）；"
             f"部分命中 {partial:,}；完全未命中 {total-hit-partial:,}", "",
             "> 判据：引文按省略号/破折号切段后**逐段**回语料核对；「部分命中」= 拼接了不相邻的原文，需人工确认。",
             "> 未命中**不等于错误**：语料库只收剧情台词，而包里的引文还来自衣着、造像、语音库、公告、签到等非剧情文本。", "",
             "## 按文件（按命中率升序）", "", "| 命中/总数 | 文件 |", "|---|---|"]
        for k, (h, t) in sorted(per_file.items(), key=lambda kv: (kv[1][0] / kv[1][1])):
            L.append(f"| {h}/{t} | `{k}` |")
        L += ["", "## 未命中明细", "", "| 判定 | 文件:行 | 引文 | 上下文 |", "|---|---|---|---|"]
        for f, ln, verdict, segs, q, ctx in miss[:args.max_miss]:
            tag = f"部分命中 {segs}" if verdict == "partial" else "未命中"
            L.append(f"| {tag} | `{f}:{ln}` | {q} | {ctx} |")
        rp.write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
        print(f"\n报告已写出：{rp}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
