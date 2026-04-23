#!/bin/bash
# 網站部署前本地測試腳本
# 用法: ./test_website_locally.sh

set -e  # 遇到錯誤立即停止

echo "🧪 網站部署前本地測試"
echo "===================="

# 檢查必要工具
echo "1. 檢查必要工具..."
command -v python3 >/dev/null 2>&1 || { echo "❌ 需要 python3"; exit 1; }
command -v curl >/dev/null 2>&1 || { echo "❌ 需要 curl"; exit 1; }
echo "   ✅ 必要工具齊全"

# 2. 啟動本地測試伺服器
echo "2. 啟動本地測試伺服器..."
python3 -m http.server 8080 --directory . > /dev/null 2>&1 &
SERVER_PID=$!

# 等待伺服器啟動
sleep 3

# 檢查伺服器是否運行
if ! kill -0 $SERVER_PID 2>/dev/null; then
    echo "❌ 無法啟動本地伺服器"
    exit 1
fi
echo "   ✅ 本地伺服器已啟動 (PID: $SERVER_PID)"

# 3. 測試網站可訪問性
echo "3. 測試網站可訪問性..."
if curl -s -f http://localhost:8080/ > /dev/null; then
    echo "   ✅ 網站可正常訪問"
else
    echo "❌ 網站無法訪問"
    kill $SERVER_PID 2>/dev/null
    exit 1
fi

# 4. 檢查關鍵內容
echo "4. 檢查關鍵內容..."
HTML_CONTENT=$(curl -s http://localhost:8080/)

REQUIRED_KEYWORDS=("伊萊診所" "施奕仲" "預防醫學" "心臟血管" "專業團隊")
KEYWORDS_MISSING=0

for keyword in "${REQUIRED_KEYWORDS[@]}"; do
    if echo "$HTML_CONTENT" | grep -q "$keyword"; then
        echo "   ✅ 包含關鍵字: $keyword"
    else
        echo "   ⚠️  缺少關鍵字: $keyword"
        KEYWORDS_MISSING=$((KEYWORDS_MISSING + 1))
    fi
done

# 5. 檢查圖片資源
echo "5. 檢查圖片資源載入..."
IMG_TAGS=$(echo "$HTML_CONTENT" | grep -o '<img[^>]*src="[^"]*"' | sed 's/.*src="//' | sed 's/"//')
IMG_COUNT=$(echo "$IMG_TAGS" | wc -w)

echo "   📊 頁面圖片數量: $IMG_COUNT"

IMG_ERRORS=0
if [ $IMG_COUNT -gt 0 ]; then
    for img in $IMG_TAGS; do
        if curl -s -f "http://localhost:8080/$img" > /dev/null; then
            echo "   ✅ 圖片可訪問: $img"
        else
            echo "   ❌ 圖片無法訪問: $img"
            IMG_ERRORS=$((IMG_ERRORS + 1))
        fi
    done
else
    echo "   ℹ️  頁面中未找到圖片"
fi

# 6. 檢查連結
echo "6. 檢查內部連結..."
INTERNAL_LINKS=$(echo "$HTML_CONTENT" | grep -o 'href="[^"]*"' | sed 's/href="//' | sed 's/"//' | grep -v 'http' | grep -v 'mailto:' | grep -v 'tel:' | grep -v '^#' | grep -v '^$')

LINK_ERRORS=0
if [ -n "$INTERNAL_LINKS" ]; then
    for link in $INTERNAL_LINKS; do
        # 處理相對路徑
        if [[ $link == /* ]]; then
            TEST_LINK="http://localhost:8080$link"
        else
            TEST_LINK="http://localhost:8080/$link"
        fi
        
        if curl -s -f "$TEST_LINK" > /dev/null; then
            echo "   ✅ 連結可訪問: $link"
        else
            echo "   ❌ 連結無法訪問: $link"
            LINK_ERRORS=$((LINK_ERRORS + 1))
        fi
    done
else
    echo "   ℹ️  未找到內部連結"
fi

# 7. 檢查表單
echo "7. 檢查表單元素..."
FORM_COUNT=$(echo "$HTML_CONTENT" | grep -c '<form')
echo "   📊 表單數量: $FORM_COUNT"

if [ $FORM_COUNT -gt 0 ]; then
    # 檢查表單是否有必要的屬性
    FORMS=$(echo "$HTML_CONTENT" | grep -o '<form[^>]*>')
    FORM_NUM=1
    for form in $FORMS; do
        echo "   📝 表單 $FORM_NUM: $form"
        FORM_NUM=$((FORM_NUM + 1))
    done
fi

# 8. 檢查 meta 標籤
echo "8. 檢查 SEO 相關標籤..."
TITLE_COUNT=$(echo "$HTML_CONTENT" | grep -c '<title')
META_DESC=$(echo "$HTML_CONTENT" | grep -i 'meta.*description' | head -1)
META_VIEWPORT=$(echo "$HTML_CONTENT" | grep -i 'meta.*viewport' | head -1)

if [ $TITLE_COUNT -gt 0 ]; then
    echo "   ✅ 有 title 標籤"
else
    echo "   ⚠️  缺少 title 標籤"
fi

if [ -n "$META_DESC" ]; then
    echo "   ✅ 有 meta description"
else
    echo "   ⚠️  缺少 meta description"
fi

if [ -n "$META_VIEWPORT" ]; then
    echo "   ✅ 有 viewport 設定"
else
    echo "   ⚠️  缺少 viewport 設定"
fi

# 9. 停止測試伺服器
echo "9. 停止測試伺服器..."
kill $SERVER_PID 2>/dev/null
wait $SERVER_PID 2>/dev/null
echo "   ✅ 測試伺服器已停止"

# 10. 測試結果總結
echo ""
echo "📊 測試結果摘要:"
echo "   關鍵字檢查: $KEYWORDS_MISSING 個缺失"
echo "   圖片錯誤: $IMG_ERRORS 個"
echo "   連結錯誤: $LINK_ERRORS 個"
echo "   表單數量: $FORM_COUNT 個"

TOTAL_ERRORS=$((KEYWORDS_MISSING + IMG_ERRORS + LINK_ERRORS))

if [ $TOTAL_ERRORS -eq 0 ]; then
    echo ""
    echo "✅ 所有測試通過，網站狀態良好"
    exit 0
else
    echo ""
    echo "❌ 發現 $TOTAL_ERRORS 個問題需要修復"
    echo ""
    echo "🔧 建議操作:"
    if [ $KEYWORDS_MISSING -gt 0 ]; then
        echo "1. 檢查缺少的關鍵字是否必要"
    fi
    if [ $IMG_ERRORS -gt 0 ]; then
        echo "2. 修復無法訪問的圖片路徑"
    fi
    if [ $LINK_ERRORS -gt 0 ]; then
        echo "3. 修復無法訪問的連結"
    fi
    exit 1
fi