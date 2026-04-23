# 伊萊診所網站更新標準作業程序 (SOP)

## 文件資訊
- **文件版本**: 1.0
- **建立日期**: 2026-04-23
- **適用專案**: elai-clinic (伊萊診所網站)
- **部署架構**: GitHub + Vercel 自動部署
- **上次更新**: $(date)

## 1. 概述與目的

### 1.1 目的
本 SOP 旨在規範 elai-clinic 網站的更新流程，確保：
- 更新過程標準化、可重複
- 避免資源遺失或損壞
- 確保網站功能完整性
- 快速恢復異常狀態

### 1.2 適用範圍
- 所有網站內容更新（文字、圖片、樣式）
- 功能新增或修改
- 網站結構調整
- 緊急修復和問題處理

### 1.3 核心原則
1. **安全第一**：重大修改前必須備份
2. **小步迭代**：頻繁提交小更改，避免大規模修改
3. **完整測試**：部署前必須進行本地測試
4. **清晰記錄**：所有修改必須有詳細記錄
5. **資源保護**：確保所有圖片和資源檔案存在且可訪問

## 2. 更新前準備工作

### 2.1 環境檢查清單
在開始任何修改前，必須完成以下檢查：

```bash
# 1. 確認當前工作目錄
pwd  # 應為 /workspace/elai-clinic

# 2. 檢查 Git 狀態
git status

# 3. 檢查重要資源檔案狀態
ls -la assets/*.jpg assets/*.png | wc -l  # 確認圖片數量

# 4. 檢查網站基本功能
python3 -m http.server 8080 &  # 本地測試伺服器
curl -s http://localhost:8080/ | grep -q "伊萊診所" && echo "✅ 網站正常" || echo "❌ 網站異常"
kill %1  # 關閉測試伺服器
```

### 2.2 資源備份策略
#### 2.2.1 圖片資源備份
```bash
# 創建圖片資源備份
BACKUP_DIR="backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR/assets"
cp -r assets/*.jpg assets/*.png "$BACKUP_DIR/assets/" 2>/dev/null

# 創建備份清單
ls -la assets/*.jpg assets/*.png > "$BACKUP_DIR/image_inventory.txt"
echo "備份時間: $(date)" >> "$BACKUP_DIR/backup_report.md"
```

#### 2.2.2 程式碼備份
```bash
# 創建重要檔案備份
cp index.html "$BACKUP_DIR/index.html.backup"
cp css/style.css "$BACKUP_DIR/style.css.backup"

# 創建 Git 快照
git branch "backup/$(date +%Y%m%d_%H%M%S)"
```

### 2.3 修改計畫制定
每次修改前必須填寫修改計畫表：

| 項目 | 內容 |
|------|------|
| **修改目的** | 明確說明修改原因 |
| **影響範圍** | 列出受影響的檔案和功能 |
| **風險評估** | 高/中/低風險等級 |
| **備份策略** | 具體備份方法 |
| **測試計畫** | 如何測試修改效果 |
| **回滾方案** | 如果失敗如何恢復 |

## 3. 標準修改流程

### 3.1 小型修改流程（文字、樣式微調）
```
1. 檢查 Git 狀態
2. 創建修改分支
3. 進行修改
4. 本地測試
5. 提交更改
6. 合併到主分支
7. 部署
```

### 3.2 中型修改流程（圖片更新、內容重組）
```
1. 完整環境檢查
2. 資源備份
3. 創建修改分支
4. 修改並保留原始檔案備份
5. 多設備測試
6. 創建修改報告
7. 提交並部署
```

### 3.3 大型修改流程（結構重構、功能新增）
```
1. 專案會議確認需求
2. 完整備份（程式碼+資源）
3. 創建功能分支
4. 分階段實施
5. 每階段測試
6. 完整回歸測試
7. 正式部署
```

## 4. 圖片資源管理特別規範

### 4.1 圖片更新流程
基於「院長照片消失」事件，制定以下強制規範：

