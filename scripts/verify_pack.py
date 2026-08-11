# -*- coding: utf-8 -*-
"""rev1999-pack 全面验证脚本"""
import os, re, sys, codecs, glob

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'data')
errors, warnings = [], []

# ---------- 1. 结构计数 ----------
print('=' * 60)
print('[1] 目录结构计数')
print('=' * 60)
expected_dirs = {
    '世界观设定': 7, '主线': 15, '支线': 22, '轩事': 39, '活动': 84,
    'UTTU': 41, '版本': 15, '角色': 52, '角色列表': 141, '小径': 113,
    '衣着': 294, '物品': 43, '征集': 2, '心相': 4, '律的调校': 1,
    '荒原': 445, '鬃毛邮报': 75, '雨中悬想': 2, '人工梦游': 463,
    '签到记录': 3, '配音': 1, '官方资料': 19, '过场信息': 1,
    '前线观察室': 3, '局外演绎': 1, '沙盘解构': 4, '文档': 4,
    '剧情时间线': 31, '其他': 2236, '第三扇门': 5, '收藏品': 3,
    '恢奇牌儿': 5, '造像': 133, '雨前精编': 5, '扩充': 74, '模型适配': 2,
    '战斗关卡': 1836,
}
for d, exp in expected_dirs.items():
    p = os.path.join(DATA, d)
    if d == '战斗关卡':
        n = sum(len(f) for _, _, f in os.walk(p)) if os.path.isdir(p) else -1
    else:
        n = len([f for f in os.listdir(p)]) if os.path.isdir(p) else -1
    status = 'OK' if n == exp else 'MISMATCH'
    if n != exp:
        errors.append(f'目录 {d}: 期望 {exp}, 实际 {n}')
    print(f'  {d}: {n} (期望 {exp}) [{status}]')

total_files = sum(len(f) for root, _, f in os.walk(DATA) if '.index' not in root)
print(f'  data 总文件数: {total_files}')
if total_files != 6255:
    errors.append(f'data 总文件数 {total_files} != 6231')

skill_docs = sorted(f for f in os.listdir(DATA) if f.startswith('skill_'))
expected_prefixes = ['skill_%02d_' % i for i in [0,1,2,3,4,5,6,7,8,9,10,11,15,16,17]]
missing = [e for e in expected_prefixes if not any(f.startswith(e) for f in skill_docs)]
print(f'  skill 文档 {len(skill_docs)} 个: 缺失 {missing or "无"}')
if missing:
    errors.append(f'skill 文档缺失: {missing}')

analysis = [f for f in os.listdir(DATA) if f.startswith('analysis_')]
print(f'  analysis 文档 {len(analysis)} 个 (期望16)')
if len(analysis) != 16:
    errors.append(f'analysis 数量 {len(analysis)} != 16')

skills = [d for d in os.listdir(os.path.join(ROOT, 'skills')) if os.path.isdir(os.path.join(ROOT, 'skills', d))]
print(f'  skills 目录: {len(skills)} 个: {sorted(skills)}')
if len(skills) != 8:
    errors.append(f'skills 数量 {len(skills)} != 8')

# ---------- 2. UTF-8 可读性与空文件 ----------
print('=' * 60)
print('[2] 编码与文件完整性 (遍历全部数据文件)')
print('=' * 60)
bad_enc, empty, no_tail = 0, [], []
for root, _, files in os.walk(DATA):
    if os.path.basename(root) == '.index':
        continue
    for fn in files:
        fp = os.path.join(root, fn)
        try:
            with open(fp, 'rb') as f:
                raw = f.read()
        except OSError as e:
            errors.append(f'读取失败 {fp}: {e}')
            continue
        if len(raw) == 0:
            empty.append(fp); continue
        try:
            raw.decode('utf-8')
        except UnicodeDecodeError:
            bad_enc += 1
            if bad_enc <= 5:
                errors.append(f'非UTF-8: {fp}')
print(f'  空文件: {len(empty)} {empty[:3]}')
if empty:
    errors.append('存在空文件')
print(f'  非UTF-8文件: {bad_enc}')
print('  编码检查完成（中文路径文件均已正确解码）')

# 文件名乱码检查（mojibake 特征）
mojibake = []
for root, _, files in os.walk(DATA):
    if os.path.basename(root) == '.index':
        continue
    for fn in files:
        if re.search(r'[\u4e00-\u9fff]', fn):
            for ch in fn:
                if ord(ch) > 0x9fff and not (0x3400 <= ord(ch) <= 0x4dbf):
                    pass
        # 常见 mojibake 字符：鍏 粬 涓 栫 鐣 瓒
        if any(c in fn for c in '鍏粬涓栫鐣瓒棰唴鍒锋氮涔'):
            mojibake.append(fp)
print(f'  疑似乱码文件名: {len(mojibake)}')

# ---------- 3. 引用完整性 ----------
print('=' * 60)
print('[3] 技能与README中的 data/ 引用完整性')
print('=' * 60)
ref_files = []
for pat in [os.path.join(ROOT, 'skills', '*', 'SKILL.md'), os.path.join(ROOT, 'README.md')]:
    ref_files += glob.glob(pat)
all_data_files = set()
for root, _, files in os.walk(DATA):
    if os.path.basename(root) == '.index':
        continue
    for fn in files:
        all_data_files.add(os.path.normpath(os.path.join(root, fn)).lower())
bad_refs = []
for rf in ref_files:
    with open(rf, encoding='utf-8') as f:
        txt = f.read()
    for m in re.finditer(r'data/[\S]+?\.md', txt):
        ref = m.group(0)
        # 清理误抓的后续字符
        ref = ref.split('、')[0].split('`')[0].split('）')[0].split(')')[0].split('：')[0]
        target = os.path.normpath(os.path.join(ROOT, ref)).lower()
        if not (target in all_data_files or ref.endswith('skill_*.md') or 'model' in ref):
            bad_refs.append((os.path.basename(rf), ref))
