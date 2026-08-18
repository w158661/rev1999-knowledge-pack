# -*- coding: utf-8 -*-
"""
《重返未来：1999》知识技能包 -> LLM 训练数据集转换脚本
输出: JSONL (每条 = {"instruction", "input", "output", "metadata"})
清洗: 移除 wiki 爬取痕迹([编辑]/[图: ...]/huiji 链接/多余空行)
"""
import os
import re
import sys
import json
import hashlib

sys.stdout.reconfigure(encoding='utf-8')

SRC = r'C:\Users\Asus\Desktop\rev1999-pack'
DST = r'C:\Users\Asus\Desktop\shujuji'

# ---------------- 清洗规则 ----------------
def clean_text(t: str) -> str:
    # 去除 BOM
    if t.startswith('\ufeff'):
        t = t[1:]
    # 去除 [编辑] 锚点
    t = re.sub(r'\[\s*编辑\s*\]', '', t)
    # 去除 wiki 图片标记 [图: URL]
    t = re.sub(r'\[图:\s*https?://[^\]]+\]', '', t)
    # 去除 huiji/res1999 链接与缩略图引用
    t = re.sub(r'https?://(?:huiji|res1999)[^\s\)\]]+', '', t)
    # 去除行内 URL 残留
    t = re.sub(r'https?://\S+', '', t)
    # 压缩连续空行
    t = re.sub(r'\n{3,}', '\n\n', t)
    # 去除每行首尾空白
    lines = [l.rstrip() for l in t.split('\n')]
    t = '\n'.join(lines).strip()
    return t


# ---------------- 指令模板 ----------------
def make_record(instruction: str, output: str, category: str, title: str, relpath: str):
    h = hashlib.md5(output.encode('utf-8')).hexdigest()[:12]
    return {
        'instruction': instruction,
        'input': '',
        'output': output,
        'metadata': {
            'category': category,
            'title': title,
            'source': relpath.replace('\\', '/'),
            'hash': h,
            'domain': '重返未来：1999',
        }
    }


CAT_CN = {
    '世界观设定': '世界观设定', '主线': '主线剧情', '支线': '支线剧情',
    '轩事': '轩事剧情', '活动': '活动剧情', 'UTTU': 'UTTU栏目',
    '版本': '版本资料', '角色': '角色档案', '角色列表': '角色列表',
    '小径': '小径文本', '衣着': '衣着资料', '物品': '物品资料',
    '征集': '征集资料', '心相': '心相资料', '律的调校': '律的调校',
    '荒原': '荒原资料', '鬃毛邮报': '鬃毛邮报', '雨中悬想': '雨中悬想',
    '人工梦游': '人工梦游', '签到记录': '签到记录', '配音': '配音资料',
    '官方资料': '官方资料', '过场信息': '过场信息', '前线观察室': '前线观察室',
    '局外演绎': '局外演绎', '沙盘解构': '沙盘解构', '文档': '文档资料',
    '剧情时间线': '剧情时间线', '其他': '杂项资料', '第三扇门': '第三扇门',
    '收藏品': '收藏品', '恢奇牌儿': '恢奇牌儿', '造像': '造像资料',
    '雨前精编': '雨前精编', '扩充': '扩充卷', '模型适配': '模型适配',
    '文风': '文风库', '战斗关卡': '战斗关卡', '同人参考': '同人参考',
    'analysis': '分析文档',
}

INSTRUCTION_BY_CAT = {
    '世界观设定': '以下是《重返未来：1999》世界观设定资料，请学习并掌握：',
    '主线剧情': '以下是《重返未来：1999》主线剧情文本，请学习并掌握剧情内容：',
    '支线剧情': '以下是《重返未来：1999》支线剧情文本，请学习并掌握剧情内容：',
    '轩事剧情': '以下是《重返未来：1999》轩事剧情文本，请学习并掌握剧情内容：',
    '活动剧情': '以下是《重返未来：1999》活动剧情文本，请学习并掌握剧情内容：',
    'UTTU栏目': '以下是《重返未来：1999》UTTU栏目文本，请学习并掌握：',
    '版本资料': '以下是《重返未来：1999》版本资料，请学习并掌握：',
    '角色档案': '以下是《重返未来：1999》角色档案，请学习并掌握该角色信息：',
    '角色列表': '以下是《重返未来：1999》角色列表资料，请学习并掌握：',
    '小径文本': '以下是《重返未来：1999》小径文本，请学习并掌握：',
    '衣着资料': '以下是《重返未来：1999》衣着资料，请学习并掌握：',
    '物品资料': '以下是《重返未来：1999》物品资料，请学习并掌握：',
    '战斗关卡': '以下是《重返未来：1999》战斗关卡文本，请学习并掌握：',
    '人工梦游': '以下是《重返未来：1999》人工梦游文本，请学习并掌握：',
    '官方资料': '以下是《重返未来：1999》官方资料，请学习并掌握：',
    '剧情时间线': '以下是《重返未来：1999》剧情时间线，请学习并掌握：',
    '扩充卷': '以下是《重返未来：1999》深度解析扩充卷，请学习并掌握：',
    '分析文档': '以下是《重返未来：1999》剧情分析文档，请学习并掌握：',
    '同人参考': '以下是《重返未来：1999》同人参考内容（二创，与官方冲突处以官方为准），请学习：',
    '雨前精编': '以下是《重返未来：1999》雨前精编资料，请学习并掌握：',
    '杂项资料': '以下是《重返未来：1999》杂项资料，请学习并掌握：',
    '文档资料': '以下是《重返未来：1999》项目文档，请学习并掌握：',
}


