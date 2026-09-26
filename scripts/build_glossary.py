#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_glossary.py —— 生成「五语对照表」（角色名 · 专有名词）

原理
----
五种语言的**剧情节号一致**（`## 01 · 3RD-06 · 黑羊之墙` / `## 01 · 3RD-06 · Black Sheep Wall`），
而同一节内**台词的顺序一致**。于是把两种语言的同一节按行号对齐，
第 N 行的说话人标签就构成一个 (中文名, 译名) 对——出现次数最多的译名即该角色的官方译名。

同时抽出**节标题**对照（含版本名、活动名、章节名），并统计每语言覆盖率。

产出
----
    --out <md>      人读对照表（角色名表 + 章节标题抽样 + 覆盖率）
    --json <json>   机器可读映射（{"中→英": {...}, "中→日": {...}}）

用法
----
    python build_glossary.py --root <语料库> --base zh-CN --out data/术语与角色名五语对照表.md
    python build_glossary.py --root <语料库> --json glossary.json
"""

import argparse
import json
import os
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from extract_story_dialogue import iter_files, parse_file  # noqa: E402

RE_SID = re.compile(r"\b(\d{1,2}(?:ST|ND|RD|TH|SP)-\d{1,3})\b", re.I)
RE_CH = re.compile(r"\b(CH\d{4,})\b", re.I)


def section_key(section: str):
    m = RE_SID.search(section) or RE_CH.search(section)
    if m:
        return m.group(1).upper()
    # 小径之类没有节号：用「序号 + 小节名」的序号当键（跨语言一致）
    m2 = re.match(r"^\s*(\d{1,3})\s*[·.]", section)
    return f"#{m2.group(1)}" if m2 else None


def load(root: Path, langs):
    """{lang: {key: [(who, text), ...]}}  以及 {lang: {key: 节标题}}"""
    seq = {l: defaultdict(list) for l in langs}
    titles = {l: {} for l in langs}
    for lang, kind_en, kind_cn, f in iter_files(root, langs):
        for chapter, section, who, text in parse_file(f):
            k = section_key(section)
            if not k:
                continue
            seq[lang][k].append((who, text))
            titles[lang].setdefault(k, section)
    return seq, titles


def align_names(seq, base, other):
    """按节内行序对齐，投票得出 中文名 → 译名"""
    votes = defaultdict(Counter)
    common = set(seq[base]) & set(seq[other])
    for k in common:
        a, b = seq[base][k], seq[other][k]
        for (wa, _), (wb, _) in zip(a, b):
            if wa and wb:
                votes[wa][wb] += 1
    out = {}
    for zh, c in votes.items():
        name, n = c.most_common(1)[0]
        total = sum(c.values())
        out[zh] = {"name": name, "hit": n, "total": total,
                   "conf": round(n / total, 2) if total else 0}
    return out, len(common)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=os.environ.get("STORY_TEXT_ROOT"))
    ap.add_argument("--base", default="zh-CN")
    ap.add_argument("--others", default="en,ja,ko,zh-TW")
    ap.add_argument("--min-lines", type=int, default=20, help="只收该语言下台词数≥此值的角色")
    ap.add_argument("--out")
    ap.add_argument("--json", dest="json_out")
    args = ap.parse_args(argv)

    if not args.root:
        print("错误：需要 --root", file=sys.stderr)
        return 2
    root = Path(args.root).expanduser().resolve()
    others = [s.strip() for s in args.others.split(",") if s.strip()]
    langs = [args.base] + others
    seq, titles = load(root, langs)

    base_counts = Counter(w for v in seq[args.base].values() for w, _ in v)
    keep = {w for w, n in base_counts.items() if n >= args.min_lines}
    print(f"基准语言 {args.base}：{len(base_counts):,} 个说话人，其中 ≥{args.min_lines} 句的 {len(keep):,} 个")
    for l in langs:
        n = sum(len(v) for v in seq[l].values()) if l in seq else 0
        print(f"  {l:<7} 节 {len(seq.get(l, {})):>5}  台词 {n:>7,}")

    results = {}
    for other in others:
        if other not in seq:
            continue
        table, common = align_names(seq, args.base, other)
        results[other] = {"table": table, "common_sections": common}
        print(f"  对齐 {args.base} ↔ {other}: 共同节 {common:,}，得到 {len(table):,} 组名字对")

    if args.json_out:
        p = Path(args.json_out); p.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "base": args.base,
            "sections": {l: titles.get(l, {}) for l in langs},
            "names": {o: {k: v for k, v in r["table"].items()} for o, r in results.items()},
        }
        p.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"JSON 已写出：{p}  ({p.stat().st_size/1024:.0f} KB)")

    if args.out:
        L = ["# 术语与角色名 · 五语对照表", "",
             "> 由 `scripts/build_glossary.py` 自动生成：利用**剧情节号跨语言一致**这一锚点，",
             "> 将各语言同一节内的台词按行序对齐，投票得出每个中文角色名在其它语言中的官方译名。",
             "> 「置信」= 该译名在对齐中出现的占比；低于 0.8 的建议人工复核（多半是同一节里两人交替说话造成的错位）。", ""]
        L += ["## 语言与规模", "", "| 语言 | 节数 | 台词数 |", "|---|---|---|"]
        for l in langs:
            n = sum(len(v) for v in seq[l].values()) if l in seq else 0
            L.append(f"| `{l}` | {len(seq.get(l, {})):,} | {n:,} |")
        L.append("")
        for other, r in results.items():
            L += [f"## 角色名对照（{args.base} → {other}）", "",
                  f"共同节 {r['common_sections']:,}；收录 {len(r['table']):,} 组。", "",
                  f"| 中文 | {other} | 置信 | 样本/总对齐 |", "|---|---|---|---|"]
            rows = sorted(r["table"].items(),
                          key=lambda kv: (-base_counts.get(kv[0], 0), kv[0]))
            for zh, v in rows:
                if zh not in keep and base_counts.get(zh, 0) < args.min_lines:
                    continue
                L.append(f"| {zh} | {v['name']} | {v['conf']} | {v['hit']}/{v['total']} |")
            L.append("")
            L += [f"### 章节标题抽样（{args.base} → {other}）", "",
                  f"| 节号 | {args.base} | {other} |", "|---|---|---|"]
            keys = sorted(set(titles.get(args.base, {})) & set(titles.get(other, {})))[:40]
            for k in keys:
                L.append(f"| {k} | {titles[args.base][k]} | {titles[other][k]} |")
            L.append("")
        p = Path(args.out); p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
        print(f"对照表已写出：{p}  ({p.stat().st_size/1024:.0f} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
