#!/bin/bash
# 網站資源完整性檢查腳本（改進版）
# 用法: ./check_website_resources.sh

echo "🔍 網站資源完整性檢查"
echo "========================"

MISSING_COUNT=0
TOTAL_IMAGES=0
EXTERNAL_URLS=0

# 檢查 HTML 中引用的所有圖片
echo "1. 檢查 HTML 中的圖片引用..."
HTML_IMAGES=$(grep -o 'src="[^"]*\.\(jpg\|png\|svg\|gif\|jpeg\)"' index.html | sed 's/src="//' | sed 's/"//')

if [ -n "$HTML_IMAGES" ]; then
    for img in $HTML_IMAGES; do
        TOTAL_IMAGES=$((TOTAL_IMAGES + 1))
        
        # 檢查是否為外部 URL
        if [[ $img == http://* ]] || [[ $img == https://* ]]; then
            echo "   🌐 外部圖片: $img"
            EXTERNAL_URLS=$((EXTERNAL_URLS + 1))
        elif [ ! -f "$img" ]; then
            echo "   ❌ 缺失: $img"
            MISSING_COUNT=$((MISSING_COUNT + 1))
        else
            FILE_SIZE=$(du -h "$img" 2>/dev/null | cut -f1)
            FILE_INFO=$(file "$img" 2>/dev/null | cut -d: -f2- | cut -c1-40)
            echo "   ✅ 存在: $img ($FILE_SIZE, $FILE_INFO)"
        fi
    done
else
    echo "   ℹ️  HTML 中未找到圖片引用"
fi

# 檢查 CSS 中的背景圖片
echo "2. 檢查 CSS 中的圖片引用..."
CSS_IMAGES=$(grep -o 'url("[^"]*\.\(jpg\|png\|svg\|gif\|jpeg\)")' css/style.css 2>/dev/null | sed 's/url("//' | sed 's/")//')

if [ -n "$CSS_IMAGES" ]; then
    for img in $CSS_IMAGES; do
        TOTAL_IMAGES=$((TOTAL_IMAGES + 1))
        
        # 檢查是否為外部 URL
        if [[ $img == http://* ]] || [[ $img == https://* ]] || [[ $img == //* ]]; then
            echo "   🌐 外部圖片: $img"
            EXTERNAL_URLS=$((EXTERNAL_URLS + 1))
        elif [ ! -f "$img" ]; then
            echo "   ❌ 缺失: $img"
            MISSING_COUNT=$((MISSING_COUNT + 1))
        else
            FILE_SIZE=$(du -h "$img" 2>/dev/null | cut -f1)
            echo "   ✅ 存在: $img ($FILE_SIZE)"
        fi
    done
else
    echo "   ℹ️  CSS 中未找到圖片引用"
fi

# 檢查 assets 目錄中的圖片檔案
echo "3. 檢查 assets 目錄中的圖片檔案..."
if [ -d "assets" ]; then
    ASSET_IMAGES=$(find assets -name "*.jpg" -o -name "*.png" -o -name "*.jpeg" -o -name "*.gif" -o -name "*.svg" 2>/dev/null | wc -l)
    echo "   📊 assets 目錄圖片數量: $ASSET_IMAGES"
    
    # 列出大檔案
    LARGE_FILES=$(find assets -name "*.jpg" -size +500k 2>/dev/null)
    if [ -n "$LARGE_FILES" ]; then
        echo "   ⚠️  發現大檔案 (>500KB):"
        for file in $LARGE_FILES; do
            SIZE=$(du -h "$file" | cut -f1)
            echo "      - $file ($SIZE)"
        done
    fi
else
    echo "   ⚠️  assets 目錄不存在"
fi

# 檢查 JavaScript 和 CSS 檔案
echo "4. 檢查 JavaScript 和 CSS 檔案..."
JS_FILES=$(grep -o 'src="[^"]*\.js"' index.html | sed 's/src="//' | sed 's/"//')
CSS_FILES=$(grep -o 'href="[^"]*\.css"' index.html | sed 's/href="//' | sed 's/"//')

for js in $JS_FILES; do
    # 檢查是否為外部 URL
    if [[ $js == http://* ]] || [[ $js == https://* ]]; then
        echo "   🌐 外部 JavaScript: $js"
    elif [ ! -f "$js" ]; then
        echo "   ❌ 缺失 JavaScript: $js"
        MISSING_COUNT=$((MISSING_COUNT + 1))
    else
        echo "   ✅ 存在 JavaScript: $js"
    fi
done

for css in $CSS_FILES; do
    # 檢查是否為外部 URL
    if [[ $css == http://* ]] || [[ $css == https://* ]]; then
        echo "   🌐 外部 CSS: $css"
    elif [ ! -f "$css" ]; then
        echo "   ❌ 缺失 CSS: $css"
        MISSING_COUNT=$((MISSING_COUNT + 1))
    else
        echo "   ✅ 存在 CSS: $css"
    fi
done

# 檢查部落格圖片是否存在（如果HTML中有引用）
echo "5. 檢查部落格圖片..."
BLOG_IMAGES="assets/blog-heart-health.jpg assets/blog-preventive-care.jpg assets/blog-nutrition.jpg"
for blog_img in $BLOG_IMAGES; do
    if grep -q "$blog_img" index.html; then
        if [ ! -f "$blog_img" ]; then
            echo "   ❌ 部落格圖片缺失但被引用: $blog_img"
            MISSING_COUNT=$((MISSING_COUNT + 1))
        else
            echo "   ✅ 部落格圖片存在: $blog_img"
        fi
    else
        echo "   ℹ️  部落格圖片未引用: $blog_img"
    fi
done

# 總結報告
echo ""
echo "📊 檢查結果摘要:"
echo "   總檢查資源數: $TOTAL_IMAGES"
echo "   外部 URL 數: $EXTERNAL_URLS"
echo "   缺失檔案數: $MISSING_COUNT"
echo "   資產目錄圖片數: $ASSET_IMAGES"

# 計算實際缺失的本地檔案（排除外部URL）
LOCAL_MISSING=0
for img in $HTML_IMAGES $CSS_IMAGES; do
    if [[ $img != http://* ]] && [[ $img != https://* ]] && [[ $img != //* ]]; then
        if [ ! -f "$img" ]; then
            LOCAL_MISSING=$((LOCAL_MISSING + 1))
        fi
    fi
done

if [ $LOCAL_MISSING -eq 0 ]; then
    echo ""
    echo "✅ 所有本地資源檔案完整"
    echo "   注意: 有 $EXTERNAL_URLS 個外部資源依賴網路連接"
    exit 0
else
    echo ""
    echo "❌ 發現 $LOCAL_MISSING 個本地檔案缺失"
    echo "   外部 URL: $EXTERNAL_URLS 個"
    echo ""
    echo "🔧 建議操作:"
    echo "1. 檢查缺失檔案的路徑是否正確"
    echo "2. 確認檔案是否已上傳到正確位置"
    echo "3. 更新 HTML/CSS 中的檔案路徑"
    echo "4. 從備份恢復缺失的檔案"
    echo "5. 考慮將外部資源下載到本地以減少依賴"
    exit 1
fi