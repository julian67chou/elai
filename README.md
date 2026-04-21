# 伊萊診所網站

專業的自然醫學、整合醫學、預防醫學與能量醫學診所網站。

## 網站架構

```
elai-clinic/
├── index.html          # 首頁（單頁面應用）
├── about.html          # 關於我們頁面
├── css/
│   └── style.css      # 自訂樣式（醫療風格）
├── js/
│   └── main.js        # 網站功能
├── assets/            # 圖片、字體等資源
├── content/           # Markdown 內容檔案
├── blog/              # 部落格文章
└── scripts/           # Hermes 管理腳本
```

## 功能特色

1. **專業醫療設計**
   - 醫療藍色與綠色主題
   - 響應式設計（手機、平板、電腦）
   - 中文字體優化（思源黑體）

2. **核心功能**
   - 線上預約系統
   - 醫師團隊介紹
   - 服務項目展示
   - 健康資訊部落格
   - Google 地圖整合
   - PDF 下載功能

3. **Hermes 管理功能**
   - 自然語言更新內容
   - 自動生成健康資訊
   - 一鍵部署到 GitHub Pages
   - Markdown 內容管理

## 使用 Hermes 管理網站

### 基本指令

```bash
# 更新診所資訊
「更新診所電話為 (03) 9876-5432」
「修改營業時間為週一至週六 9:00-18:00」

# 新增健康文章
「新增一篇關於冬季保健的文章」
「在健康資訊新增『糖尿病預防』文章」

# 更新醫師介紹
「新增一位復健科醫師」
「更新陳醫師的專長領域」

# 部署網站
「部署網站到 GitHub Pages」
「更新網站到網路」
```

### 進階管理

使用 `scripts/manage_site.py` 腳本：

```bash
# 啟動本地測試伺服器
python3 scripts/manage_site.py --serve

# 更新所有頁面
python3 scripts/manage_site.py --update

# 生成健康資訊 PDF
python3 scripts/manage_site.py --generate-pdf

# 部署到 GitHub Pages
python3 scripts/manage_site.py --deploy
```

## 部署選項

### 1. GitHub Pages（免費）
```bash
# Hermes 會自動幫您：
# 1. 建立 GitHub 倉庫
# 2. 設定 GitHub Actions
# 3. 配置自訂網域
# 4. 啟用 HTTPS
```

### 2. Netlify（免費）
```bash
# 功能：
# - 自動部署
# - 表單處理
# - 全球 CDN
# - 即時預覽
```

### 3. Vercel（免費）
```bash
# 適合現代化網站
# 速度快，支援 Serverless Functions
```

## 內容管理系統

### Markdown 格式

健康資訊文章使用 Markdown 格式儲存在 `content/` 目錄：

```markdown
---
title: "地中海飲食對心血管的益處"
date: 2024-03-15
author: "陳醫師"
category: "營養健康"
tags: ["飲食", "心血管", "健康"]
---

# 地中海飲食對心血管的益處

地中海飲食富含橄欖油、堅果、魚類和蔬果...
```

### 自動生成

Hermes 可以自動：
- 從 Markdown 生成 HTML 頁面
- 更新部落格索引
- 生成 RSS feed
- 建立網站地圖

## 網站維護

### 定期更新
1. **每週**：更新健康資訊
2. **每月**：檢查聯絡資訊
3. **每季**：更新醫師團隊
4. **每年**：審查服務項目

### 備份策略
- Git 版本控制
- 自動備份到 Google Drive
- 離線備份 PDF 文件

## 客製化修改

### 修改顏色主題
編輯 `css/style.css` 中的 CSS 變數：

```css
:root {
    --primary-blue: #1a5276;
    --primary-green: #2ecc71;
    /* ... */
}
```

### 修改聯絡資訊
編輯 `index.html` 中的聯絡區塊，或使用 Hermes 指令：

```
「更新診所地址為宜蘭市中山路三段456號」
「新增 Line 官方帳號連結」
```

### 新增服務項目
在 `index.html` 的服務區塊新增項目，或使用 Hermes：

```
「新增『兒童發展評估』服務項目」
「在服務項目加入『睡眠障礙治療』」
```

## 故障排除

### 常見問題

1. **中文顯示問題**
   - 確保使用 UTF-8 編碼
   - 檢查字體載入順序
   - 使用思源黑體備用字體

2. **行動裝置顯示**
   - 測試不同螢幕尺寸
   - 檢查觸控按鈕大小
   - 優化圖片載入

3. **表單無法提交**
   - 檢查 JavaScript 錯誤
   - 驗證必填欄位
   - 測試網路連線

### 支援

如有問題，請使用 Hermes 指令：

```
「網站出現亂碼怎麼辦」
「如何新增預約時段」
「我想修改網站顏色」
```

## 技術規格

- **前端框架**：Bootstrap 5.3
- **字體**：思源黑體 Noto Sans TC
- **圖標**：Bootstrap Icons
- **地圖**：Google Maps Embed
- **部署**：GitHub Pages / Netlify
- **管理工具**：Hermes Agent + Python 腳本

## 更新記錄

- **2024-03-15**：初版網站建立
- **2024-03-16**：新增 Hermes 管理功能
- **2024-03-17**：優化行動裝置體驗

---

**重要提醒**：本網站為靜態網站，實際醫療服務請以診所現場公告為準。緊急情況請撥打 119。