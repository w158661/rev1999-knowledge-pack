#!/bin/bash
# 重返未来1999 数据查询脚本
# 用法: ./query.sh <关键词> [文件类型]
# 文件类型: all(默认), character, story, system, world, event
# 优先使用 Python 搜索索引，不可用时降级为 grep

KEYWORD="$1"
TYPE="${2:-all}"

# 数据路径: 优先使用 REV1999_DATA 环境变量，否则包内路径
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PACKAGE_DATA="$(cd "$SCRIPT_DIR/../../.." && pwd)/data"
if [ -n "$REV1999_DATA" ] && [ -d "$REV1999_DATA" ]; then
  BASE="$REV1999_DATA"
else
  BASE="$PACKAGE_DATA"
fi

if [ ! -d "$BASE" ]; then
  echo "错误: 数据目录不存在 ($BASE)"
  echo "请设置 REV1999_DATA 环境变量指向数据目录"
  echo "export REV1999_DATA=/path/to/rev1999-pack/data"
  exit 1
fi

# 检查 Python 是否可用
PYTHON_BIN=""
if command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="python3"
elif command -v python >/dev/null 2>&1; then
  PYTHON_BIN="python"
fi

# 检查搜索索引脚本是否存在且索引已构建（先查 BASE，再查包内路径）
SEARCH_SCRIPT="$(cd "$(dirname "$0")" && pwd)/search_index.py"
INDEX_FILE="$BASE/.index/inverted_index.pkl"
if [ ! -f "$INDEX_FILE" ] && [ -f "$PACKAGE_DATA/.index/inverted_index.pkl" ]; then
  INDEX_FILE="$PACKAGE_DATA/.index/inverted_index.pkl"
fi
USE_PYTHON=0
if [ -n "$PYTHON_BIN" ] && [ -f "$SEARCH_SCRIPT" ] && [ -f "$INDEX_FILE" ]; then
  USE_PYTHON=1
fi

# Python 搜索统一使用包内数据目录（索引所在位置）
PY_BASE="$BASE"
if [ -f "$PACKAGE_DATA/.index/inverted_index.pkl" ]; then
  PY_BASE="$PACKAGE_DATA"
fi

# Python 搜索模式
if [ "$USE_PYTHON" -eq 1 ]; then
  case "$TYPE" in
    all|character|story|system|world|event)
      "$PYTHON_BIN" "$SEARCH_SCRIPT" search "$KEYWORD" --type "$TYPE" --top 20 --datadir "$PY_BASE"
      ;;
    related)
      "$PYTHON_BIN" "$SEARCH_SCRIPT" related "$KEYWORD" --datadir "$PY_BASE"
      ;;
    *)
      echo "用法: ./query.sh <关键词> [类型]"
      echo "类型: all, character, story, system, world, event, stage, related"
      echo "示例: ./query.sh 维尔汀 character"
      echo "      ./query.sh 暴雨 world"
      echo "      ./query.sh 维尔汀 related"
      exit 1
      ;;
  esac
  exit 0
fi

# 降级模式: grep 搜索
echo "提示: Python搜索不可用，使用grep降级模式 (运行 search_index.py build 启用索引)"
echo ""

