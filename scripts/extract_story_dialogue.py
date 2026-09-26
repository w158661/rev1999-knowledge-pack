#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
extract_story_dialogue.py —— 从「剧情文本库」(Klu5ure/reverse-1999-story-text) 抽取逐字台词语料。

用途
----
把第三方剧情文本库（5 语言 / 216 章 / 约 10.5 万行台词）转成可检索的语料，
供 rev1999 技能包做三件事：
  1. 角色语音库重建（每角色几十~几千句真台词，替代现有几百字的样本）；
  2. 引文校验（技能包里每一条引文都能回到原文核对）；
  3. 多语言对照（同一句在 5 种语言下的写法）。

设计原则
--------
* **只读、不落地文本**：脚本本身可随包分发；抽取结果按需生成到指定路径，默认只打印统计，
  不把游戏原文写进本仓库（版权与体积两方面的考虑）。
* 语料库路径由参数或环境变量 STORY_TEXT_ROOT 指定，不硬编码。

用法
----
    python extract_story_dialogue.py --root /path/to/reverse-1999-story-text --stats
    python extract_story_dialogue.py --root ... --char 牙仙 --limit 40
    python extract_story_dialogue.py --root ... --jsonl out/dialogue.jsonl
    python extract_story_dialogue.py --root ... --char 玛蒂尔达 --lang zh-CN,en --compare

输出格式约定（已核对剧情库实际排版）
------------------------------------
    章标题：  # 故事一无所有
    章信息：  > 主线剧情 · 第 004 章 · 41 节
    节标题：  ## 01 · 3RD-01 · 迦勒底神谕
    台词行：  **十四行诗**：报告教员，灵知的特征是……
    图片行：  *〔图：迦勒底神谕〕*