def detect_category(relpath: str) -> str:
    parts = relpath.split(os.sep)
    if parts and parts[0] == 'data':
        parts = parts[1:]
    if not parts:
        return '杂项资料'
    top = parts[0]
    if top in CAT_CN:
        return CAT_CN[top]
    if top == 'analysis' or top.startswith('analysis_'):
        return '分析文档'
    return '杂项资料'


def main():
    os.makedirs(DST, exist_ok=True)
    records = []
    stats = {}

    data_dir = os.path.join(SRC, 'data')
    for root, dirs, files in os.walk(data_dir):
        for f in sorted(files):
            ext = os.path.splitext(f)[1].lower()
            if ext not in ('.md', '.txt'):
                continue
            rel = os.path.relpath(os.path.join(root, f), SRC)
            rel_plain = rel.replace(os.sep, '/')
            try:
                raw = open(os.path.join(root, f), encoding='utf-8').read()
            except Exception:
                continue
            text = clean_text(raw)
            if len(text) < 30:
                continue
            title = f
            if f.endswith('.md'):
                m = re.search(r'^#\s+(.+)$', text, re.M)
                if m:
                    title = m.group(1).strip()
            cat = detect_category(rel)
            instr = INSTRUCTION_BY_CAT.get(cat, '以下是《重返未来：1999》相关资料，请学习并掌握：')
            records.append(make_record(instr, text, cat, title, rel_plain))
            stats[cat] = stats.get(cat, 0) + 1

    # skills 的 SKILL.md 单独处理
    skill_dir = os.path.join(SRC, 'skills')
    if os.path.isdir(skill_dir):
        for name in sorted(os.listdir(skill_dir)):
            sp = os.path.join(skill_dir, name, 'SKILL.md')
            if not os.path.isfile(sp):
                continue
            raw = open(sp, encoding='utf-8').read()
            text = clean_text(raw)
            rel = f'skills/{name}/SKILL.md'
            records.append(make_record(
                f'以下是技能「{name}」的完整定义（{name} 技能），请学习并掌握该技能的工作流：',
                text, '技能定义', f'技能 {name}', rel))
            stats['技能定义'] = stats.get('技能定义', 0) + 1

    # 顶层文档（README/CHANGELOG）
    for f in ['README.md', 'CHANGELOG.md']:
        p = os.path.join(SRC, f)
        if os.path.isfile(p):
            text = clean_text(open(p, encoding='utf-8').read())
            if len(text) > 30:
                records.append(make_record(
                    f'以下是《重返未来：1999》知识技能包的项目文档（{f}），请学习并掌握：',
                    text, '项目文档', f, f))
                stats['项目文档'] = stats.get('项目文档', 0) + 1

    # 写 JSONL
    out_path = os.path.join(DST, 'rev1999_dataset.jsonl')
    with open(out_path, 'w', encoding='utf-8') as fh:
        for r in records:
            fh.write(json.dumps(r, ensure_ascii=False) + '\n')

    # 统计信息
    total_chars = sum(len(r['output']) for r in records)
    info = {
        'dataset': 'rev1999-knowledge-pack',
        'version': 'v2.7.0',
        'domain': '重返未来：1999',
        'format': 'jsonl',
        'schema': {'instruction': 'str', 'input': 'str', 'output': 'str', 'metadata': 'dict'},
        'total_records': len(records),
        'total_chars': total_chars,
        'total_tokens_est': int(total_chars / 1.5),
        'categories': dict(sorted(stats.items(), key=lambda x: -x[1])),
    }
    with open(os.path.join(DST, 'dataset_info.json'), 'w', encoding='utf-8') as fh:
        json.dump(info, fh, ensure_ascii=False, indent=2)

    print(f'记录总数: {len(records)}')
    print(f'总字符: {total_chars:,}')
    print(f'估算 tokens: {int(total_chars/1.5):,}')
    for k, v in sorted(stats.items(), key=lambda x: -x[1]):
        print(f'  {k}: {v}')


if __name__ == '__main__':
    main()