case "$TYPE" in
  character)
    echo "=== 搜索角色资料 ==="
    grep -ri "$KEYWORD" "$BASE/角色/" "$BASE/角色列表/" 2>/dev/null | head -50
    grep -ri "$KEYWORD" "$BASE/skill_03_角色百科A.md" "$BASE/skill_04_角色百科B.md" 2>/dev/null | head -30
    echo "--- 雨前精编(权威) ---"
    grep -ri "$KEYWORD" "$BASE/雨前精编/04_角色生平精编.md" 2>/dev/null | head -30
    echo "--- 扩充卷(权威) ---"
    grep -ri "$KEYWORD" "$BASE/扩充/06_角色档案全量.md" "$BASE/扩充/24_造像深度全解.md" 2>/dev/null | head -20
    ;;
  story)
    echo "=== 搜索剧情 ==="
    grep -ri "$KEYWORD" "$BASE/主线/" "$BASE/支线/" 2>/dev/null | head -50
    grep -ri "$KEYWORD" "$BASE/skill_02_时间线与主线.md" "$BASE/skill_05_支线活动.md" 2>/dev/null | head -30
    echo "--- 雨前精编(权威) ---"
    grep -ri "$KEYWORD" "$BASE/雨前精编/02_主线剧情精编.md" "$BASE/雨前精编/03_支线剧情精编.md" 2>/dev/null | head -30
    echo "--- 扩充卷(深度) ---"
    grep -ri "$KEYWORD" "$BASE/扩充/01_主线剧情深度全解.md" "$BASE/扩充/02_支线剧情深度全解.md" "$BASE/扩充/11_全剧情时间线总表.md" 2>/dev/null | head -20
    ;;
  system)
    echo "=== 搜索游戏系统 ==="
    grep -ri "$KEYWORD" "$BASE/征集/" "$BASE/心相/" "$BASE/鬃毛邮报/" 2>/dev/null | head -50
    grep -ri "$KEYWORD" "$BASE/skill_06_游戏系统.md" 2>/dev/null | head -30
    ;;
  world)
    echo "=== 搜索世界观 ==="
    grep -ri "$KEYWORD" "$BASE/世界观设定/" "$BASE/小径/" 2>/dev/null | head -50
    grep -ri "$KEYWORD" "$BASE/skill_01_世界观核心.md" "$BASE/skill_08_术语词典.md" 2>/dev/null | head -30
    echo "--- 雨前精编(权威) ---"
    grep -ri "$KEYWORD" "$BASE/雨前精编/01_世界观与组织.md" 2>/dev/null | head -30
    ;;
  stage)
    echo "=== 搜索战斗关卡 ==="
    grep -ri "$KEYWORD" "$BASE/战斗关卡/" 2>/dev/null | head -40
    echo "--- 关卡深度索引(扩充28~34) ---"
    grep -ri "$KEYWORD" "$BASE/扩充/34_战斗关卡汇总索引.md" "$BASE/扩充/28_"*.md "$BASE/扩充/29_"*.md "$BASE/扩充/30_"*.md "$BASE/扩充/31_"*.md "$BASE/扩充/32_"*.md "$BASE/扩充/33_"*.md 2>/dev/null | head -30
    ;;
  event)
    echo "=== 搜索活动 ==="
    grep -ri "$KEYWORD" "$BASE/轩事/" "$BASE/活动/" 2>/dev/null | head -50
    echo "--- 战斗关卡 ---"
    grep -ri "$KEYWORD" "$BASE/战斗关卡/" 2>/dev/null | head -20
    grep -ri "$KEYWORD" "$BASE/skill_05_支线活动.md" 2>/dev/null | head -30
    ;;
  all)
    echo "=== 全面搜索: $KEYWORD ==="
    grep -ri "$KEYWORD" "$BASE/skill_"*.md 2>/dev/null | head -40
    echo "--- 原始数据 ---"
    grep -ri "$KEYWORD" "$BASE/角色/" "$BASE/角色列表/" 2>/dev/null | head -15
    echo "---"
    grep -ri "$KEYWORD" "$BASE/主线/" "$BASE/支线/" 2>/dev/null | head -15
    echo "---"
    grep -ri "$KEYWORD" "$BASE/世界观设定/" "$BASE/小径/" 2>/dev/null | head -15
    echo "--- 雨前精编(权威) ---"
    grep -ri "$KEYWORD" "$BASE/雨前精编/" 2>/dev/null | head -25
    echo "--- 扩充卷(深度) ---"
    grep -ri "$KEYWORD" "$BASE/扩充/" 2>/dev/null | head -25
    echo "--- 战斗关卡 ---"
    grep -ri "$KEYWORD" "$BASE/战斗关卡/" 2>/dev/null | head -15
    ;;
  related)
    echo "=== 关联搜索: $KEYWORD ==="
    for dir in 角色 角色列表 主线 支线 世界观设定 小径 雨前精编 扩充 战斗关卡; do
      hits=$(grep -rl "$KEYWORD" "$BASE/$dir/" 2>/dev/null | head -3)
      if [ -n "$hits" ]; then
        echo "--- $dir ---"
        echo "$hits"
      fi
    done
    ;;
  *)
    echo "用法: ./query.sh <关键词> [类型]"
    echo "类型: all, character, story, system, world, event, stage, related"
    echo "示例: ./query.sh 维尔汀 character"
    echo "      ./query.sh 暴雨 world"
    exit 1
    ;;
esac

echo "=== 搜索完成 ==="