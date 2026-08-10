# 重返未来1999 知识技能包（rev1999-knowledge-pack）

> **v1.1.0** ｜ 1300+ 数据文件 / 8 个技能 / 21 份深度扩充 / 10 模型适配卡
> 兼容：Claude Code（Claude Code 技能系统）· opencode（`skills.paths` 注册）· 任意对话式 AI（配合"传统对话方案"粘贴使用）

《重返未来1999》完整知识库与创作技能包：**查（query）/ 写（write）/ 扮演（roleplay）/ 配队（team）/ 新手（newbie）/ OC（oc）/ 剧情（story）/ 综合（rev1999）** 八技能分层，覆盖世界观、剧情、角色、系统、九味写作法典、反AI病谱、上下文污染与逻辑核查协议、逐模型适配体系。

数据来源：灰机wiki（res1999.huijiwiki.com）+ 社区同人项目《雨前演练 · Before the Rain》剧情精编（github.com/huoyingfirefly/beforerain）

## 包内容

```
rev1999-pack/
├── skills/              # Claude Code 技能目录
│   ├── rev1999/         # 主技能：综合知识库
│   │   ├── SKILL.md     # 世界观/角色/系统/创作全覆盖
│   │   └── scripts/     # 数据查询脚本
│   ├── rev1999-roleplay/ # 角色扮演技能
│   ├── rev1999-oc/       # OC创作技能
│   ├── rev1999-newbie/   # 新手引导技能
│   ├── rev1999-team/     # 队伍搭配技能
│   ├── rev1999-story/    # 剧情时间线技能
│   ├── rev1999-write/    # 写作辅助技能
│   └── rev1999-query/    # 数据快速查询技能
├── data/                # 数据文件 (1309个, 23MB+)
│   ├── skill_*.md       # 15个知识文档
│   ├── analysis_*.txt   # 16个分析文件
│   ├── 雨前精编/        # 《雨前演练》剧情精编 (交叉验证权威参考)
│   │   ├── 01_世界观与组织.md
│   │   ├── 02_主线剧情精编.md
│   │   ├── 03_支线剧情精编.md
│   │   └── 04_角色生平精编.md
│   ├── 扩充/            # 深度精读扩充卷 (18个文件)
│   ├── 模型适配/        # 模型适配总纲与分模型方案 (由并行任务创建)
│   ├── 主线/ 支线/ 角色/ 角色列表/ 小径/ 轩事/ 活动/
│   ├── 世界观设定/ 物品/ 衣着/ 鬃毛邮报/ 第三扇门/ ...
│   └── ...
├── install.sh           # 安装脚本
└── README.md            # 本文件
```

## 安装

### 方式1：自动安装（Windows / macOS / Linux）

Windows（cmd 或双击）：
```bat
install.bat
```

Windows PowerShell：
```powershell
.\install.bat
```

macOS / Linux：
```bash
cd rev1999-pack
bash install.sh
```

### 方式2：手动安装

macOS / Linux：
```bash
# 复制技能到 Claude Code 技能目录
cp -r rev1999-pack/skills/* .claude/skills/

# 设置数据路径环境变量
echo 'export REV1999_DATA="/path/to/rev1999-pack/data"' >> ~/.bashrc
source ~/.bashrc
```

Windows PowerShell：
```powershell
# 复制技能到 .claude\skills
Copy-Item -Recurse -Force skills\* .claude\skills\

# 设置数据路径环境变量（用户级，永久生效）
[Environment]::SetEnvironmentVariable('REV1999_DATA', 'C:\path\to\rev1999-pack\data', 'User')
```

## 使用方式

Claude Code 中直接输入斜杠命令：

| 命令 | 功能 |
|------|------|
| `/rev1999` | 综合知识库，问任何1999问题 |
| `/rev1999-newbie` | 新手引导（开荒/资源/阵容） |
| `/rev1999-roleplay` | 让AI扮演游戏角色 |
| `/rev1999-oc` | 创作符合世界观的原创角色 |
| `/rev1999-team` | 队伍搭配建议 |
| `/rev1999-story` | 查询剧情时间线 |
| `/rev1999-write` | 1999风格同人写作辅助 |
| `/rev1999-query` | 快速搜索原始数据 |

## 数据查询

