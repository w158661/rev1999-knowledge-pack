#!/bin/bash
# 重返未来1999 数据查询脚本
# 用法: ./query.sh <关键词> [文件类型]
# 文件类型: all(默认), character, story, system, world, event

KEYWORD="$1"
TYPE="${2:-all}"

# 数据路径: 优先使用 REV1999_DATA 环境变量
# 安装时设置: export REV1999_DATA=/path/to/rev1999-pack/data
if [ -n "$REV1999_DATA" ]; then
  BASE="$REV1999_DATA"
else
  SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
  BASE="$(cd "$SCRIPT_DIR/../.." && pwd)/data"
fi

if [ ! -d "$BASE" ]; then
  echo "错误: 数据目录不存在 ($BASE)"
  echo "请设置 REV1999_DATA 环境变量指向数据目录"
  echo "export REV1999_DATA=/path/to/rev1999-pack/data"
  exit 1
fi

case "$TYPE" in
  character)
    echo "=== 搜索角色资料 ==="
    grep -ri "$KEYWORD" "$BASE/角色/" "$BASE/角色列表/" 2>/dev/null | head -50
    grep -ri "$KEYWORD" "$BASE/skill_03_角色百科A.md" "$BASE/skill_04_角色百科B.md" 2>/dev/null | head -30
    ;;
  story)
    echo "=== 搜索剧情 ==="
    grep -ri "$KEYWORD" "$BASE/主线/" "$BASE/支线/" 2>/dev/null | head -50
    grep -ri "$KEYWORD" "$BASE/skill_02_时间线与主线.md" "$BASE/skill_05_支线活动.md" 2>/dev/null | head -30
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
    ;;
  event)
    echo "=== 搜索活动 ==="
    grep -ri "$KEYWORD" "$BASE/轩事/" "$BASE/活动/" 2>/dev/null | head -50
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
    ;;
  *)
    echo "用法: ./query.sh <关键词> [类型]"
    echo "类型: all, character, story, system, world, event"
    echo "示例: ./query.sh 维尔汀 character"
    echo "      ./query.sh 暴雨 world"
    exit 1
    ;;
esac

echo "=== 搜索完成 ==="