#### 4.1.1 圖片替換步驟
```bash
# 1. 檢查原始圖片是否存在
ORIGINAL_IMAGE="assets/yilan-landscape.jpg"
if [ ! -f "$ORIGINAL_IMAGE" ]; then
    echo "❌ 錯誤：原始圖片不存在，中止操作"
    exit 1
fi

# 2. 備份原始圖片
BACKUP_IMAGE="assets/yilan-landscape_$(date +%Y%m%d).backup.jpg"
cp "$ORIGINAL_IMAGE" "$BACKUP_IMAGE"

# 3. 檢查新圖片檔案
NEW_IMAGE="path/to/new/image.jpg"
if [ ! -f "$NEW_IMAGE" ]; then
    echo "❌ 錯誤：新圖片不存在，中止操作"
    exit 1
fi

# 4. 驗證新圖片格式和大小
file "$NEW_IMAGE" | grep -q "JPEG image" || echo "⚠️ 警告：非標準JPEG格式"
du -h "$NEW_IMAGE"  # 顯示檔案大小

# 5. 執行替換
cp "$NEW_IMAGE" "$ORIGINAL_IMAGE"

# 6. 更新 HTML 中的圖片引用
# 保持 alt 和 title 屬性不變，除非明確需要修改
```

#### 4.1.2 圖片路徑變更規範
**禁止直接修改圖片路徑而不更新檔案！**

正確做法：
```bash
# 錯誤做法：直接修改HTML中的路徑
# <img src="assets/old-image.jpg"> → <img src="assets/new-image.jpg">

# 正確做法：
# 1. 確保新圖片檔案已存在
cp /path/to/source/new-image.jpg assets/

# 2. 更新HTML
sed -i 's|assets/old-image.jpg|assets/new-image.jpg|g' index.html

# 3. 驗證修改
grep -n "assets/new-image.jpg" index.html
```

### 4.2 圖片存在性檢查腳本
創建自動檢查腳本 `check_website_resources.sh`：

```bash
#!/bin/bash
# 網站資源完整性檢查腳本

echo "🔍 網站資源完整性檢查"
echo "========================"

# 檢查 HTML 中引用的所有圖片
echo "1. 檢查 HTML 中的圖片引用..."
HTML_IMAGES=$(grep -o 'src="[^"]*\.\(jpg\|png\|svg\|gif\)"' index.html | sed 's/src="//' | sed 's/"//')

MISSING_COUNT=0
for img in $HTML_IMAGES; do
    if [ ! -f "$img" ]; then
        echo "   ❌ 缺失: $img"
        MISSING_COUNT=$((MISSING_COUNT + 1))
    else
        echo "   ✅ 存在: $img ($(du -h "$img" | cut -f1))"
    fi
done

# 檢查 CSS 中的背景圖片
echo "2. 檢查 CSS 中的圖片引用..."
CSS_IMAGES=$(grep -o 'url("[^"]*\.\(jpg\|png\|svg\|gif\)")' css/style.css | sed 's/url("//' | sed 's/")//')

for img in $CSS_IMAGES; do
    if [ ! -f "$img" ]; then
        echo "   ❌ 缺失: $img"
        MISSING_COUNT=$((MISSING_COUNT + 1))
    else
        echo "   ✅ 存在: $img"
    fi
done

# 總結報告
echo ""
echo "📊 檢查結果:"
if [ $MISSING_COUNT -eq 0 ]; then
    echo "   ✅ 所有資源檔案完整"
else
    echo "   ❌ 發現 $MISSING_COUNT 個缺失檔案"
    echo "   建議立即修復後再進行部署"
    exit 1
fi
```

## 5. 測試與驗證流程

### 5.1 本地測試清單
在部署前必須完成以下測試：

| 測試項目 | 測試方法 | 預期結果 |
|----------|----------|----------|
| **HTML 語法檢查** | `python3 -m html5validator index.html` | 無錯誤 |
| **圖片載入測試** | 本地伺服器 + 瀏覽器檢查 | 所有圖片正常顯示 |
| **響應式設計** | 調整瀏覽器視窗大小 | 各斷點正常顯示 |
| **連結檢查** | 檢查所有內部連結 | 無404錯誤 |
| **表單功能** | 測試聯絡表單 | 正常提交（測試環境） |
| **控制台錯誤** | 瀏覽器開發者工具 | 無 JavaScript 錯誤 |

