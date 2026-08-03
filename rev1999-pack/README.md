# 重返未来1999 知识技能包

《重返未来1999》完整知识库，适配 Claude Code 技能系统。
数据来源：灰机wiki（res1999.huijiwiki.com）

## 包内容

```
rev1999-pack/
├── skills/              # Claude Code 技能目录
│   ├── rev1999/         # 主技能：综合知识库
│   │   ├── SKILL.md     # 世界观/角色/系统/创作全覆盖
│   │   └── scripts/     # 数据查询脚本
│   ├── rev1999-roleplay/ # 角色扮演技能
│   ├── rev1999-oc/       # OC创作技能
│   ├── rev1999-team/     # 队伍搭配技能
│   ├── rev1999-story/    # 剧情时间线技能
│   └── rev1999-query/    # 数据快速查询技能
├── data/                # 数据文件 (760个, 23MB)
│   ├── skill_*.md       # 9个知识文档 (392KB)
│   ├── analysis_*.txt   # 15个分析文件
│   ├── 主线/ 支线/ 角色/ 角色列表/ 小径/ 轩事/ 活动/
│   ├── 世界观设定/ 物品/ 衣着/ 鬃毛邮报/ 第三扇门/ ...
│   └── ...
├── install.sh           # 安装脚本
└── README.md            # 本文件
```

## 安装

### 方式1：自动安装

```bash
cd rev1999-pack
bash install.sh
```

### 方式2：手动安装

```bash
# 复制技能到 Claude Code 技能目录
cp -r rev1999-pack/skills/* .claude/skills/

# 设置数据路径环境变量
echo 'export REV1999_DATA="/path/to/rev1999-pack/data"' >> ~/.bashrc
source ~/.bashrc
```

## 使用方式

Claude Code 中直接输入斜杠命令：

| 命令 | 功能 |
|------|------|
| `/rev1999` | 综合知识库，问任何1999问题 |
| `/rev1999-roleplay` | 让AI扮演游戏角色 |
| `/rev1999-oc` | 创作符合世界观的原创角色 |
| `/rev1999-team` | 队伍搭配建议 |
| `/rev1999-story` | 查询剧情时间线 |
| `/rev1999-query` | 快速搜索原始数据 |

## 数据查询

```bash
# 设置数据路径
export REV1999_DATA=/path/to/rev1999-pack/data

# 使用查询脚本
bash skills/rev1999/scripts/query.sh "维尔汀" character
bash skills/rev1999/scripts/query.sh "暴雨" world
bash skills/rev1999/scripts/query.sh "37" all

# 直接grep
grep -ri "阿尔卡纳" $REV1999_DATA/skill_*.md
grep -ri "灵感" $REV1999_DATA/世界观设定/
```

## 数据目录

| 目录 | 文件数 | 内容 |
|------|--------|------|
| 世界观设定 | 7 | 暴雨、基金会、重塑之手、神秘学家 |
| 主线 | 15 | 序章~第十三章 |
| 支线 | 22 | 活动剧情 |
| 角色 | 52 | 角色故事/文学 |
| 角色列表 | 133 | 角色数据/机制 |
| 小径 | 112 | 氛围文本/世界观细节 |
| 轩事 | 31 | 支线故事 |
| 活动 | 69 | 版本活动 |
| 物品 | 43 | 道具/材料 |
| 衣着 | 149 | 皮肤/服装描述 |
| 鬃毛邮报 | 75 | 游戏模式 |
| 第三扇门 | 5 | 隐藏故事 |

## 知识文档

| 文件 | 大小 | 内容 |
|------|------|------|
| skill_00_主索引.md | 34KB | 导航索引+交叉引用 |
| skill_01_世界观核心.md | 25KB | 暴雨/基金会/重塑之手 |
| skill_02_时间线与主线.md | 30KB | 11次暴雨/主线全览 |
| skill_03_角色百科A.md | 73KB | 25个角色详细档案 |
| skill_04_角色百科B.md | 78KB | 26个角色详细档案 |
| skill_05_支线活动.md | 57KB | 活动版本全览 |
| skill_06_游戏系统.md | 22KB | 战斗/养成/模式 |
| skill_07_文学风格与创作指南.md | 29KB | 风格分析/OC创作 |
| skill_08_术语词典.md | 30KB | 术语/角色/版本索引 |

## 能力覆盖

- 角色扮演（角色百科+说话风格+场景）
- 同人创作（文学风格+创作指南）
- 队伍建议（配队模板+体系+攻略）
- 游戏向导（系统+模式+机制）
- OC创作（9种灵感+介质香调+命名）
- 剧情查询（时间线+主线+活动）
- 数据快速索引（grep+脚本+目录结构）
- AI陷阱规避（反通用描述）

## 许可

数据来源：灰机wiki 重返未来1999中文维基（CC BY-NC-SA 3.0）
整理制作：社区贡献者