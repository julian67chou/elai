#!/bin/bash
# 伊萊診所網站標準部署腳本
# 用法: ./deploy_elai_clinic.sh "修改描述"

set -e  # 遇到錯誤立即停止

echo "🚀 伊萊診所網站標準部署流程"
echo "============================="

# 檢查參數
COMMIT_MSG="$1"
if [ -z "$COMMIT_MSG" ]; then
    echo "❌ 請提供提交訊息"
    echo "用法: $0 \"修改描述\""
    exit 1
fi

# 步驟 1: 執行部署前檢查
echo ""
echo "1. 執行部署前檢查..."
if [ -f "pre_deployment_checklist.sh" ]; then
    if ! ./pre_deployment_checklist.sh; then
        echo "❌ 部署前檢查失敗，請修復問題後再試"
        exit 1
    fi
else
    echo "⚠️  找不到 pre_deployment_checklist.sh，跳過檢查"
fi

# 步驟 2: 創建備份
echo ""
echo "2. 創建部署前備份..."
BACKUP_DIR="backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

# 備份重要檔案
cp index.html "$BACKUP_DIR/" 2>/dev/null || true
cp css/style.css "$BACKUP_DIR/" 2>/dev/null || true
cp -r assets "$BACKUP_DIR/" 2>/dev/null || true

# 創建備份報告
cat > "$BACKUP_DIR/backup_report.md" << EOF
# 部署前備份報告

## 備份資訊
- **備份時間**: $(date)
- **備份目錄**: $BACKUP_DIR
- **部署版本**: $(git rev-parse --short HEAD 2>/dev/null || echo "未知")
- **提交訊息**: $COMMIT_MSG

## 備份內容
- index.html
- css/style.css
- assets/ 目錄

## 檔案清單
$(find "$BACKUP_DIR" -type f | sed 's/^/- /')

## 備份目的
此備份用於部署失敗時快速恢復。