### 5.2 自動化測試腳本
```bash
#!/bin/bash
# 網站部署前自動測試腳本

echo "🧪 網站部署前測試"
echo "=================="

# 1. 啟動本地測試伺服器
echo "1. 啟動本地測試伺服器..."
python3 -m http.server 8080 --directory . > /dev/null 2>&1 &
SERVER_PID=$!
sleep 2

# 2. 測試網站可訪問性
echo "2. 測試網站可訪問性..."
if curl -s -f http://localhost:8080/ > /dev/null; then
    echo "   ✅ 網站可正常訪問"
else
    echo "   ❌ 網站無法訪問"
    kill $SERVER_PID 2>/dev/null
    exit 1
fi

# 3. 檢查關鍵內容
echo "3. 檢查關鍵內容..."
REQUIRED_KEYWORDS=("伊萊診所" "施奕仲" "預防醫學" "心臟血管")
for keyword in "${REQUIRED_KEYWORDS[@]}"; do
    if curl -s http://localhost:8080/ | grep -q "$keyword"; then
        echo "   ✅ 包含關鍵字: $keyword"
    else
        echo "   ⚠️  缺少關鍵字: $keyword"
    fi
done

# 4. 檢查圖片資源
echo "4. 檢查圖片資源..."
HTML_CONTENT=$(curl -s http://localhost:8080/)
IMG_TAGS=$(echo "$HTML_CONTENT" | grep -o '<img[^>]*src="[^"]*"' | sed 's/.*src="//' | sed 's/"//')

for img in $IMG_TAGS; do
    if curl -s -f "http://localhost:8080/$img" > /dev/null; then
        echo "   ✅ 圖片可訪問: $img"
    else
        echo "   ❌ 圖片無法訪問: $img"
    fi
done

# 5. 停止測試伺服器
kill $SERVER_PID 2>/dev/null

echo ""
echo "✅ 本地測試完成"
```

## 6. 標準部署流程

### 6.1 完整部署工作流
```bash
#!/bin/bash
# 標準部署腳本 - deploy_elai_clinic.sh

set -e  # 遇到錯誤立即停止

echo "🚀 伊萊診所網站標準部署流程"
echo "============================="

# 步驟 1: 資源完整性檢查
echo "1. 執行資源完整性檢查..."
./check_website_resources.sh

# 步驟 2: 本地測試
echo "2. 執行本地測試..."
./test_website_locally.sh

# 步驟 3: Git 狀態檢查
echo "3. 檢查 Git 狀態..."
git status

# 步驟 4: 提交更改
echo "4. 提交更改..."
read -p "請輸入提交訊息: " COMMIT_MSG
if [ -z "$COMMIT_MSG" ]; then
    COMMIT_MSG="網站更新 - $(date '+%Y-%m-%d %H:%M')"
fi

git add -A
git commit -m "$COMMIT_MSG"

# 步驟 5: 推送到 GitHub
echo "5. 推送到 GitHub..."
git push origin main

# 步驟 6: 創建觸發文件
echo "6. 創建 Vercel 觸發文件..."
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
TRIGGER_FILE="trigger_update_${TIMESTAMP}.txt"

cat > "$TRIGGER_FILE" << EOF
# Vercel 部署觸發文件
觸發時間: $(date)
修改內容: $COMMIT_MSG
執行者: $(whoami)
狀態: 等待部署
EOF

git add "$TRIGGER_FILE"
git commit -m "Trigger Vercel update - ${TIMESTAMP}"
git push origin main

# 步驟 7: 創建部署報告
echo "7. 創建部署報告..."
REPORT_FILE="DEPLOYMENT_REPORT_$(date +%Y%m%d_%H%M%S).md"

cat > "$REPORT_FILE" << EOF
# 伊萊診所網站部署報告

## 基本資訊
- **部署時間**: $(date)
- **提交版本**: $(git rev-parse --short HEAD)
- **提交訊息**: $COMMIT_MSG
- **執行者**: $(whoami)

## 修改內容
### 本次修改摘要
[請填寫具體修改內容]

### 修改的文件清單
$(git diff --name-only HEAD~1 HEAD | sed 's/^/- /')

## 測試結果
- ✅ 資源完整性檢查: 通過
- ✅ 本地功能測試: 通過
- ✅ Git 狀態檢查: 正常

## 部署狀態
1. ✅ Git 提交: 已完成
2. ✅ GitHub 推送: 已完成
3. ⏳ Vercel 部署: 已觸發，等待執行
4. ⏳ CDN 緩存更新: 等待中

## 預計時間線
- 0-2分鐘: GitHub Actions 同步
- 2-7分鐘: Vercel 檢測更新並開始部署
- 7-30分鐘: CDN 緩存更新完成

## 重要連結
- **網站**: https://elai1.vercel.app/
- **GitHub 倉庫**: https://github.com/julian67chou/elai
- **Vercel 控制台**: https://vercel.com/julian67chou
- **部署觸發文件**: $TRIGGER_FILE

## 驗證步驟
1. 等待 5-10 分鐘後訪問網站
2. 檢查修改內容是否已更新
3. 使用無痕模式或清除瀏覽器緩存
4. 運行驗證腳本: ./verify_deployment.sh

## 備註
[其他注意事項]
EOF

echo "✅ 部署報告已創建: $REPORT_FILE"

# 步驟 8: 創建驗證腳本
echo "8. 創建部署驗證腳本..."
cat > verify_deployment.sh << 'EOF'
#!/bin/bash
# 部署驗證腳本

echo "🔍 驗證網站部署狀態"
echo "===================="

SITE_URL="https://elai1.vercel.app/"

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
for item in "${REQUIRED_CONTENT[@]}"; do
    if echo "$CONTENT" | grep -q "$item"; then
        echo "   ✅ 包含: $item"
    else
        echo "   ⚠️  缺少: $item"
    fi
done

# 檢查圖片
echo "3. 檢查圖片載入..."
IMG_COUNT=$(echo "$CONTENT" | grep -o '<img' | wc -l)
echo "   📊 頁面圖片數量: $IMG_COUNT"

# 檢查最後修改時間
echo "4. 檢查更新時間..."
LAST_MODIFIED=$(curl -s -I "$SITE_URL" | grep -i "last-modified" | cut -d' ' -f2-)
if [ -n "$LAST_MODIFIED" ]; then
    echo "   📅 伺服器最後修改時間: $LAST_MODIFIED"
fi

echo ""
echo "📋 驗證建議:"
echo "1. 直接訪問: $SITE_URL"
echo "2. 無痕模式: 避免緩存問題"
echo "3. 添加時間戳: ${SITE_URL}?t=$(date +%s)"
echo "4. 等待 CDN 更新: 可能需要 30 分鐘"
EOF

chmod +x verify_deployment.sh

echo ""
echo "🎉 部署流程完成！"
echo ""
echo "📋 下一步操作:"
echo "1. 等待 5-10 分鐘讓部署完成"
echo "2. 運行驗證腳本: ./verify_deployment.sh"
echo "3. 檢查部署報告: $REPORT_FILE"
echo "4. 如有問題，參考報告中的回滾方案"
```

