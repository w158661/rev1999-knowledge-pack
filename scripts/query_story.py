#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
query_story.py —— 剧情原文检索 CLI（rev1999-text 技能的后端）

把第三方剧情文本库当成一个"可检索的原文数据库"用，支持四种查询：

    # 1) 某角色的台词（可限定章节/关键词）
    python query_story.py --char 牙仙 --limit 20
    python query_story.py --char 维尔汀 --contains 暴雨

    # 2) 全文关键词检索（带前后文）
    python query_story.py --grep 乳牙 --context 2 --limit 30

    # 3) 按节号 / 章节 dump 原文
    python query_story.py --id 3RD-06
    python query_story.py --chapter 故事一无所有 --section "黑羊之墙"

    # 4) 多语言对照（同一节在五种语言下的写法）
    python query_story.py --id 3RD-06 --lang zh-CN,en,ja

语料库路径：--root 或环境变量 STORY_TEXT_ROOT。
默认不写任何文件，只打印；需要留档时自行重定向。
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from extract_story_dialogue import iter_files, parse_file, DIR_KINDS  # noqa: E402


def load(root: Path, langs, kinds=None):
    """返回 [(lang, kind, file, chapter, section, who, text)]"""
    rows = []
    for lang, kind_en, kind_cn, f in iter_files(root, langs):
        if kinds and kind_cn not in kinds:
            continue
        for chapter, section, who, text in parse_file(f):
            rows.append((lang, kind_cn, f.name, chapter, section, who, text))
    return rows


def fmt(r, show_id=True):
    lang, kind, fn, chapter, section, who, text = r
    head = f"[{kind}·{chapter}·{section}]" if show_id else f"[{kind}·{chapter}]"
    return f"{head} {who}：{text}"


def cmd_char(rows, name, limit, contains, lang):
    hit = [r for r in rows if r[5] == name and r[0] == lang and (not contains or contains in r[6])]
    if not hit:
        alt = sorted({r[5] for r in rows if name in r[5]})[:12]
        print(f"没有找到「{name}」在 {lang} 下的台词。" + (f"名称相近的有：{'、'.join(alt)}" if alt else ""))
        return 1
    print(f"== {name} @ {lang}：命中 {len(hit)} 句（显示前 {min(limit, len(hit))}）==\n")
    for r in hit[:limit]:
        print(fmt(r))
    return 0


def cmd_grep(rows, kw, limit, context, lang):
    idx = [i for i, r in enumerate(rows) if kw in r[6] and (not lang or r[0] == lang)]
    print(f"== 关键词「{kw}」：命中 {len(idx)} 行（显示前 {min(limit, len(idx))}）==\n")
    shown = 0
    for i in idx[:limit]:
        if context:
            for j in range(max(0, i - context), min(len(rows), i + context + 1)):
                mark = ">" if j == i else " "
                print(f"{mark} {fmt(rows[j])}")
            print()
        else:
            print(fmt(rows[i]))
        shown += 1
    return 0


def cmd_id(rows, sid, langs):
    sel = [r for r in rows if sid.lower() in r[4].lower()]
    if not sel:
        print(f"没有找到节号「{sid}」。")
        return 1
    bylang = {}
    for r in sel:
        bylang.setdefault(r[0], []).append(r)
    print(f"== 节号 {sid}：{len(sel)} 行，语言 {', '.join(sorted(bylang))} ==\n")
    for lang in sorted(bylang):
        print(f"---- {lang} ----")
        sec = None
        for r in bylang[lang]:
            if r[4] != sec:
                sec = r[4]
                print(f"\n[{r[1]}·{r[3]}·{sec}]")
            print(f"  {r[5]}：{r[6]}")
        print()
    return 0


def cmd_chapter(rows, chapter, section, lang):
    sel = [r for r in rows if r[3] == chapter and (not section or section in r[4]) and r[0] == lang]
    if not sel:
        names = sorted({r[3] for r in rows if r[0] == lang})
        cand = [n for n in names if chapter in n][:10]
        print(f"没有找到章节「{chapter}」。" + (f"相近：{'、'.join(cand)}" if cand else ""))
        return 1
    print(f"== {chapter}" + (f" · {section}" if section else "") + f" @ {lang}：{len(sel)} 行 ==\n")
    sec = None
    for r in sel:
        if r[4] != sec:
            sec = r[4]
            print(f"\n[{sec}]")
        print(f"  {r[5]}：{r[6]}")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="剧情原文检索")
    ap.add_argument("--root", default=os.environ.get("STORY_TEXT_ROOT"))
    ap.add_argument("--lang", default="zh-CN", help="语言目录，可逗号分隔（多语言查询用）")
    ap.add_argument("--kind", help="限定类别：主线/活动/角色剧情/玩法故事/荒原互动/附加片段/影像附文")
    ap.add_argument("--char", help="按角色名检索台词")
    ap.add_argument("--contains", help="配合 --char：只保留含该词的台词")
    ap.add_argument("--grep", help="全文关键词检索")
    ap.add_argument("--context", type=int, default=0, help="配合 --grep：显示前后 N 行")
    ap.add_argument("--id", help="按节号检索，如 3RD-06")
    ap.add_argument("--chapter", help="按章节名检索")
    ap.add_argument("--section", help="配合 --chapter：限定小节名")
    ap.add_argument("--limit", type=int, default=30)
    ap.add_argument("--json", action="store_true", help="以 JSON 输出（便于程序处理）")
    args = ap.parse_args(argv)

    if not args.root:
        print("错误：需要 --root，或设置 STORY_TEXT_ROOT", file=sys.stderr)
        return 2
    root = Path(args.root).expanduser().resolve()
    if not root.is_dir():
        print(f"错误：目录不存在 {root}", file=sys.stderr)
        return 2

    langs = [s.strip() for s in args.lang.split(",") if s.strip()]
    kinds = [args.kind] if args.kind else None
    rows = load(root, langs, kinds)

    if args.json:
        if args.char:
            out = [r for r in rows if r[5] == args.char and (not args.contains or args.contains in r[6])]
        elif args.grep:
            out = [r for r in rows if args.grep in r[6]]
        elif args.id:
            out = [r for r in rows if args.id.lower() in r[4].lower()]
        elif args.chapter:
            out = [r for r in rows if r[3] == args.chapter]
        else:
            out = rows[:0]
        print(json.dumps([{"lang": r[0], "kind": r[1], "file": r[2], "chapter": r[3],
                           "section": r[4], "who": r[5], "text": r[6]} for r in out[:args.limit]],
                         ensure_ascii=False, indent=1))
        return 0

    if args.char:
        return cmd_char(rows, args.char, args.limit, args.contains, langs[0])
    if args.grep:
        return cmd_grep(rows, args.grep, args.limit, args.context, langs[0] if len(langs) == 1 else None)
    if args.id:
        return cmd_id(rows, args.id, langs)
    if args.chapter:
        return cmd_chapter(rows, args.chapter, args.section, langs[0])

    ap.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
