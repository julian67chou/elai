#!/bin/bash
# 網站快速回滾腳本
# 用法: ./rollback_website.sh [commit-hash]

echo "🔄 執行網站快速回滾"
echo "==================="

# 檢查是否在 Git 倉庫中
if ! git status > /dev/null 2>&1; then
    echo "❌ 當前目錄不是 Git 倉庫"
    exit 1
fi

# 獲取當前分支
CURRENT_BRANCH=$(git branch --show-current)
echo "當前分支: $CURRENT_BRANCH"

# 顯示最近提交
echo ""
echo "最近提交記錄:"
git log --oneline -10

# 獲取目標提交
TARGET_COMMIT="$1"
if [ -z "$TARGET_COMMIT" ]; then
    echo ""
    read -p "請輸入要回滾到的 commit hash (或輸入 'HEAD~1' 回滾上個版本): " TARGET_COMMIT
fi

if [ -z "$TARGET_COMMIT" ]; then
    echo "❌ 未指定回滾目標"
    exit 1
fi

# 驗證目標提交是否存在
if ! git rev-parse --verify "$TARGET_COMMIT" > /dev/null 2>&1; then
    echo "❌ 提交 '$TARGET_COMMIT' 不存在"
    exit 1
fi

# 顯示目標提交資訊
echo ""
echo "目標提交資訊:"
git log --oneline -1 "$TARGET_COMMIT"

# 顯示將被丟棄的更改
echo ""
echo "將被丟棄的更改 (從 $TARGET_COMMIT 到 HEAD):"
git log --oneline "$TARGET_COMMIT"..HEAD

# 確認操作
echo ""
read -p "確定要回滾到 $TARGET_COMMIT 嗎？這將丟棄之後的所有更改。(y/N): " CONFIRM
if [ "$CONFIRM" != "y" ] && [ "$CONFIRM" != "Y" ]; then
    echo "❌ 取消回滾"
    exit 0
fi

# 創建回滾備份
echo ""
echo "創建回滾備份..."
ROLLBACK_BACKUP_DIR="rollback_backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$ROLLBACK_BACKUP_DIR"

# 備份當前狀態
cp index.html "$ROLLBACK_BACKUP_DIR/" 2>/dev/null || true
cp css/style.css "$ROLLBACK_BACKUP_DIR/" 2>/dev/null || true

# 執行回滾
echo "執行回滾到 $TARGET_COMMIT..."
if git reset --hard "$TARGET_COMMIT"; then
    echo "✅ 本地回滾完成"
else
    echo "❌ 回滾失敗"
    exit 1
fi

# 強制推送到遠端
echo ""
echo "強制推送到 GitHub..."
read -p "確定要強制推送到遠端嗎？這將覆蓋遠端歷史。(y/N): " PUSH_CONFIRM

if [ "$PUSH_CONFIRM" = "y" ] || [ "$PUSH_CONFIRM" = "Y" ]; then
    if git push origin "$CURRENT_BRANCH" --force; then
        echo "✅ 已強制推送到 GitHub"
    else
        echo "❌ 推送失敗"
        echo "本地已回滾，但遠端未更新"
        echo "手動推送命令: git push origin $CURRENT_BRANCH --force"
    fi
else
    echo "⚠️  跳過遠端推送，僅本地回滾"
    echo "遠端倉庫保持原狀，本地已回滾到 $TARGET_COMMIT"
fi

# 創建回滾報告
echo ""
echo "創建回滾報告..."
ROLLBACK_REPORT="ROLLBACK_REPORT_$(date +%Y%m%d_%H%M%S).md"

cat > "$ROLLBACK_REPORT" << EOF
# 網站回滾報告

## 回滾資訊
- **回滾時間**: $(date)
- **目標版本**: $TARGET_COMMIT
- **目標版本訊息**: $(git log --format="%s" -1 "$TARGET_COMMIT")
- **當前分支**: $CURRENT_BRANCH
- **執行者**: $(whoami)
- **備份目錄**: $ROLLBACK_BACKUP_DIR

## 回滾原因
[請填寫回滾原因]

## 被丟棄的更改
以下提交已被回滾丟棄：