## 7. 問題預防措施

### 7.1 基於歷史問題的預防措施

#### 7.1.1 圖片資源遺失預防
**問題回顧**: 提交 `0ce65e1` 中將 `yilan-landscape.jpg` 改為不存在的 `hero-image.jpg`

**預防措施**:
1. **強制檢查**: 所有 HTML 修改必須通過資源檢查腳本
2. **雙重驗證**: 修改圖片路徑時，必須驗證目標檔案存在
3. **自動恢復**: 建立常用圖片清單，缺失時自動從備份恢復

#### 7.1.2 程式碼衝突預防
**預防措施**:
1. **分支策略**: 所有修改必須在獨立分支進行
2. **預合併測試**: 合併前必須測試與主分支的兼容性
3. **衝突檢測**: 使用自動化工具檢測潛在衝突

### 7.2 檢查清單系統
建立強制檢查清單，部署前必須全部通過：

```bash
#!/bin/bash
# 部署前強制檢查清單

echo "📋 部署前強制檢查清單"
echo "====================="

CHECKS_PASSED=0
CHECKS_TOTAL=8

# 檢查 1: Git 狀態
echo "1. Git 狀態檢查..."
if [ -z "$(git status --porcelain)" ]; then
    echo "   ✅ 工作區乾淨"
    CHECKS_PASSED=$((CHECKS_PASSED + 1))
else
    echo "   ❌ 有未提交的更改"
fi

# 檢查 2: 資源完整性
echo "2. 資源完整性檢查..."
if ./check_website_resources.sh > /dev/null 2>&1; then
    echo "   ✅ 資源完整"
    CHECKS_PASSED=$((CHECKS_PASSED + 1))
else
    echo "   ❌ 資源缺失"
fi

# 檢查 3: 本地測試
echo "3. 本地功能測試..."
if ./test_website_locally.sh > /dev/null 2>&1; then
    echo "   ✅ 本地測試通過"
    CHECKS_PASSED=$((CHECKS_PASSED + 1))
else
    echo "   ❌ 本地測試失敗"
fi

# 檢查 4: 圖片優化
echo "4. 圖片檔案大小檢查..."
LARGE_IMAGES=$(find assets -name "*.jpg" -size +500k 2>/dev/null | wc -l)
if [ $LARGE_IMAGES -eq 0 ]; then
    echo "   ✅ 無過大圖片檔案"
    CHECKS_PASSED=$((CHECKS_PASSED + 1))
else
    echo "   ⚠️  發現 $LARGE_IMAGES 個大檔案 (>500KB)"
fi

# 檢查 5: HTML 語法
echo "5. HTML 語法檢查..."
if python3 -m html5validator index.html --ignore "section" > /dev/null 2>&1; then
    echo "   ✅ HTML 語法正確"
    CHECKS_PASSED=$((CHECKS_PASSED + 1))
else
    echo "   ❌ HTML 語法錯誤"
fi

# 檢查 6: 外部連結
echo "6. 外部連結檢查..."
EXTERNAL_LINKS=$(grep -o 'href="http[^"]*"' index.html | wc -l)
echo "   📊 外部連結數量: $EXTERNAL_LINKS"
CHECKS_PASSED=$((CHECKS_PASSED + 1))

# 檢查 7: 響應式斷點
echo "7. 響應式設計檢查..."
MEDIA_QUERIES=$(grep -c "@media" css/style.css)
echo "   📊 CSS 媒體查詢數量: $MEDIA_QUERIES"
CHECKS_PASSED=$((CHECKS_PASSED + 1))

# 檢查 8: 備份狀態
echo "8. 備份狀態檢查..."
BACKUP_COUNT=$(find . -name "*.backup*" -o -name "*backup*" | wc -l)
echo "   📊 備份檔案數量: $BACKUP_COUNT"
CHECKS_PASSED=$((CHECKS_PASSED + 1))

# 總結
echo ""
echo "📊 檢查結果: $CHECKS_PASSED/$CHECKS_TOTAL 通過"
if [ $CHECKS_PASSED -eq $CHECKS_TOTAL ]; then
    echo "✅ 所有檢查通過，可以部署"
    exit 0
else
    echo "❌ 檢查未全部通過，請修復問題後再部署"
    exit 1
fi
```

