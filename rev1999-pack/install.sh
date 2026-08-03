#!/bin/bash
# rev1999 知识技能包 安装脚本
# 用法: ./install.sh [目标目录]
# 默认目标: .claude/skills/ (当前项目)

set -e

PACKAGE_DIR="$(cd "$(dirname "$0")" && pwd)"
TARGET_DIR="${1:-$PACKAGE_DIR/../.claude/skills}"
DATA_DIR="$PACKAGE_DIR/data"

echo "=== 安装 rev1999 知识技能包 ==="
echo "包目录: $PACKAGE_DIR"
echo "目标: $TARGET_DIR"
echo "数据: $DATA_DIR"

# 创建目标目录
mkdir -p "$TARGET_DIR"

# 复制技能文件
echo ">>> 安装技能..."
cp -r "$PACKAGE_DIR/skills/"* "$TARGET_DIR/"
echo "    已安装:"
for skill in "$TARGET_DIR"/rev1999*; do
  echo "    - $(basename $skill)"
done

# 设置环境变量
echo ""
echo ">>> 配置数据路径..."
echo "请将以下行添加到 ~/.bashrc 或 ~/.zshrc:"
echo ""
echo "  export REV1999_DATA=\"$DATA_DIR\""
echo ""

# 安装完成
echo "=== 安装完成 ==="
echo ""
echo "使用方式:"
echo "  /rev1999           - 综合知识库"
echo "  /rev1999-roleplay  - 角色扮演"
echo "  /rev1999-oc        - OC创作"
echo "  /rev1999-team      - 队伍搭配"
echo "  /rev1999-story     - 剧情时间线"
echo "  /rev1999-query     - 数据快速查询"
echo ""
echo "数据查询:"
echo "  export REV1999_DATA=\"$DATA_DIR\""
echo "  bash skills/rev1999/scripts/query.sh \"暴雨\" world"
echo ""