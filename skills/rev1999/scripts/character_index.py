#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成《重返未来1999》角色登场索引
扫描主线/支线/轩事/角色/角色列表，统计每个角色在哪些章节登场。
防幻觉：索引完全基于原始数据文件，不依赖模型记忆。
用法: python character_index.py [数据目录]
输出: data/skill_16_角色登场索引.md
"""

import os
import sys
import re
from collections import defaultdict

def resolve_data_dir():
    """解析数据目录（三级兜底：环境变量 > ../../../data 实际仓库布局 > ../../data 规范约定）"""
    if len(sys.argv) > 1:
        return sys.argv[1]
    env = os.environ.get("REV1999_DATA")
    if env:
        return env
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # 实际仓库布局: ../../../data/ (scripts -> rev1999 -> skills -> rev1999-pack -> data)
    candidate = os.path.normpath(os.path.join(script_dir, "..", "..", "..", "data"))
    if os.path.isdir(candidate):
        return candidate
    # 规范约定: ../../data/
    candidate = os.path.normpath(os.path.join(script_dir, "..", "..", "data"))
    if os.path.isdir(candidate):
        return candidate
    # 兜底返回实际仓库布局路径（即使不存在，由调用方报错）
    return os.path.normpath(os.path.join(script_dir, "..", "..", "..", "data"))

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

def count_occurrences(content, char):
    """统计角色名出现次数，纯数字名用词边界避免误匹配（37次/6TH/210人）"""
    if is_pure_number(char):
        # 前后不能是数字或字母，避免匹配"37次""6TH""210人"
        pattern = r'(?<![0-9a-zA-Z])' + re.escape(char) + r'(?![0-9a-zA-Z])'
    else:
        pattern = re.escape(char)
    return len(re.findall(pattern, content))

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
