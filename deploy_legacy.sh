#!/bin/bash
# 伊萊診所網站部署腳本

set -e  # 遇到錯誤時停止執行

echo "開始部署伊萊診所網站..."

# 檢查必要工具
command -v git >/dev/null 2>&1 || { echo "請先安裝 git"; exit 1; }

# 設定顏色輸出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}步驟 1/5: 檢查專案結構${NC}"
if [ ! -f "index.html" ]; then
    echo -e "${RED}錯誤: index.html 不存在${NC}"
    exit 1
fi

echo -e "${GREEN}步驟 2/5: 更新版本資訊${NC}"
# 更新最後更新日期
current_date=$(date '+%Y年%m月%d日 %H:%M')
sed -i "s/最後更新:.*/最後更新: ${current_date}/" index.html
sed -i "s/最後更新:.*/最後更新: ${current_date}/" README.md

echo -e "${GREEN}步驟 3/5: 建立部署檔案${NC}"
# 建立部署目錄
DEPLOY_DIR="_deploy"
rm -rf $DEPLOY_DIR
mkdir -p $DEPLOY_DIR

# 複製必要檔案
cp -r index.html css js assets $DEPLOY_DIR/ 2>/dev/null || true
cp -r blog content scripts $DEPLOY_DIR/ 2>/dev/null || true
cp README.md clinic_info.json $DEPLOY_DIR/ 2>/dev/null || true

# 建立 CNAME 檔案（自訂網域）
if [ -f "CNAME" ]; then
    cp CNAME $DEPLOY_DIR/
fi

# 建立 .nojekyll 檔案（讓 GitHub Pages 不忽略下劃線開頭的目錄）
touch $DEPLOY_DIR/.nojekyll

echo -e "${GREEN}步驟 4/5: 建立 GitHub Pages 設定${NC}"
cat > $DEPLOY_DIR/_config.yml << EOF
# GitHub Pages 設定
title: 伊萊診所
description: 自然醫學、整合醫學、預防醫學與能量醫學
baseurl: ""
url: "https://elai-clinic.tw"
lang: zh-TW
timezone: Asia/Taipei

# 外掛
plugins:
  - jekyll-seo-tag
  - jekyll-sitemap

# 排除檔案
exclude:
  - scripts/
  - node_modules/
  - vendor/
  - Gemfile
  - Gemfile.lock
EOF

echo -e "${GREEN}步驟 5/5: 準備完成${NC}"
echo "部署檔案已準備於 $DEPLOY_DIR 目錄"
echo ""
echo "下一步："
echo "1. 將 $DEPLOY_DIR 目錄內容推送到 GitHub 倉庫"
echo "2. 或使用以下指令部署到 Netlify/Vercel："
echo ""
echo "   # 部署到 Netlify"
echo "   netlify deploy --prod --dir=$DEPLOY_DIR"
echo ""
echo "   # 部署到 Vercel"
echo "   vercel --prod $DEPLOY_DIR"
echo ""
echo "部署完成！網站應該會在幾分鐘內上線。"

# 生成部署報告
cat > deployment-report.md << EOF
# 伊萊診所網站部署報告

- 部署時間: $(date)
- 檔案數量: $(find $DEPLOY_DIR -type f | wc -l)
- 總大小: $(du -sh $DEPLOY_DIR | cut -f1)
- 包含檔案:
  - 首頁 (index.html)
  - CSS 樣式檔案
  - JavaScript 功能檔案
  - 健康資訊文章 ($(find content -name "*.md" 2>/dev/null | wc -l) 篇)
  - 管理腳本

## 部署選項

### GitHub Pages
\`\`\`bash
# 建立新的倉庫
git init $DEPLOY_DIR
cd $DEPLOY_DIR
git add .
git commit -m "部署伊萊診所網站"
git branch -M main
git remote add origin https://github.com/你的帳號/elai-clinic.git
git push -u origin main
\`\`\`

### Netlify
1. 註冊 Netlify 帳號
2. 拖放 $DEPLOY_DIR 到 Netlify 網站
3. 設定自訂網域 (選用)

### Vercel
\`\`\`bash
npm i -g vercel
cd $DEPLOY_DIR
vercel --prod
\`\`\`

## 後續維護
- 使用 Hermes Agent 更新內容
- 定期執行部署腳本
- 備份重要資料
EOF

echo -e "${GREEN}部署報告已生成: deployment-report.md${NC}"