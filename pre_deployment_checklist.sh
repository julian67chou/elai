#!/bin/bash
# 部署前強制檢查清單
# 用法: ./pre_deployment_checklist.sh

echo "📋 部署前強制檢查清單"
echo "====================="

CHECKS_PASSED=0
CHECKS_TOTAL=10
ERRORS=()

# 檢查 1: Git 狀態
echo "1. Git 狀態檢查..."
GIT_STATUS=$(git status --porcelain)
if [ -z "$GIT_STATUS" ]; then
    echo "   ✅ 工作區乾淨"
    CHECKS_PASSED=$((CHECKS_PASSED + 1))
else
    echo "   ⚠️  有未提交的更改:"
    echo "$GIT_STATUS" | sed 's/^/      /'
    ERRORS+=("有未提交的Git更改")
fi

# 檢查 2: 資源完整性
echo "2. 資源完整性檢查..."
if [ -f "check_website_resources.sh" ]; then
    if ./check_website_resources.sh > /dev/null 2>&1; then
        echo "   ✅ 資源完整"
        CHECKS_PASSED=$((CHECKS_PASSED + 1))
    else
        echo "   ❌ 資源缺失 (運行 ./check_website_resources.sh 查看詳情)"
        ERRORS+=("資源檔案缺失")
    fi
else
    echo "   ⚠️  缺少檢查腳本 check_website_resources.sh"
    ERRORS+=("缺少資源檢查腳本")
fi

# 檢查 3: 本地測試
echo "3. 本地功能測試..."
if [ -f "test_website_locally.sh" ]; then
    if ./test_website_locally.sh > /dev/null 2>&1; then
        echo "   ✅ 本地測試通過"
        CHECKS_PASSED=$((CHECKS_PASSED + 1))
    else
        echo "   ❌ 本地測試失敗 (運行 ./test_website_locally.sh 查看詳情)"
        ERRORS+=("本地測試失敗")
    fi
else
    echo "   ⚠️  缺少測試腳本 test_website_locally.sh"
    ERRORS+=("缺少本地測試腳本")
fi

# 檢查 4: 圖片檔案大小
echo "4. 圖片檔案大小檢查..."
if [ -d "assets" ]; then
    LARGE_IMAGES=$(find assets -name "*.jpg" -o -name "*.jpeg" -o -name "*.png" -size +800k 2>/dev/null)
    LARGE_COUNT=$(echo "$LARGE_IMAGES" | grep -v '^$' | wc -l)
    
    if [ $LARGE_COUNT -eq 0 ]; then
        echo "   ✅ 無過大圖片檔案 (>800KB)"
        CHECKS_PASSED=$((CHECKS_PASSED + 1))
    else
        echo "   ⚠️  發現 $LARGE_COUNT 個大檔案 (>800KB):"
        for img in $LARGE_IMAGES; do
            SIZE=$(du -h "$img" 2>/dev/null | cut -f1)
            echo "      - $img ($SIZE)"
        done
        ERRORS+=("發現過大圖片檔案")
    fi
else
    echo "   ⚠️  assets 目錄不存在"
    ERRORS+=("缺少assets目錄")
fi

# 檢查 5: HTML 語法
echo "5. HTML 語法檢查..."
if command -v python3 >/dev/null 2>&1 && python3 -c "import html5validator" 2>/dev/null; then
    if python3 -m html5validator index.html --ignore "section" 2>/dev/null; then
        echo "   ✅ HTML 語法正確"
        CHECKS_PASSED=$((CHECKS_PASSED + 1))
    else
        echo "   ❌ HTML 語法錯誤 (運行: python3 -m html5validator index.html)"
        ERRORS+=("HTML語法錯誤")
    fi
else
    echo "   ℹ️  跳過 HTML 語法檢查 (需要安裝 html5validator)"
    CHECKS_PASSED=$((CHECKS_PASSED + 1))  # 跳過不算失敗
fi

# 檢查 6: 外部連結數量
echo "6. 外部連結檢查..."
EXTERNAL_LINKS=$(grep -o 'href="http[^"]*"' index.html 2>/dev/null | wc -l)
echo "   📊 外部連結數量: $EXTERNAL_LINKS"
if [ $EXTERNAL_LINKS -le 10 ]; then
    echo "   ✅ 外部連結數量合理"
    CHECKS_PASSED=$((CHECKS_PASSED + 1))
