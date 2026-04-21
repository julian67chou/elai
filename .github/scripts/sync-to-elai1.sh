#!/bin/bash
# GitHub Actions 使用的同步腳本

set -e

echo "🔄 開始同步 elai 到 elai1..."

# 配置 Git
git config --global user.name "GitHub Actions"
git config --global user.email "actions@github.com"

# 添加 elai1 遠端
ELAI1_TOKEN="$1"
if [ -z "$ELAI1_TOKEN" ]; then
    echo "❌ 錯誤: 未提供權杖"
    exit 1
fi

git remote add elai1 "https://x-access-token:${ELAI1_TOKEN}@github.com/julian67chou/elai1.git" || true

# 檢查當前分支
CURRENT_BRANCH=$(git branch --show-current)
echo "當前分支: $CURRENT_BRANCH"

# 推送到 elai1
echo "🚀 推送到 elai1..."
if git push elai1 "${CURRENT_BRANCH}:main" --force; then
    echo "✅ 同步成功！"
    
    # 記錄同步信息
    cat > sync-info.json << EOF
{
  "source": "${{ github.repository }}",
  "target": "julian67chou/elai1",
  "commit": "${{ github.sha }}",
  "branch": "${CURRENT_BRANCH}",
  "timestamp": "$(date -Iseconds)",
  "status": "success"
}
EOF
    
    exit 0
else
    echo "❌ 同步失敗"
    exit 1
fi