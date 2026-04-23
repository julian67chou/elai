#!/bin/bash
# 伊萊診所網站更新驗證腳本

echo "🔍 檢查伊萊診所網站更新狀態"
echo "================================="

# 檢查網站是否可訪問
echo "1. 檢查網站可訪問性..."
if curl -s -f https://elai1.vercel.app/ > /dev/null; then
    echo "   ✅ 網站可正常訪問"
else
    echo "   ❌ 網站無法訪問"
    exit 1
fi

# 獲取網站內容並檢查關鍵字
echo "2. 檢查服務項目順序..."
CONTENT=$(curl -s https://elai1.vercel.app/)

# 檢查新順序的關鍵服務
echo "   檢查新順序服務項目:"
if echo "$CONTENT" | grep -q "分子點滴治療"; then
    echo "   ✅ 分子點滴治療 (位置 1)"
else
    echo "   ❌ 未找到分子點滴治療"
fi

if echo "$CONTENT" | grep -q "EECP體外反搏治療"; then
    echo "   ✅ EECP體外反搏治療 (位置 2)"
else
    echo "   ❌ 未找到EECP體外反搏治療"
fi

if echo "$CONTENT" | grep -q "SIS磁場治療"; then
    echo "   ✅ SIS磁場治療 (位置 3)"
else
    echo "   ❌ 未找到SIS磁場治療"
fi

if echo "$CONTENT" | grep -q "靜脈雷射"; then
    echo "   ✅ 靜脈雷射 (位置 4)"
else
    echo "   ❌ 未找到靜脈雷射"
fi

if echo "$CONTENT" | grep -q "氫氣治療"; then
    echo "   ✅ 氫氣治療 (位置 5)"
else
    echo "   ❌ 未找到氫氣治療"
fi

if echo "$CONTENT" | grep -q "預防醫學諮詢"; then
    echo "   ✅ 預防醫學諮詢 (位置 6)"
else
    echo "   ❌ 未找到預防醫學諮詢"
fi

# 檢查最後修改時間
echo "3. 檢查網站最後更新時間..."
LAST_MODIFIED=$(curl -s -I https://elai1.vercel.app/ | grep -i "last-modified" | cut -d' ' -f2-)
if [ -n "$LAST_MODIFIED" ]; then
    echo "   📅 最後修改時間: $LAST_MODIFIED"
    
    # 檢查是否為今天更新
    TODAY=$(date -u +"%a, %d %b %Y")
    if echo "$LAST_MODIFIED" | grep -q "$TODAY"; then
        echo "   ✅ 網站今天已更新"
    else
        echo "   ⚠️  網站可能尚未更新到最新版本"
        echo "     建議等待幾分鐘後重試，或清除瀏覽器緩存"
    fi
fi

echo ""
echo "📋 驗證建議:"
echo "1. 直接訪問網站: https://elai1.vercel.app/"
echo "2. 使用無痕模式查看最新版本"
echo "3. 添加時間戳參數避免緩存: https://elai1.vercel.app/?t=$(date +%s)"
echo "4. 等待 5-10 分鐘讓 CDN 緩存更新"
echo ""
echo "🔄 如果網站尚未更新，請稍後再執行此腳本檢查"