else
    echo "   ⚠️  外部連結較多，可能影響載入速度"
    ERRORS+=("外部連結過多")
fi

# 檢查 7: 響應式設計
echo "7. 響應式設計檢查..."
if [ -f "css/style.css" ]; then
    MEDIA_QUERIES=$(grep -c "@media" css/style.css 2>/dev/null || echo 0)
    VIEWPORT=$(grep -i "viewport" index.html 2>/dev/null | wc -l)
    
    echo "   📊 CSS 媒體查詢數量: $MEDIA_QUERIES"
    echo "   📊 Viewport meta 標籤: $VIEWPORT"
    
    if [ $MEDIA_QUERIES -gt 0 ] && [ $VIEWPORT -gt 0 ]; then
        echo "   ✅ 響應式設計完整"
        CHECKS_PASSED=$((CHECKS_PASSED + 1))
    else
        if [ $MEDIA_QUERIES -eq 0 ]; then
            echo "   ⚠️  缺少媒體查詢"
            ERRORS+=("缺少響應式媒體查詢")
        fi
        if [ $VIEWPORT -eq 0 ]; then
            echo "   ⚠️  缺少 viewport meta 標籤"
            ERRORS+=("缺少viewport標籤")
        fi
    fi
else
    echo "   ❌ 缺少 CSS 檔案"
    ERRORS+=("缺少CSS檔案")
fi

# 檢查 8: 備份狀態
echo "8. 備份狀態檢查..."
BACKUP_FILES=$(find . -name "*.backup*" -o -name "*backup*" -o -name "*.old" -o -name "*.bak" 2>/dev/null | grep -v node_modules | grep -v .git)
BACKUP_COUNT=$(echo "$BACKUP_FILES" | grep -v '^$' | wc -l)

echo "   📊 備份檔案數量: $BACKUP_COUNT"
if [ $BACKUP_COUNT -gt 0 ]; then
    echo "   ✅ 有備份檔案"
    # 列出最近的備份
    RECENT_BACKUPS=$(echo "$BACKUP_FILES" | head -5)
    echo "   最近的備份:"
    echo "$RECENT_BACKUPS" | sed 's/^/      - /'
else
    echo "   ⚠️  沒有找到備份檔案"
    ERRORS+=("沒有備份檔案")
fi
CHECKS_PASSED=$((CHECKS_PASSED + 1))  # 備份檢查不是強制失敗

# 檢查 9: 檔案權限
echo "9. 檔案權限檢查..."
WRITABLE_FILES=$(find . -name "*.sh" ! -executable 2>/dev/null | head -5)
if [ -z "$WRITABLE_FILES" ]; then
    echo "   ✅ 腳本檔案權限正確"
    CHECKS_PASSED=$((CHECKS_PASSED + 1))
else
    echo "   ⚠️  以下腳本檔案需要執行權限:"
    echo "$WRITABLE_FILES" | sed 's/^/      - /'
    echo "   執行: chmod +x 檔案名稱"
    ERRORS+=("腳本檔案權限問題")
fi

# 檢查 10: Git 遠端設定
echo "10. Git 遠端設定檢查..."
REMOTE_URL=$(git remote get-url origin 2>/dev/null)
if [ -n "$REMOTE_URL" ]; then
    echo "   ✅ Git 遠端設定正常: $REMOTE_URL"
    CHECKS_PASSED=$((CHECKS_PASSED + 1))
else
    echo "   ❌ 沒有設定 Git 遠端"
    ERRORS+=("沒有Git遠端設定")
fi

# 總結
echo ""
echo "📊 檢查結果: $CHECKS_PASSED/$CHECKS_TOTAL 通過"

if [ ${#ERRORS[@]} -eq 0 ]; then
    echo ""
    echo "✅ 所有檢查通過，可以部署"
    echo ""
    echo "🚀 建議部署命令:"
    echo "   ./deploy_elai_clinic.sh \"你的修改描述\""
    exit 0
else
    echo ""
    echo "❌ 發現 ${#ERRORS[@]} 個問題:"
    for error in "${ERRORS[@]}"; do
        echo "   - $error"
    done
    echo ""
    echo "🔧 請修復以上問題後再進行部署"
    exit 1
fi