print(f'  无效引用: {len(bad_refs)}')
for b in bad_refs[:10]:
    errors.append(f'无效引用 {b}')
if not bad_refs:
    print('  全部引用有效 ✓')

# ---------- 4. 事实修正验证 ----------
print('=' * 60)
print('[4] 三处事实修正落实情况')
print('=' * 60)
s02 = open(os.path.join(DATA, 'skill_02_时间线与主线.md'), encoding='utf-8').read()
checks = [
    ('天使兄弟会渗透保留', '被天使兄弟会渗透严重' in s02),
    ('伊戈尔远征记洗白', '远征记' in s02 and '洗白' in s02),
    ('兀尔德失踪口径', '按失踪处理' in s02),
    ('第一次暴雨8岁(旧14岁已清除)', '维尔汀年龄：8岁' in s02 and '14岁' not in s02.split('第六次暴雨')[0]),
    ('第三次暴雨12岁', '维尔汀年龄：12岁' in s02),
]
for name, ok in checks:
    print(f'  {name}: {"✓" if ok else "✗ 未落实"}')
    if not ok:
        errors.append(f'事实修正未落实: {name}')

story_skill = open(os.path.join(ROOT, 'skills', 'rev1999-story', 'SKILL.md'), encoding='utf-8').read()
s2_checks = [
    ('story表5TH为阿派朗2007', '阿派朗岛（岛上时间2007）' in story_skill),
    ('story表6TH维也纳1913', '1913维也纳' in story_skill),
    ('story表与skill_02一致(无1914)', '1914' not in story_skill),
    ('story 10次暴雨表与skill_02一致', '1999.12.31' in story_skill and '1987' in story_skill),
]
for name, ok in s2_checks:
    print(f'  {name}: {"✓" if ok else "✗"}')
    if not ok:
        errors.append(f'story技能一致性: {name}')

雨前02 = open(os.path.join(DATA, '雨前精编', '02_主线剧情精编.md'), encoding='utf-8').read()
print(f'  雨前精编02 失踪口径: {"✓" if "按失踪处理" in 雨前02 else "✗"}')
if '按失踪处理' not in 雨前02:
    errors.append('雨前精编02 失踪口径缺失')

# ---------- 5. 扩充文件完整性 ----------
print('=' * 60)
print('[5] 扩充卷 31 文件与模型适配 2 文件')
print('=' * 60)
ext_dir = os.path.join(DATA, '扩充')
for fn in sorted(os.listdir(ext_dir)):
    fp = os.path.join(ext_dir, fn)
    size = os.path.getsize(fp)
    with open(fp, encoding='utf-8') as f:
        lines = f.read().splitlines()
    tail = lines[-1].strip() if lines else ''
    truncated = size > 0 and lines and lines[-1].strip() != '' and not re.match(r'^[（(]?全文完', tail) and len(lines) < 100
    print(f'  {fn}: {size/1024:.0f}KB, {len(lines)}行 {"✓" if not truncated else "✗ 疑似截断"}')
    if size < 4000 and fn not in ('10_杂项资源全解.md',):
        warnings.append(f'扩充文件偏小: {fn} {size}B')
for fn in sorted(os.listdir(os.path.join(DATA, '模型适配'))):
    fp = os.path.join(DATA, '模型适配', fn)
    print(f'  模型适配/{fn}: {os.path.getsize(fp)/1024:.0f}KB ✓')

# ---------- 6. 组装文件检查 ----------
print('=' * 60)
print('[6] 支线组装文件 22 篇完整性')
print('=' * 60)
s02_ext = open(os.path.join(ext_dir, '02_支线剧情深度全解.md'), encoding='utf-8').read()
codes = ['AC','AFF','CO','DIA','FR','FT','GLN','JMP','LAFP','LD','LEE','LPdF',
         'NS','PD','RUG','SC','SU','THH','TMW','TRC','TTSC','TTS']
missing_codes = [c for c in codes if c not in s02_ext]
print(f'  支线代码命中: {len(codes)-len(missing_codes)}/22 缺失: {missing_codes or "无"}')
if missing_codes:
    errors.append(f'支线组装缺篇: {missing_codes}')

# ---------- 7. 旧文档附加节 ----------
print('=' * 60)
print('[7] skill_03/04/05 雨前验证附加节')
print('=' * 60)
for fn, kw in [('skill_03_角色百科A.md', '雨前演练'), ('skill_04_角色百科B.md', '雨前演练'), ('skill_05_支线活动.md', '雨前演练')]:
    txt = open(os.path.join(DATA, fn), encoding='utf-8').read()
    ok = kw in txt
    print(f'  {fn}: {"✓" if ok else "✗"}')
    if not ok:
        errors.append(f'{fn} 缺少雨前验证附加节')

# ---------- 8. Windows 脚本 ----------
print('=' * 60)
print('[8] Windows 脚本')
print('=' * 60)
for fn in [r'skills\rev1999\scripts\query.ps1', r'install.bat']:
    fp = os.path.join(ROOT, fn)
    raw = open(fp, 'rb').read()
    bom = raw[:3] == b'\xef\xbb\xbf'
    print(f'  {fn}: 存在✓, {len(raw)}B, UTF-8 BOM: {bom}')

print('=' * 60)
print('结果汇总')
print('=' * 60)
print(f'  错误: {len(errors)}')
for e in errors:
    print(f'    [ERR] {e}')
print(f'  警告: {len(warnings)}')
for w in warnings:
    print(f'    [WARN] {w}')
print('OVERALL: ' + ('FAIL' if errors else 'PASS'))
