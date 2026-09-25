#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成《重返未来1999》角色登场索引
扫描主线/支线/轩事/角色/角色列表，统计每个角色在哪些章节登场。
防幻觉：索引完全基于原始数据文件，不依赖模型记忆。
用法: python character_index.py [-d <数据目录>]    (-h 查看帮助)
输出: data/skill_16_角色登场索引.md

注意（2026-09-25）：
  - 扫描范围仍为主线/支线/轩事；`小径/` 与 `更新_2026-09*/` 增量目录**不在扫描范围内**，
    这些新增登场记录由人工补录进输出文件，**重跑本脚本会覆盖人工补录**，请先备份再合并。
  - 同名地理名词等误匹配可用下方 FALSE_POSITIVE 表排除（已有：德雷克→德雷克海峡）。
"""

import os
import sys
import re
from collections import defaultdict

DATA_MARKERS = ("skill_00_主索引.md", "雨前精编")


def is_data_dir(path):
    """判定目录是否为有效数据根（与 query.ps1 / query.sh / search_index.py 同一口径）"""
    if not path or not os.path.isdir(path):
        return False
    return any(os.path.exists(os.path.join(path, m)) for m in DATA_MARKERS)


def resolve_data_dir(argv=None):
    """解析数据目录（可移植 + 带校验）

    优先级：命令行位置参数 / -d|--data > 环境变量 REV1999_DATA（须为有效数据根）
    > 脚本位置向上推导（../../../data 实际仓库布局、../../data 规范约定）。
    有效数据根 = 目录内存在 skill_00_主索引.md 或 雨前精编/。
    传入 -h/--help 打印用法；参数非法或数据根无效时以退出码 2 结束，绝不静默写坏文件。
    """
    argv = list(sys.argv[1:] if argv is None else argv)
    if any(a in ("-h", "--help") for a in argv):
        print(__doc__.strip())
        raise SystemExit(0)

    positional = []
    i = 0
    while i < len(argv):
        a = argv[i]
        if a in ("-d", "--data"):
            i += 1
            if i >= len(argv):
                print("错误: -d/--data 缺少参数值", file=sys.stderr)
                raise SystemExit(2)
            positional.append(argv[i])
        elif a.startswith("-"):
            print(f'错误: 未知参数 "{a}"\n', file=sys.stderr)
            print(__doc__.strip(), file=sys.stderr)
            raise SystemExit(2)
        else:
            positional.append(a)
        i += 1

    out = positional[0] if positional else None
    if out and not is_data_dir(out):
        print(f'错误: "{out}" 不是有效数据根（缺少 skill_00_主索引.md / 雨前精编/）', file=sys.stderr)
        raise SystemExit(2)
    if not out:
        env = os.environ.get("REV1999_DATA")
        if is_data_dir(env):
            out = env
        elif env:
            print(f'警告: REV1999_DATA="{env}" 不是有效数据根（空目录或路径过期），已回退到脚本位置推导', file=sys.stderr)
    if not out:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        for parts in (("..", "..", "..", "data"), ("..", "..", "data")):
            cand = os.path.normpath(os.path.join(script_dir, *parts))
            if is_data_dir(cand):
                out = cand
                break
    if not out:
        print("错误: 无法定位数据根。请设置有效的 REV1999_DATA 或传入数据目录路径。", file=sys.stderr)
        raise SystemExit(2)
    return out

# 角色名列表（来自角色列表目录的文件名 + 补充别名）
def get_character_names(data_dir):
    """从角色列表目录获取角色名"""
    names = []
    char_dir = os.path.join(data_dir, "角色列表")
    if os.path.isdir(char_dir):
        for f in sorted(os.listdir(char_dir)):
            if f.endswith(".md"):
                name = f[:-3].strip()
                if name and name != "《湖边的女人》":
                    names.append(name)
    return names

# 补充角色别名/核心角色（可能没有独立文件，但剧情常出现）
ALIASES = {
    "维尔汀": ["司辰"],
    "阿尔卡纳": [],
    "康斯坦丁": [],
    "勿忘我": [],
    "Z女士": [],
    "霍夫曼": [],
    "斯奈德": [],
    "苏菲亚": [],
    "210": [],
    "6": [],
    "37": [],
}

def is_pure_number(name):
    """判断角色名是否是纯数字（如 37、6、210）"""
    return bool(re.match(r'^\d+$', name))

# 误匹配排除表：角色名 + 不该计入的紧邻片段（同名地理名词/专名等）
# 例：主线 10TH 里的"德雷克海峡"是地理名词，不是角色"德雷克"登场。
FALSE_POSITIVE = {
    "德雷克": ["海峡"],
}

def count_occurrences(content, char):
    """统计角色名出现次数，纯数字名用词边界避免误匹配（37次/6TH/210人）"""
    if is_pure_number(char):
        # 前后不能是数字或字母，避免匹配"37次""6TH""210人"
        pattern = r'(?<![0-9a-zA-Z])' + re.escape(char) + r'(?![0-9a-zA-Z])'
    else:
        pattern = re.escape(char)
    n = len(re.findall(pattern, content))
    for bad in FALSE_POSITIVE.get(char, []):
        # 角色名紧邻排除片段的（前接或后接）不计入
        n -= len(re.findall(pattern + re.escape(bad), content))
        n -= len(re.findall(re.escape(bad) + pattern, content))
    return max(n, 0)

def main():
    data_dir = resolve_data_dir()
    print(f"数据目录: {data_dir}")

    # 收集角色名
    char_names = get_character_names(data_dir)
    # 合并别名
    all_chars = set(char_names)
    for alias, more in ALIASES.items():
        all_chars.add(alias)
        all_chars.update(more)
    all_chars = sorted(all_chars, key=len, reverse=True)  # 长名优先匹配

    # 扫描目录：主线、支线、轩事
    scan_dirs = {
        "主线": os.path.join(data_dir, "主线"),
        "支线": os.path.join(data_dir, "支线"),
        "轩事": os.path.join(data_dir, "轩事"),
    }

    # 统计：角色 -> [(目录, 文件, 出现次数)]
    appearances = defaultdict(list)
    char_roles = {}  # 角色 -> 角色列表文件中的定位信息

    # 1. 扫描剧情文件
    for cat, dpath in scan_dirs.items():
        if not os.path.isdir(dpath):
            continue
        for fname in sorted(os.listdir(dpath)):
            if not fname.endswith((".md", ".txt")):
                continue
            fpath = os.path.join(dpath, fname)
            try:
                with open(fpath, "r", encoding="utf-8", errors="replace") as f:
                    content = f.read()
            except:
                continue
            # 统计每个角色出现的次数
            for char in all_chars:
                count = count_occurrences(content, char)
                if count > 0:
                    appearances[char].append((cat, fname, count))

    # 2. 从角色列表文件提取定位信息（灵感/介质/香调等）
    char_list_dir = os.path.join(data_dir, "角色列表")
    if os.path.isdir(char_list_dir):
        for fname in os.listdir(char_list_dir):
            if not fname.endswith(".md"):
                continue
            char = fname[:-3]
            try:
                with open(os.path.join(char_list_dir, fname), "r", encoding="utf-8", errors="replace") as f:
                    content = f.read()
            except:
                continue
            # 提取灵感/介质/香调/定位
            info = {}
            for key in ["灵感", "介质", "香调", "定位"]:
                m = re.search(key + r'[：:\s]+([^\n]+)', content)
                if m:
                    info[key] = m.group(1).strip()[:50]
            if info:
                char_roles[char] = info

    # 3. 生成索引文件
    out_lines = []
    out_lines.append("# 重返未来1999 角色登场索引")
    out_lines.append("")
    out_lines.append("本索引由脚本自动生成，基于原始数据文件统计，用于防幻觉——写角色时必须查此索引确认该角色确实在哪些章节登场。")
    out_lines.append("")
    out_lines.append("## 使用说明")
    out_lines.append("- 角色登场 = 该角色名在该章节文本中出现")
    out_lines.append("- 写作/角色扮演前，先查目标角色的登场章节，确认其经历")
    out_lines.append("- 若索引中某角色没有登场记录，说明资料库中无该角色的剧情内容，不要编造")
    out_lines.append("")
    out_lines.append("## 角色登场表")
    out_lines.append("")

    for char in sorted(appearances.keys()):
        info = char_roles.get(char, {})
        info_str = " ".join(f"{k}：{v}" for k, v in info.items())
        out_lines.append(f"### 【{char}】")
        if info_str:
            out_lines.append(info_str)
        out_lines.append("")
        out_lines.append("登场章节：")
        for cat, fname, count in sorted(appearances[char], key=lambda x: x[1]):
            out_lines.append(f"- [{cat}] {fname} (出现{count}次)")
        out_lines.append("")

    # 标注无登场记录的角色
    no_show = [c for c in sorted(all_chars) if c not in appearances]
    if no_show:
        out_lines.append("## 资料库中无剧情登场的角色")
        out_lines.append("（以下角色在主线/支线/轩事中未出现，写作时不要编造其剧情经历）")
        out_lines.append("")
        for c in no_show:
            out_lines.append(f"- {c}")
        out_lines.append("")

    out_path = os.path.join(data_dir, "skill_16_角色登场索引.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(out_lines))

    print(f"完成: {len(appearances)} 个角色有登场记录")
    print(f"输出: {out_path}")

if __name__ == "__main__":
    main()
