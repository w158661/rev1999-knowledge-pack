#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成《重返未来1999》角色签到剧场档案
从签到数据中按角色归集所有相关条目，形成每个角色的日常小剧场。
防幻觉：完全基于原始签到数据，不依赖模型记忆。
用法: python checkin_profile.py [数据目录]
输出: data/skill_17_角色签到剧场.md
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

# 核心角色别名，签到中可能用全名或别称
CORE_CHARS = [
    "维尔汀", "十四行诗", "星锑", "苏芙比", "37", "6", "210", "伊索尔德",
    "卡卡尼亚", "红弩箭", "槲寄生", "牙仙", "可燃点", "曲娘", "葛天",
    "北方哨歌", "露西", "X", "兔毛手袋", "帕米埃", "温妮弗雷德",
    "小春雀儿", "泥鯭的士", "远旅", "APPLe", "无名者", "洛伦兹蝴蝶",
    "玛尔纱", "程和光", "鹭鸶剪", "回声谣", "奠基石", "小瑞安侬",
    "拉莫纳", "伊戈尔", "塞梅尔维斯", "夏利", "皮克勒斯", "新巴别塔",
    "玛丽安娜", "莫莉德尔", "梅兰妮", "坎吉拉", "图图石子",
    "灰调蓝", "贝丽尔", "阿莱夫", "野树莓", "库珀花环", "芭卡洛儿",
    "纸信圈儿", "数羊羔", "蓝手帕", "珐琅眼", "埃里克",
]

def CORE_ALIASES_ADDITIONAL():
    """额外补充的核心角色（不在角色列表文件中但剧情常见）"""
    return set(CORE_CHARS)

def is_pure_number(name):
    return bool(re.match(r'^\d+$', name))

def count_line(line, name):
    """判断一行是否提到该角色（纯数字需要边界）"""
    if is_pure_number(name):
        return bool(re.search(r'(?<![0-9a-zA-Z])' + re.escape(name) + r'(?![0-9a-zA-Z])', line))
    return name in line

def main():
    data_dir = resolve_data_dir()
    checkin_file = os.path.join(data_dir, "签到记录", "签到数据_格式化.md")
    if not os.path.exists(checkin_file):
        print(f"签到数据不存在: {checkin_file}")
        return

    # 收集角色名（优先用角色列表的文件名）
    char_names = get_character_names(data_dir)
    all_chars = set(char_names)
    all_chars.update(CORE_ALIASES_ADDITIONAL())
    # 按长度排序，优先匹配长名
    all_chars = sorted(all_chars, key=len, reverse=True)

    # 读取签到数据
    with open(checkin_file, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()

    # 解析：跳过标题和日期行，只收集条目行
    entries_by_char = defaultdict(list)

    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        # 跳过纯日期/标题/分隔行（含 #、##、---、日期格式）
        if line.startswith("#") or line.startswith("-") or line.startswith("---"):
            continue
        # 跳过 "### 2023-" 这类日期标题
        if re.match(r'^#{2,3}\s\d{4}', raw):
            continue
        if "年" in line and len(line) < 15 and re.match(r'^#', raw):
            continue
        if len(line) < 8:
            continue
        # 一条条目可包含多个角色，记录给所有命中的角色
        for char in all_chars:
            if count_line(line, char):
                entries_by_char[char].append(line)

    # 生成输出
    out_lines = []
    out_lines.append("# 重返未来1999 角色签到剧场")
    out_lines.append("")
    out_lines.append("本档案由脚本自动生成，基于签到数据（1279条）。")
    out_lines.append("每条记录是该角色的日常小剧场/世界观碎片，可用于：")
    out_lines.append("- 补充角色性格细节（角色在剧情的日常状态）")
    out_lines.append("- 同人创作的日常素材（角色会做什么、喜欢什么）")
    out_lines.append("- 防幻觉（角色行为必须来自这些数据）")
    out_lines.append("")

    # 按出场条目数排序
    sorted_chars = sorted(entries_by_char.items(), key=lambda x: -len(x[1]))

    for char, items in sorted_chars:
        if len(items) < 2:
            continue  # 只保留有较丰富数据的角色
        out_lines.append(f"### 【{char}】")
        out_lines.append(f"签到剧场（{len(items)}条）：")
        for item in items:
            out_lines.append(f"- {item}")
        out_lines.append("")

    out_path = os.path.join(data_dir, "skill_17_角色签到剧场.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(out_lines))

    print(f"完成: {len([k for k in entries_by_char if len(entries_by_char[k])>=2])} 个角色有签到剧场")
    print(f"输出: {out_path}")

if __name__ == "__main__":
    main()