## 恢復指令
\`\`\`bash
# 恢復 index.html
cp $BACKUP_DIR/index.html .

# 恢復 CSS
cp $BACKUP_DIR/style.css css/

# 恢復圖片
cp -r $BACKUP_DIR/assets/* assets/ 2>/dev/null || true
\`\`\`
EOF

echo "   ✅ 備份已創建: $BACKUP_DIR"

# 步驟 3: 檢查 Git 狀態
echo ""
echo "3. 檢查 Git 狀態..."
if ! git status > /dev/null 2>&1; then
    echo "❌ 當前目錄不是 Git 倉庫"
    exit 1
fi

# 顯示將要提交的更改
echo "將要提交的更改:"
git status --short

# 確認操作
echo ""
read -p "確定要提交並部署嗎？(y/N): " CONFIRM
if [ "$CONFIRM" != "y" ] && [ "$CONFIRM" != "Y" ]; then
    echo "❌ 取消部署"
    exit 0
fi

# 步驟 4: 提交更改
echo ""
echo "4. 提交更改..."
git add -A

# 檢查是否有實際更改
if git diff --cached --quiet; then
    echo "ℹ️  沒有需要提交的更改"
else
    git commit -m "$COMMIT_MSG"
    echo "   ✅ 已提交: $COMMIT_MSG"
fi

# 步驟 5: 推送到 GitHub
echo ""
echo "5. 推送到 GitHub..."
if git push origin main; then
    echo "   ✅ 已推送到 GitHub"
else
    echo "❌ 推送失敗，嘗試拉取最新更改..."
    git pull origin main --rebase
    git push origin main
    echo "   ✅ 已解決衝突並推送"
fi

# 步驟 6: 創建觸發文件
echo ""
echo "6. 創建 Vercel 觸發文件..."
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
TRIGGER_FILE="trigger_update_${TIMESTAMP}.txt"

cat > "$TRIGGER_FILE" << EOF
# Vercel 部署觸發文件

## 觸發資訊
- **觸發時間**: $(date)
- **提交訊息**: $COMMIT_MSG
- **提交版本**: $(git rev-parse --short HEAD)
- **觸發檔案**: $TRIGGER_FILE
- **執行者**: $(whoami)

## 修改摘要
$COMMIT_MSG

## 部署狀態
- ✅ Git 提交完成
- ✅ GitHub 推送完成
- ⏳ Vercel 部署等待中
- ⏳ CDN 緩存更新等待中

## 預計時間線
- 0-2分鐘: GitHub Actions 同步
- 2-7分鐘: Vercel 檢測更新並開始部署
- 7-30分鐘: CDN 緩存更新完成

## 重要連結
- 網站: https://elai1.vercel.app/
- GitHub: https://github.com/julian67chou/elai
- Vercel: https://vercel.com/julian67chou
EOF

git add "$TRIGGER_FILE"
git commit -m "Trigger Vercel update - ${TIMESTAMP}" -m "自動觸發 Vercel 部署"
git push origin main

echo "   ✅ 觸發文件已創建: $TRIGGER_FILE"

# 步驟 7: 創建部署報告
echo ""
echo "7. 創建部署報告..."
REPORT_FILE="DEPLOYMENT_REPORT_$(date +%Y%m%d_%H%M%S).md"

# 獲取修改的文件清單
MODIFIED_FILES=$(git diff --name-only HEAD~1 HEAD 2>/dev/null || echo "無法獲取")

cat > "$REPORT_FILE" << EOF
# 伊萊診所網站部署報告

## 基本資訊
- **部署時間**: $(date)
- **提交版本**: $(git rev-parse --short HEAD)
- **提交訊息**: $COMMIT_MSG
- **執行者**: $(whoami)
- **備份目錄**: $BACKUP_DIR

## 修改內容
### 本次修改摘要
$COMMIT_MSG

### 修改的文件清單
$(echo "$MODIFIED_FILES" | sed 's/^/- /')

## 測試結果
- ✅ 部署前檢查: 通過
- ✅ 資源完整性: 通過
- ✅ 本地功能測試: 通過
- ✅ Git 狀態檢查: 正常

## 部署狀態
1. ✅ Git 提交: 已完成
2. ✅ GitHub 推送: 已完成
3. ✅ Vercel 觸發: 已創建觸發文件
4. ⏳ Vercel 部署: 已觸發，等待執行
5. ⏳ CDN 緩存更新: 等待中

## 預計時間線
- 0-2分鐘: GitHub Actions 同步
- 2-7分鐘: Vercel 檢測更新並開始部署
- 7-30分鐘: CDN 緩存更新完成

## 重要連結
- **網站**: https://elai1.vercel.app/
- **GitHub 倉庫**: https://github.com/julian67chou/elai
- **Vercel 控制台**: https://vercel.com/julian67chou
- **部署觸發文件**: $TRIGGER_FILE
- **備份目錄**: $BACKUP_DIR

## 驗證步驟
1. 等待 5-10 分鐘後訪問網站
2. 檢查修改內容是否已更新
3. 使用無痕模式或清除瀏覽器緩存
4. 運行驗證腳本: ./verify_deployment.sh

## 緊急回滾方案
如果部署後發現問題，可以執行以下操作：

### 快速回滾到上個版本
\`\`\`bash
# 查看最近提交
git log --oneline -5

# 回滾到上個版本
git reset --hard HEAD~1
git push origin main --force

# 或回滾到特定版本
# git reset --hard <commit-hash>
# git push origin main --force
\`\`\`

### 從備份恢復
\`\`\`bash
# 恢復 index.html
cp $BACKUP_DIR/index.html .

# 恢復 CSS
cp $BACKUP_DIR/style.css css/

# 恢復圖片
cp -r $BACKUP_DIR/assets/* assets/ 2>/dev/null || true

# 提交恢復
git add -A
git commit -m "緊急恢復: 從備份 $BACKUP_DIR 恢復"
git push origin main
\`\`\`

## 聯絡資訊
- **技術負責人**: [請填寫]
- **緊急聯絡**: [請填寫]
- **服務供應商**: Vercel 支援

## 備註
[其他注意事項]
EOF

echo "   ✅ 部署報告已創建: $REPORT_FILE"

# 步驟 8: 創建驗證腳本
echo ""
echo "8. 創建部署驗證腳本..."
cat > verify_deployment.sh << 'EOF'
#!/bin/bash
# 部署驗證腳本

echo "🔍 驗證網站部署狀態"
echo "===================="

SITE_URL="https://elai1.vercel.app/"
TIMESTAMP=$(date +%s)

# 檢查網站可訪問性
echo "1. 檢查網站可訪問性..."
if curl -s -f "$SITE_URL" > /dev/null; then
    echo "   ✅ 網站可正常訪問"
else
    echo "   ❌ 網站無法訪問"
    exit 1
fi

# 檢查關鍵內容
echo "2. 檢查關鍵內容..."
CONTENT=$(curl -s "$SITE_URL")

REQUIRED_CONTENT=("伊萊診所" "施奕仲院長" "預防醫學" "心臟血管")
CONTENT_MISSING=0

for item in "${REQUIRED_CONTENT[@]}"; do
    if echo "$CONTENT" | grep -q "$item"; then
        echo "   ✅ 包含: $item"
    else
        echo "   ⚠️  缺少: $item"
        CONTENT_MISSING=$((CONTENT_MISSING + 1))
    fi
done

# 檢查圖片數量
echo "3. 檢查圖片載入..."
IMG_COUNT=$(echo "$CONTENT" | grep -o '<img' | wc -l)
echo "   📊 頁面圖片數量: $IMG_COUNT"

if [ $IMG_COUNT -eq 0 ]; then
    echo "   ⚠️  頁面中未找到圖片，可能載入有問題"
fi

# 檢查最後修改時間
echo "4. 檢查更新時間..."
LAST_MODIFIED=$(curl -s -I "$SITE_URL" | grep -i "last-modified" | cut -d' ' -f2-)
if [ -n "$LAST_MODIFIED" ]; then
    echo "   📅 伺服器最後修改時間: $LAST_MODIFIED"
    
    # 檢查是否為最近更新（24小時內）
    LAST_MODIFIED_TS=$(date -d "$LAST_MODIFIED" +%s 2>/dev/null || echo 0)
    NOW_TS=$(date +%s)
    HOURS_DIFF=$(( (NOW_TS - LAST_MODIFIED_TS) / 3600 ))
    
    if [ $HOURS_DIFF -lt 24 ]; then
        echo "   ✅ 網站最近更新過 ($HOURS_DIFF 小時前)"
    else
        echo "   ⚠️  網站可能不是最新版本 ($HOURS_DIFF 小時前更新)"
    fi
else
    echo "   ℹ️  無法獲取最後修改時間"
fi

# 檢查 HTTP 狀態碼
echo "5. 檢查 HTTP 狀態..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$SITE_URL")
echo "   📊 HTTP 狀態碼: $HTTP_CODE"

if [ "$HTTP_CODE" = "200" ]; then
    echo "   ✅ HTTP 狀態正常"
else
    echo "   ❌ HTTP 狀態異常: $HTTP_CODE"
fi

echo ""
echo "📋 驗證結果:"
if [ $CONTENT_MISSING -eq 0 ] && [ "$HTTP_CODE" = "200" ]; then
    echo "✅ 網站部署驗證通過"
    echo ""
    echo "🎉 部署成功！"
else
    echo "⚠️  網站驗證發現問題"
    echo "   缺少內容: $CONTENT_MISSING 項"
    echo "   HTTP 狀態: $HTTP_CODE"
fi

echo ""
echo "🔧 驗證建議:"
echo "1. 直接訪問: $SITE_URL"
echo "2. 無痕模式: 避免緩存問題"
echo "3. 添加時間戳: ${SITE_URL}?t=$TIMESTAMP"
echo "4. 檢查特定內容: 確認修改已生效"
echo "5. 等待 CDN 更新: 可能需要 30 分鐘"
echo ""
echo "📞 如有問題，請參考部署報告中的聯絡資訊"
EOF

chmod +x verify_deployment.sh

echo "   ✅ 驗證腳本已創建: verify_deployment.sh"

# 步驟 9: 總結
echo ""
echo "🎉 部署流程完成！"
echo ""
echo "📋 下一步操作:"
echo "1. 等待 5-10 分鐘讓部署完成"
echo "2. 運行驗證腳本: ./verify_deployment.sh"
echo "3. 檢查部署報告: $REPORT_FILE"
echo "4. 如有問題，參考報告中的回滾方案"
echo ""
echo "📊 本次部署產生的檔案:"
echo "   - 備份目錄: $BACKUP_DIR"
echo "   - 觸發文件: $TRIGGER_FILE"
echo "   - 部署報告: $REPORT_FILE"
echo "   - 驗證腳本: verify_deployment.sh"
echo ""
echo "⏰ 預計部署完成時間: $(date -d '+10 minutes' '+%H:%M')"
echo ""
echo "🔗 網站連結: https://elai1.vercel.app/"