\`\`\`
$(git log --oneline "$TARGET_COMMIT"..HEAD@{1})
\`\`\`

## 受影響的檔案
\`\`\`
$(git diff --name-only "$TARGET_COMMIT" HEAD@{1} 2>/dev/null || echo "無法獲取差異")
\`\`\`

## 回滾操作
1. ✅ 創建本地備份: $ROLLBACK_BACKUP_DIR
2. ✅ 執行本地回滾: git reset --hard $TARGET_COMMIT
3. $(if [ "$PUSH_CONFIRM" = "y" ] || [ "$PUSH_CONFIRM" = "Y" ]; then echo "✅ 強制推送到遠端"; else echo "⚠️  僅本地回滾，未推送遠端"; fi)

## 網站狀態
- **本地狀態**: 已回滾到 $TARGET_COMMIT
- **遠端狀態**: $(if [ "$PUSH_CONFIRM" = "y" ] || [ "$PUSH_CONFIRM" = "Y" ]; then echo "已同步回滾"; else echo "保持原狀"; fi)
- **Vercel 部署**: $(if [ "$PUSH_CONFIRM" = "y" ] || [ "$PUSH_CONFIRM" = "Y" ]; then echo "將自動觸發重新部署"; else echo "不會觸發部署"; fi)

## 重要連結
- 網站: https://elai1.vercel.app/
- GitHub: https://github.com/julian67chou/elai
- 目標版本: https://github.com/julian67chou/elai/commit/$TARGET_COMMIT
- 回滾前版本: $(git rev-parse --short HEAD@{1} 2>/dev/null || echo "未知")

## 後續行動
### 如果回滾正確
1. 等待 Vercel 重新部署（如果已推送）
2. 驗證網站功能正常
3. 分析導致回滾的問題原因
4. 制定預防措施

### 如果回滾錯誤
從備份恢復：
\`\`\`bash
# 恢復 index.html
cp $ROLLBACK_BACKUP_DIR/index.html .

# 恢復 CSS
cp $ROLLBACK_BACKUP_DIR/style.css css/

# 提交恢復
git add -A
git commit -m "恢復回滾前的狀態"
git push origin $CURRENT_BRANCH
\`\`\`

## 問題分析與預防
### 導致回滾的問題
[描述導致需要回滾的問題]

### 根本原因
[分析問題的根本原因]

### 預防措施
1. [具體預防措施1]
2. [具體預防措施2]
3. [具體預防措施3]

## 聯絡資訊
- **技術負責人**: [請填寫]
- **問題回報**: [請填寫]
- **緊急聯絡**: [請填寫]
EOF

echo "✅ 回滾報告已創建: $ROLLBACK_REPORT"

# 創建驗證腳本
echo ""
echo "創建回滾驗證腳本..."
cat > verify_rollback.sh << EOF
#!/bin/bash
# 回滾驗證腳本

echo "🔍 驗證網站回滾狀態"
echo "===================="

SITE_URL="https://elai1.vercel.app/"

echo "1. 檢查網站可訪問性..."
if curl -s -f "\$SITE_URL" > /dev/null; then
    echo "   ✅ 網站可正常訪問"
else
    echo "   ❌ 網站無法訪問"
    exit 1
fi

echo "2. 檢查版本內容..."
EXPECTED_COMMIT="$TARGET_COMMIT"
EXPECTED_MSG="$(git log --format="%s" -1 "$TARGET_COMMIT")"

echo "   目標版本: \$EXPECTED_COMMIT"
echo "   版本訊息: \$EXPECTED_MSG"

echo ""
echo "📋 驗證步驟:"
echo "1. 訪問網站: \$SITE_URL"
echo "2. 檢查回滾的修改是否已恢復"
echo "3. 確認網站功能正常"
echo "4. 如有問題，參考回滾報告: $ROLLBACK_REPORT"

echo ""
echo "⚠️  注意: 如果未強制推送，遠端網站可能還是舊版本"
if [ "$PUSH_CONFIRM" != "y" ] && [ "$PUSH_CONFIRM" != "Y" ]; then
    echo "   本次僅本地回滾，遠端未更新"
    echo "   需要手動推送: git push origin $CURRENT_BRANCH --force"
fi
EOF

chmod +x verify_rollback.sh

echo "✅ 驗證腳本已創建: verify_rollback.sh"

# 總結
echo ""
echo "🎉 回滾流程完成！"
echo ""
echo "📋 產生的檔案:"
echo "   - 回滾備份: $ROLLBACK_BACKUP_DIR"
echo "   - 回滾報告: $ROLLBACK_REPORT"
echo "   - 驗證腳本: verify_rollback.sh"
echo ""
echo "🔧 下一步操作:"
echo "1. 運行驗證腳本: ./verify_rollback.sh"
echo "2. 檢查回滾報告: $ROLLBACK_REPORT"
echo "3. 分析問題原因，制定預防措施"
echo "4. 如果需要，從備份恢復錯誤的回滾"
echo ""
echo "📞 如有問題，請參考回滾報告中的聯絡資訊"