Windows（PowerShell）：
```powershell
powershell -ExecutionPolicy Bypass -File skills\rev1999\scripts\query.ps1 "维尔汀" character
powershell -ExecutionPolicy Bypass -File skills\rev1999\scripts\query.ps1 "暴雨" world
powershell -ExecutionPolicy Bypass -File skills\rev1999\scripts\query.ps1 "37" all
```

macOS / Linux：
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
| 雨前精编 | 5 | 《雨前演练》剧情精编（世界观/主线/支线/角色/说明），社区权威参考 |
| 扩充 | 18 | 深度精读扩充卷（剧情/角色/系统/风格/模型适配研究） |
| 模型适配 | 2 | 模型适配总纲与分模型方案（由并行任务创建） |
| 主线 | 15 | 序章~第十三章 |
| 支线 | 22 | 活动剧情 |
| 轩事 | 31 | 支线故事 |
| 活动 | 83 | 版本活动 |
| 版本 | 15 | 版本总览 |
| UTTU | 41 | UTTU挑战 |
| 角色 | 52 | 角色故事/文学 |
| 角色列表 | 133 | 角色数据/机制 |
| 小径 | 112 | 氛围文本/世界观细节 |
| 衣着 | 149 | 皮肤/服装描述 |
| 物品 | 43 | 道具/材料 |
| 荒原 | 354 | 家园系统 |
| 鬃毛邮报 | 75 | 游戏模式 |
| 剧情时间线 | 31 | 官方时间线 |
| 造像 | 7 | 造像系统 |
| 第三扇门 | 5 | 隐藏故事 |
| 恢奇牌儿 | 5 | 成就系统 |
| 收藏品 | 3 | 收藏系统 |
| 其他 | 53 | 其他数据 |
| 合计 | 1309 | — |

## 《雨前演练》融合说明

本包已与社区同人互动剧本游戏《雨前演练 · Before the Rain》（github.com/huoyingfirefly/beforerain / gitee.com/fire-flies/beforerain）的世界观文本（119条RAG片段，约5.1万字）完成融合，用于**交叉验证与补充**：

- 新增 `data/雨前精编/` 作为剧情、角色、世界观类回答的**权威参考**（叙事质感更贴近玩家社区品味）
- `skill_02_时间线与主线.md` 已按《雨前》文本全面修正（暴雨纪年、章节经过、伏笔、势力）
- `skill_03/skill_04/skill_05` 末尾追加《雨前》交叉验证修正节（曲娘、伊索尔德、洛佩拉、蓝手帕、阿莱夫、诺谛卡、马库斯、朔日手记、地球上最后的夜晚、77号往事、1987宇宙组曲、飞驰！明日之城等）
- 技能文件（rev1999 / rev1999-story / rev1999-write / rev1999-roleplay）与 query.sh 均已接入该数据源

使用原则：知识文档与《雨前》文本冲突时，以《雨前》文本为准。

## 知识文档

| 文件 | 大小 | 内容 |
|------|------|------|
| skill_00_主索引.md | 35KB | 导航索引+交叉引用 |
| skill_01_世界观核心.md | 25KB | 暴雨/基金会/重塑之手 |
| skill_02_时间线与主线.md | 74KB | 11次暴雨/主线全览 |
| skill_03_角色百科A.md | 79KB | 25个角色详细档案 |
| skill_04_角色百科B.md | 89KB | 26个角色详细档案 |
| skill_05_支线活动.md | 66KB | 活动版本全览 |
| skill_06_游戏系统.md | 53KB | 战斗/养成/模式 |
| skill_07_文学风格与创作指南.md | 151KB | 风格分析/OC创作 |
| skill_08_术语词典.md | 33KB | 术语/角色/版本索引 |
| skill_09_仿写与OC模板.md | 42KB | 仿写模板/OC九步法 |
| skill_10_世界观深度解读与写作.md | 38KB | 世界观哲学解读/写作 |
| skill_11_角色语音风格库.md | 470KB | 128个角色原声台词 |
| skill_15_写作逻辑与防幻觉指南.md | 13KB | 7大通病/防幻觉五铁律 |
| skill_16_角色登场索引.md | 64KB | 角色登场章节索引 |
| skill_17_角色签到剧场.md | 169KB | 121个角色签到小剧场 |

## 能力覆盖

