# 《重返未来1999》知识技能包（rev1999-knowledge-pack）

<p align="center">
  <img src="https://re.bluepoch.com/home/img/v2.webp" alt="重返未来1999 官网视觉" width="720">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/版本-v2.7.0-blue" alt="版本">
  <img src="https://img.shields.io/badge/数据文件-6098-green" alt="数据文件">
  <img src="https://img.shields.io/badge/技能-8-orange" alt="技能数">
  <img src="https://img.shields.io/badge/深度扩充-77-purple" alt="扩充卷">
  <img src="https://img.shields.io/badge/许可-CC%20BY--NC--SA%204.0-lightgrey" alt="许可">
</p>

> **仓库**：https://github.com/w158661/rev1999-knowledge-pack
> **技能包作者QQ**：3233826425
> **推荐观看**：B站泡面番《1999神秘学对策部》
> 兼容：Claude Code · opencode（`skills.paths` 注册）· 任意对话式 AI（配合"传统对话方案"粘贴使用）

---

## 关于这款游戏

> *"1999年最后一天，'暴雨'降临世界：地面无故溢起积水，你的指尖碰到飞升的雨滴——一场'暴雨'在向天空倾泻。行人和墙壁在雨中剥落溶解，世界似乎来到一个崭新的旧时代。而除了你之外的所有人，都在'暴雨'侵蚀后不知所踪。1999年的秘密，藏在层层雨幕的背后，藏在1999年最后一天。"*
>
> —— 官方开场文案（[重返未来：1999 官方网站](https://re.bluepoch.com/home/)）

《重返未来：1999》是一款 20 世纪复古神秘学策略 RPG。1999 年的最后一天，一场"暴雨"向天空倾泻，世界开始倒退。你将以"司辰"的身份，作为无数时代的见证者，带领神秘学家们逃离"暴雨"。

本技能包是其**完整知识库与创作技能包**：**查 / 写 / 扮演 / 配队 / 新手 / OC / 剧情 / 综合** 八技能分层，覆盖世界观、剧情、角色、系统、九味写作法典、反AI病谱、上下文污染与逻辑核查协议、逐模型适配体系。

<p align="center">
  <img src="https://re.bluepoch.com/home/img/backstory/p1.png" alt="官网世界观视觉" width="480">
</p>

---

## 包内容

```
rev1999-pack/
├── skills/              # 8 个技能（每个含 SKILL.md，主技能含查询脚本）
│   ├── rev1999/         # 综合知识库（含 scripts/query.ps1、query.sh）
│   ├── rev1999-roleplay/ # 角色扮演
│   ├── rev1999-oc/       # OC创作
│   ├── rev1999-newbie/   # 新手引导
│   ├── rev1999-team/     # 队伍搭配
│   ├── rev1999-story/    # 剧情时间线
│   ├── rev1999-write/    # 写作辅助
│   └── rev1999-query/    # 数据快速查询
├── data/                # 6098 个数据文件 / 39 个子目录
│   ├── skill_*.md       # 15 个知识文档
│   ├── analysis_*.txt   # 16 个分析文件
│   ├── 扩充/            # 77 个深度精读扩充卷
│   ├── 雨前精编/        # 《雨前演练》剧情精编（权威参考）
│   ├── 同人参考/        # 同人《雨幕之下》内容提炼
│   ├── 战斗关卡/        # 1851 个战斗关卡页（按章节分类）
│   └── ...
├── CHANGELOG.md         # 版本更新日志
├── install.sh / install.bat
└── README.md            # 本文件
```

## 数据来源

| 来源 | 说明 |
|------|------|
| [灰机wiki · 重返未来1999中文维基](https://res1999.huijiwiki.com/) | 全站 5860 个内容页面 100% 覆盖（主线/支线/角色/系统/战斗关卡等） |
| 《雨前演练 · Before the Rain》（github.com/huoyingfirefly/beforerain） | 社区剧情精编，交叉验证权威参考 |
| 同人《雨幕之下》（作者 B站 F0Y208J524，QQ群 1065146736） | 角色外观服装分区描写/人设档案/文化背景/时间线/小说《夜曲：1929》 |
| [重返未来：1999 官方网站](https://re.bluepoch.com/home/)（深蓝互动） | 官方开场文案与视觉（仅展示用途，版权归深蓝互动所有） |

## 安装

### 方式1：自动安装
- Windows：双击 `install.bat`
- macOS / Linux：`bash install.sh`

### 方式2：手动安装
```bash
# 复制技能到 Claude Code 技能目录
cp -r rev1999-pack/skills/* .claude/skills/
# 设置数据路径环境变量
echo 'export REV1999_DATA="/path/to/rev1999-pack/data"' >> ~/.bashrc
```
Windows PowerShell：
```powershell
Copy-Item -Recurse -Force skills\* .claude\skills\
[Environment]::SetEnvironmentVariable('REV1999_DATA', 'C:\path\to\rev1999-pack\data', 'User')
```

## 使用方式

| 命令 | 功能 |
|------|------|
| `/rev1999` | 综合知识库，问任何1999问题 |
| `/rev1999-roleplay` | 让AI扮演游戏角色 |
| `/rev1999-oc` | 创作符合世界观的原创角色 |
| `/rev1999-team` | 队伍搭配建议 |
| `/rev1999-story` | 查询剧情时间线 |
| `/rev1999-write` | 1999风格同人写作辅助 |
| `/rev1999-newbie` | 新手引导（开荒/资源/阵容） |
| `/rev1999-query` | 快速搜索原始数据 |

每次加载技能时，AI 会输出固定首句（项目链接/作者/同人致谢/B站番推荐）。

## 数据查询

Windows（PowerShell）：
```powershell
powershell -ExecutionPolicy Bypass -File skills\rev1999\scripts\query.ps1 "维尔汀" character
powershell -ExecutionPolicy Bypass -File skills\rev1999\scripts\query.ps1 "黄昏的音序" stage
```
macOS / Linux：
```bash
bash skills/rev1999/scripts/query.sh "暴雨" world
bash skills/rev1999/scripts/query.sh "黄昏的音序" stage   # 活动名直达关卡目录
```
类型：`all / character / world / story / stage / fan / skill`。

## 数据目录

| 目录 | 文件数 | 内容 |
|------|--------|------|
| 战斗关卡 | 1851 | 主线14章296/支线24条475/活动18个664/轩事27个198/角色剧情65/材料关卡47/模式106 |
| 其他 | 2220 | 剧情文本、角色个人故事、活动变体、特殊页 |
| 荒原 | 444 | 家园系统（建筑/孤屿/装潢/主题） |
| 人工梦游 | 462 | 浅眠10/深眠371/醒梦68/怪梦栖所12 |
| 衣着 | 148 | 皮肤/服装描述 |
| 扩充 | 77 | 深度精读扩充卷（含 36~42 实测/调研/种族/链接系列） |
| 角色列表 | 143 | 角色数据/机制 |
| 小径 | 113 | 氛围文本/世界观细节 |
| 活动 | 58 | 版本活动 |
| 鬃毛邮报 | 76 | 游戏模式 |
| 角色 | 51 | 角色故事/文学 |
| UTTU | 41 | UTTU挑战 |
| 轩事 | 39 | 支线故事 |
| 剧情时间线 | 31 | CG图库索引 |
| 官方资料 | 19 | 官方美术/漫画 |
| 版本 | 16 | 版本总览 |
| 主线 | 15 | 序章~第十三章 |
| 支线 | 23 | 活动剧情 |
| 造像 | 133 | 角色造像道具页 |
| 同人参考 | 7 | 同人《雨幕之下》内容提炼 |
| 雨前精编 | 6 | 《雨前演练》剧情精编（含 05_更新补充） |
| 世界观设定 | 10 | 暴雨/基金会/重塑之手/神秘学家/意识唤醒者/人类等 |
| 物品 | 43 | 道具/材料 |
| 模型适配 | 2 | 模型适配总纲与分模型方案 |
| 文档 | 4 | 爬取记录/普查 |
| 其余 | ~30 | 心相/征集/签到/沙盘/收藏/配音等 |
| **合计** | **6098** | 39 个子目录（2026-08-18 实测口径；v2.7.0 新增3.9版本25文件） |

## 知识文档

| 文件 | 内容 |
|------|------|
| skill_00_主索引.md | 全库导航主索引（v2.3/2.4 登记） |
| skill_01_世界观核心.md | 暴雨/基金会/重塑之手/神秘学家 |
| skill_02_时间线与主线.md | 暴雨纪年（10次确认+序章推算）/主线全览/伏笔网络（按《雨前》修正） |
| skill_03/04_角色百科A/B.md | 51 个角色详细档案 |
| skill_05_支线活动.md | 版本体系/活动/支线/轩事全览 |
| skill_06_游戏系统.md | 战斗/养成/模式 |
| skill_07_文学风格与创作指南.md | 风格分析/OC/同人创作 |
| skill_08_术语词典.md | 术语/角色/版本索引 |
| skill_09_仿写与OC模板.md | 仿写模板/OC九步法 |
| skill_10_世界观深度解读与写作.md | 世界观哲学解读/写作 |
| skill_11_角色语音风格库.md | 128 个角色原声台词 |
| skill_15_写作逻辑与防幻觉指南.md | 7大通病/防幻觉五铁律 |
| skill_16_角色登场索引.md | 角色登场章节索引 |
| skill_17_角色签到剧场.md | 121 个角色签到小剧场 |

## 扩充卷亮点

- **13_九味风格总纲** / **40_社区文风调研**：九味写作法典 + 社区实证（9味共识10条/AI味判据12条）
- **15_反AI写作病清单**：31 病种 + N 系强化 + 社区实证病种 N6~N14（症状/成因/修法/反例/正例）
- **20_九味范文库**：官方名场面 15 篇 + 同人优秀作品索引 10 篇
- **21_上下文污染与逻辑核查协议**：三张主权地图/因果链五问/语音指纹卡
- **28~34 关卡深度全解**：主线/支线/活动/轩事/角色/材料/模式/战斗关卡全量深读
- **36~39 实测与鉴证报告**：22 份技能实测（写作/扮演/群像/恐怖/推理/长程一致性等）

## 同人融合致谢

- **《雨幕之下》**：作者 B站 **F0Y208J524**，同人QQ群 **1065146736** —— 角色外观服装分区描写、人设档案、文化背景、同人时间线、小说《夜曲：1929》
- **《雨前演练 · Before the Rain》**：作者 B站 **雨蝇rainfly**（github.com/huoyingfirefly/beforerain，MIT）—— 剧情精编交叉验证
- **推荐观看**：B站泡面番 **《1999神秘学对策部》**

## 许可

- **知识内容**（data/、skills/、README 等）：[CC BY-NC-SA 4.0](LICENSE)
  - 数据整理自 灰机wiki 重返未来1999中文维基（原数据 CC BY-NC-SA 3.0）
  - `data/雨前精编/` 整理自《雨前演练 · Before the Rain》（MIT）
  - `data/同人参考/` 经作者授权融合，引用请保留来源标注
- **代码与脚本**（scripts/、install.sh、install.bat 等）：[MIT](scripts/LICENSE)
- **官网图片**：仅作 README 展示用途，版权归深蓝互动所有
