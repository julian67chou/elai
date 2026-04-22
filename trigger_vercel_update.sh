#!/bin/bash
# 手動觸發 elai1 網站更新

set -e

echo "🚀 手動觸發 elai1 網站更新"
echo "=============================="

# 檢查權杖
if [ -z "$GITHUB_TOKEN" ]; then
    echo "❌ 錯誤: 請設置 GITHUB_TOKEN"
    echo "export GITHUB_TOKEN=\"您的權杖\""
    exit 1
fi

echo "✅ 權杖已設置 (前8位: ${GITHUB_TOKEN:0:8}...)"

# 創建一個小的更新來觸發部署
echo "📝 創建觸發文件..."
TRIGGER_FILE="trigger_update_$(date +%Y%m%d_%H%M%S).txt"
echo "# 觸發 Vercel 部署更新" > "$TRIGGER_FILE"
echo "更新時間: $(date)" >> "$TRIGGER_FILE"
echo "目的: 手動觸發 Vercel 重新部署" >> "$TRIGGER_FILE"
echo "更改: 院長照片文字移除" >> "$TRIGGER_FILE"

echo "✅ 創建觸發文件: $TRIGGER_FILE"

# 添加到 git
git add "$TRIGGER_FILE"
git commit -m "手動觸發 Vercel 部署更新: $(date)"

echo "✅ 觸發文件已提交"

# 推送到 GitHub
echo "🚀 推送到 GitHub..."
if git push origin main; then
    echo "✅ 推送成功"
    echo ""
    echo "📋 下一步操作:"
    echo "1. 等待 1-2 分鐘讓 GitHub Actions 同步"
    echo "2. 等待 2-5 分鐘讓 Vercel 部署"
    echo "3. 強制刷新瀏覽器: Ctrl+Shift+R"
    echo ""
    echo "🔗 監控連結:"
    echo "• elai Actions: https://github.com/julian67chou/elai/actions"
    echo "• elai1 倉庫: https://github.com/julian67chou/elai1"
    echo "• Vercel 控制台: https://vercel.com/julian67chou"
    echo ""
    echo "💡 緩存清除技巧:"
    echo "• 使用無痕模式訪問: https://elai1.vercel.app/"
    echo "• 添加時間戳: https://elai1.vercel.app/?t=$(date +%s)"
    echo "• 清除瀏覽器緩存"
else
    echo "❌ 推送失敗"
    exit 1
fi

echo ""
echo "⏳ 預計時間線:"
echo "0-2分鐘: GitHub Actions 同步"
echo "2-7分鐘: Vercel 部署"
echo "7-30分鐘: CDN 緩存更新"
echo ""
echo "🔄 請稍後檢查網站更新"