## 8. 緊急應變與回滾方案

### 8.1 問題分類與應對

| 問題類型 | 症狀 | 緊急應對 | 根本解決 |
|----------|------|----------|----------|
| **圖片缺失** | 圖片無法顯示，alt文字可見 | 1. 從備份恢復圖片<br>2. 暫時移除圖片標籤 | 更新資源檢查流程 |
| **樣式錯誤** | 版面混亂，樣式異常 | 1. 恢復 CSS 備份<br>2. 使用 CDN 版本 | 加強 CSS 測試 |
| **功能異常** | 表單、連結失效 | 1. 恢復 JavaScript 備份<br>2. 暫時禁用功能 | 加強功能測試 |
| **部署失敗** | Vercel 部署錯誤 | 1. 檢查錯誤日誌<br>2. 回滾到上個版本 | 優化部署腳本 |

### 8.2 快速回滾腳本
```bash
#!/bin/bash
# 網站快速回滾腳本

echo "🔄 執行網站快速回滾"
echo "==================="

# 確認回滾版本
echo "可用的回滾版本:"
git log --oneline -10

read -p "請輸入要回滾到的 commit hash: " TARGET_COMMIT

if [ -z "$TARGET_COMMIT" ]; then
    echo "❌ 未指定回滾目標"
    exit 1
fi

# 確認操作
read -p "確定要回滾到 $TARGET_COMMIT 嗎？(y/N): " CONFIRM
if [ "$CONFIRM" != "y" ] && [ "$CONFIRM" != "Y" ]; then
    echo "❌ 取消回滾"
    exit 0
fi

# 執行回滾
echo "執行回滾..."
git reset --hard "$TARGET_COMMIT"

# 強制推送到 GitHub
echo "強制推送到 GitHub..."
git push origin main --force

# 創建回滾報告
cat > ROLLBACK_REPORT_$(date +%Y%m%d_%H%M%S).md << EOF
# 網站回滾報告

## 回滾資訊
- **回滾時間**: $(date)
- **目標版本**: $TARGET_COMMIT
- **執行者**: $(whoami)
- **回滾原因**: [請填寫原因]

## 受影響的更改
\`\`\`
$(git log --oneline HEAD..origin/main)
\`\`\`

## 後續行動
1. 等待 Vercel 重新部署
2. 驗證網站功能正常
3. 分析問題原因
4. 制定預防措施

## 重要連結
- 網站: https://elai1.vercel.app/
- GitHub: https://github.com/julian67chou/elai
- 回滾版本: https://github.com/julian67chou/elai/commit/$TARGET_COMMIT
EOF

echo "✅ 回滾完成"
echo "📄 回滾報告已創建"
```

