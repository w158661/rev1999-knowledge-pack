#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成《重返未来1999》角色语音风格库
从角色列表文件的【语音Voice】中提取角色原声台词。
防幻觉：完全基于原始数据，不依赖模型记忆。
用法: python voice_extract.py [数据目录]
输出: data/skill_11_角色语音风格库.md
"""

import os
import sys
import re

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

def extract_voice(content):
    """从角色文件内容中提取语音部分的中文台词"""
    # 定位 "语音Voice" 部分
    m = re.search(r'语音[Vv]oice[^\n]*\n', content)
    if not m:
        return None
    start = m.end()
    # 语音部分结束于下个大节
    next_sections = ["尤提姆", "荒原对话", "生日", "剧情立绘", "单品", "文化", "补充"]
    end = len(content)
    for sec in next_sections:
        idx = content.find(sec, start)
        if idx != -1 and idx < end:
            end = idx
    voice_section = content[start:end]

    # 解析：每个语音条目标签行后面跟着 "EN中日한"（或类似），再下一行是中文台词
    lines = voice_section.split("\n")
    results = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        # 跳过语言切换标记行（EN中日한 / EN中日韩 / 等）
        if re.match(r'^(EN|中|日|한|EN中日한|EN中|EN日|EN中日|中英日韩|简体中文|繁体中文|English)', line) or re.match(r'^(EN|中|日|한)$', line):
            # 下一行如果是中文（含中文且非纯标签），则提取
            if i + 1 < len(lines):
                nxt = lines[i+1].strip()
                if re.search(r'[一-鿿]', nxt) and not re.match(r'^[A-Za-z]', nxt):
                    results.append(nxt)
            i += 1
            continue
        # 跳过明显的英文翻译行
        if re.match(r'^[A-Za-z]', line) and not re.search(r'[一-鿿]', line):
            i += 1
            continue
        i += 1

    # 去重保留顺序
    seen = set()
    unique = []
    for r in results:
        if r not in seen and len(r) >= 4:
            seen.add(r)
            unique.append(r)
    return unique

def main():
    data_dir = resolve_data_dir()
    char_dir = os.path.join(data_dir, "角色列表")
    if not os.path.isdir(char_dir):
        print(f"角色列表目录不存在: {char_dir}")
        return

    out_lines = []
    out_lines.append("# 重返未来1999 角色语音风格库")
    out_lines.append("")
    out_lines.append("由脚本自动生成，提取自角色列表文件的【语音】部分。")
    out_lines.append("这些是角色的原声台词，是AI复刻角色说话风格的权威样本。")
    out_lines.append("")
    out_lines.append("## 使用说明")
    out_lines.append("- 角色语音 = 角色在各种情境下的原声台词")
    out_lines.append("- 不同情境（问候/战斗/亲昵/受敌/独白）的语言差异，是还原角色的关键")
    out_lines.append("- 写作/扮演时，参考这些台词的语气、用词、称呼习惯")
    out_lines.append("")

    count = 0
    for fname in sorted(os.listdir(char_dir)):
        if not fname.endswith(".md"):
            continue
        char = fname[:-3]
        try:
            with open(os.path.join(char_dir, fname), "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
        except:
            continue
        voice = extract_voice(content)
        if voice and len(voice) > 3:
            out_lines.append(f"### 【{char}】")
            for v in voice:
                out_lines.append(f"- {v}")
            out_lines.append("")
            count += 1

    out_path = os.path.join(data_dir, "skill_11_角色语音风格库.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(out_lines))

    print(f"完成: {count} 个角色有语音数据")
    print(f"输出: {out_path}")

if __name__ == "__main__":
    main()