- 角色扮演（角色百科+说话风格+场景）
- 同人创作（文学风格+创作指南）
- 队伍建议（配队模板+体系+攻略）
- 游戏向导（系统+模式+机制）
- OC创作（9种灵感+介质香调+命名）
- 剧情查询（时间线+主线+活动）
- 数据快速索引（grep+脚本+目录结构）
- AI陷阱规避（反通用描述）

## 扩充与模型适配说明

`data/扩充/` 为深度精读扩充卷（21个文件），由各"深读官"对原始数据逐文件精读整理而成，定位为知识文档（skill_*.md）的深度补充。引用规范：扩充文档每条信息均标注原始出处文件，与已有文档冲突处如实标注、不擅自定对错。

| 文件 | 用途 |
|------|------|
| 01_主线剧情深度全解.md | 主线15章（序章~13TH）逐文件逐行精读深度全解 |
| 02_支线剧情深度全解.md | 官方支线22个文件逐行精读（剧情/角色关系/写作参考） |
| 03_轩事剧情深度全解.md | 31个轩事文件逐个精读，每个轩事一节 |
| 04_活动版本深度全解.md | 活动83/UTTU41/版本15全景深读，冲突如实列出 |
| 05_角色故事文学深度全解.md | 角色52个故事/文学文本逐行精读 |
| 06_角色档案全量.md | 角色列表133人全部角色完整档案（灵感/介质/香调/技能/语音/背景） |
| 07_世界观设定与地点百科.md | 世界观细节库与统一地点百科 |
| 08_系统机制深度全解.md | 游戏系统机制逐文件精读深度全解 |
| 09_物品衣着收藏全解.md | 物品/衣着/收藏系统全解 |
| 10_杂项资源全解.md | 杂项资源全解（其他/文档/官方资料等） |
| 11_全剧情时间线总表.md | 全剧情时间线总表（跨主线/支线/活动/轩事/角色故事） |
| 12_全局人物关系图谱.md | 跨版本全局人物关系图谱（六大阵营全部可考关系） |
| 13_九味风格总纲.md | 九味写作风格法典（写作类技能终极风格参考） |
| 14_同人圈九味考据.md | 玩家社区"9味"考据与同人创作经验 |
| 15_反AI写作病清单.md | 反AI写作病清单（防AI味速查手册） |
| 16_GitHub写作技能蒸馏.md | GitHub活跃写作项目技能蒸馏（反AI味/角色一致性/叙事一致性） |
| 17_模型适配_GPT_Claude_Gemini_Kimi.md | GPT/Claude/Gemini/Kimi 中文创作体验调研与适配方案 |
| 18_模型适配_GLM_DeepSeek_Qwen_MiniMax.md | GLM/DeepSeek/Qwen/MiniMax（含豆包、文心）适配方案 |
| 19_写作资产审计报告.md | 写作资产全量审计（重复/断链/缺口/优先级） |
| 20_九味范文库.md | 官方名场面范文15篇+同人优秀作品索引10篇 |
| 21_上下文污染与逻辑核查协议.md | 全技能逻辑最高权威（三张主权地图/因果链五问/年龄锚点/语音指纹卡） |

`data/模型适配/` 为模型适配卷（2个文件），含**模型适配总纲**（`data/模型适配/总纲.md`）：说明不同模型（GPT/Claude/Gemini/Kimi/GLM/DeepSeek/Qwen/MiniMax等）在1999写作技能上的适配差异——不同模型采用不同的详细度与限制力度（详细度=给多少信息量，限制力度=约束多强硬，二者正交）。扩充卷17/18为各模型适配研究底稿，`模型卡片.md` 为10张逐模型适配卡（含核验日期机制）。

## 许可

- **知识内容**（data/ 数据、skills/ 文档、README 等）：[CC BY-NC-SA 4.0](LICENSE)（知识共享 署名-非商业性使用-相同方式共享 4.0 国际）
  - 数据整理自 灰机wiki 重返未来1999中文维基（res1999.huijiwiki.com，原数据 CC BY-NC-SA 3.0）
  - `data/雨前精编/` 剧情精编整理自《雨前演练 · Before the Rain》（huoyingfirefly/beforerain，MIT）
- **代码与脚本**（scripts/、install.sh、install.bat 等）：[MIT](scripts/LICENSE)
- 详细条款见仓库根 LICENSE