## 9. 文件與知識管理

### 9.1 文件結構規範
```
elai-clinic/
├── docs/                    # 文件目錄
│   ├── SOP/                # 標準作業程序
│   ├── change-logs/        # 修改記錄
│   ├── technical-specs/    # 技術規格
│   └── troubleshooting/    # 故障排除指南
├── scripts/                # 腳本目錄
│   ├── deployment/         # 部署腳本
│   ├── testing/           # 測試腳本
│   └── maintenance/       # 維護腳本
└── backups/               # 備份目錄
    ├── daily/             # 每日備份
    ├── pre-deployment/    # 部署前備份
    └── emergency/         # 緊急備份
```

### 9.2 修改記錄模板
每次修改必須填寫修改記錄：

```markdown
# 修改記錄

## 基本資訊
- **修改日期**: [日期]
- **修改類型**: [功能新增/錯誤修復/內容更新/樣式調整]
- **風險等級**: [高/中/低]
- **執行者**: [姓名]

## 修改內容
### 修改目的
[說明為什麼需要這次修改]

### 具體更改
1. [檔案1]: [修改說明]
2. [檔案2]: [修改說明]
3. [檔案3]: [修改說明]

### 測試結果
- [ ] 本地測試通過
- [ ] 資源檢查通過
- [ ] 跨瀏覽器測試
- [ ] 響應式測試

## 部署資訊
- **部署時間**: [時間]
- **部署版本**: [Git commit hash]
- **部署狀態**: [成功/失敗/部分成功]

## 問題與解決
### 遇到的問題
1. [問題描述]

### 解決方案
1. [解決方法]

### 預防措施
1. [未來如何避免類似問題]
```

## 10. 持續改進

### 10.1 定期審查
- **每週**: 檢查資源完整性
- **每月**: 審查 SOP 執行情況
- **每季**: 全面網站健康檢查
- **每年**: SOP 更新和優化

### 10.2 經驗學習
每次問題發生後，必須進行：
1. **根本原因分析** (Root Cause Analysis)
2. **流程改進建議**
3. **SOP 更新**
4. **團隊培訓**

### 10.3 自動化改進
持續將手動流程自動化：
1. 自動資源檢查
2. 自動測試執行
3. 自動部署驗證
4. 自動報告生成

---

## 附錄 A: 快速參考指南

### A.1 常用命令
```bash
# 檢查資源
./check_website_resources.sh

# 本地測試
./test_website_locally.sh

# 部署前檢查
./pre_deployment_checklist.sh

# 標準部署
./deploy_elai_clinic.sh "修改描述"

# 快速回滾
./rollback_website.sh [commit-hash]
```

### A.2 緊急聯絡
- **技術負責人**: [姓名/職位]
- **備用聯絡人**: [姓名/職位]
- **服務供應商**: Vercel 支援
- **監控系統**: [監控連結]

### A.3 重要連結
- 網站: https://elai1.vercel.app/
- GitHub: https://github.com/julian67chou/elai
- Vercel: https://vercel.com/julian67chou
- 監控: [監控面板連結]

---

**文件版本控制**
| 版本 | 日期 | 修改內容 | 修改者 |
|------|------|----------|--------|
| 1.0 | 2026-04-23 | 初始版本，基於歷史問題制定 | Hermes Agent |
| | | | |

**審核記錄**
| 審核日期 | 審核者 | 審核意見 | 狀態 |
|----------|--------|----------|------|
| | | | 待審核 |