"""

import argparse
import json
import os
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

DIR_KINDS = {
    "mainline": "主线",
    "activity": "活动",
    "character": "角色剧情",
    "gameplay": "玩法故事",
    "wilderness": "荒原互动",
    "extras": "附加片段",
    "pv-notes": "影像附文",
}

RE_CHAPTER = re.compile(r"^#\s+(.+?)\s*$")
RE_SECTION = re.compile(r"^##\s+(.+?)\s*$")
RE_LINE = re.compile(r"^\*\*(?P<who>[^*]+?)\*\*[：:]\s*(?P<text>.*)$")
RE_IMG = re.compile(r"^[＊*]?〔(?:图|画面)[:：].*〕[＊*]?$")

CJK = re.compile(r"[\u4e00-\u9fff]")


def iter_files(root: Path, langs):
    for lang in langs:
        base = root / lang
        if not base.is_dir():
            continue
        for kind_en, kind_cn in DIR_KINDS.items():
            d = base / kind_en
            if not d.is_dir():
                continue
            for f in sorted(d.glob("*.md")):
                if f.name.lower() == "readme.md":
                    continue
                yield lang, kind_en, kind_cn, f


def parse_file(path: Path):
    """返回 [(节标题, 说话人, 台词), ...]"""
    chapter, section = path.stem, ""
    out = []
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.strip()
        if not line:
            continue
        m = RE_CHAPTER.match(line)
        if m:
            chapter = m.group(1)
            continue
        m = RE_SECTION.match(line)
        if m:
            section = m.group(1)
            continue
        if RE_IMG.match(line):
            continue
        m = RE_LINE.match(line)
        if m:
            out.append((chapter, section, m.group("who").strip(), m.group("text").strip()))
    return out


def collect(root: Path, langs):
    rows = []
    for lang, kind_en, kind_cn, f in iter_files(root, langs):
        for chapter, section, who, text in parse_file(f):
            rows.append({
                "lang": lang, "kind": kind_cn, "chapter": chapter,
                "section": section, "who": who, "text": text,
            })
    return rows


def print_stats(rows, top=40):
    total = len(rows)
    speakers = Counter(r["who"] for r in rows)
    per_lang = Counter(r["lang"] for r in rows)
    print(f"台词总行数 : {total}")
    print(f"说话人标签 : {len(speakers)}")
    print(f"语言分布   : " + "  ".join(f"{k}={v}" for k, v in sorted(per_lang.items())))
    print(f"\n-- 台词数 Top {top} --")
    for name, n in speakers.most_common(top):
        avg = sum(len(r['text']) for r in rows if r['who'] == name) / n
        print(f"  {name:<14} {n:>6} 句   平均 {avg:>5.1f} 字")


def print_char(rows, name, limit, lang="zh-CN"):
    picked = [r for r in rows if r["who"] == name and r["lang"] == lang]
    if not picked:
        print(f"（没有找到说话人「{name}」在 {lang} 下的台词）")
        return
    print(f"== {name}（{lang}）共 {len(picked)} 句，显示前 {min(limit, len(picked))} 句 ==\n")
    for r in picked[:limit]:
        print(f"[{r['kind']}·{r['chapter']}·{r['section']}]")
        print(f"  {r['text']}\n")


def dump_jsonl(rows, out_path: Path, langs=None):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    n = 0
    with out_path.open("w", encoding="utf-8") as fh:
        for r in rows:
            if langs and r["lang"] not in langs:
                continue
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
            n += 1
    print(f"已写出 {n} 行 -> {out_path}")


def compare_langs(rows, name, limit):
    """把同名角色在多种语言下的台词并排抽样（用于多语言写作对照）。"""
    by_lang = defaultdict(list)
    for r in rows:
        if r["who"] == name:
            by_lang[r["lang"]].append(r)
    if not by_lang:
        print(f"（没有找到「{name}」）")
        return
    langs = sorted(by_lang)
    print(f"== {name} 多语言对照（各取前 {limit} 句）==\n")
    for lang in langs:
        print(f"---- {lang}（{len(by_lang[lang])} 句）----")
        for r in by_lang[lang][:limit]:
            print(f"  {r['text']}")
        print()


def main(argv=None):
    ap = argparse.ArgumentParser(description="从剧情文本库抽取逐字台词语料")
    ap.add_argument("--root", default=os.environ.get("STORY_TEXT_ROOT"),
                    help="剧情文本库根目录（含 zh-CN/ en/ ja/ ko/ zh-TW/）；也可用环境变量 STORY_TEXT_ROOT")
    ap.add_argument("--lang", default="zh-CN",
                    help="语言目录，逗号分隔；默认 zh-CN")
    ap.add_argument("--stats", action="store_true", help="打印总体统计")
    ap.add_argument("--char", help="打印某角色的台词样本")
    ap.add_argument("--limit", type=int, default=30, help="样本条数")
    ap.add_argument("--jsonl", help="导出 JSONL 到指定路径（不写进本仓库）")
    ap.add_argument("--compare", action="store_true", help="与 --char 搭配：多语言并排抽样")
    args = ap.parse_args(argv)

    if not args.root:
        print("错误：请用 --root 指定剧情文本库根目录，或设置 STORY_TEXT_ROOT", file=sys.stderr)
        return 2
    root = Path(args.root).expanduser().resolve()
    if not root.is_dir():
        print(f"错误：目录不存在 {root}", file=sys.stderr)
        return 2

    langs = [s.strip() for s in args.lang.split(",") if s.strip()]
    rows = collect(root, langs)
    if not rows:
        print("没有解析到任何台词，请检查目录结构是否为 <lang>/<kind>/*.md", file=sys.stderr)
        return 1

    if args.stats or not (args.char or args.jsonl):
        print_stats(rows)
    if args.char:
        if args.compare:
            compare_langs(rows, args.char, args.limit)
        else:
            print_char(rows, args.char, args.limit, langs[0])
    if args.jsonl:
        dump_jsonl(rows, Path(args.jsonl), set(langs))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
