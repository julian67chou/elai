# GitHub Actions 自動同步設置指南

## 🎯 目標
當 `elai` 倉庫更新時，自動同步到 `elai1` 倉庫，觸發 Vercel 自動部署。

## 📋 設置步驟

### 步驟1：在 GitHub 設置 Secrets
1. 訪問 `elai` 倉庫的 Settings
2. 左側選單選擇 **Secrets and variables** → **Actions**
3. 點擊 **New repository secret**

#### 需要創建的 Secret：
| 名稱 | 值 | 說明 |
|------|-----|------|
| `ELAI1_SYNC_TOKEN` | 您的 GitHub 權杖 | 用於推送 elai1 倉庫 |

### 步驟2：權杖權限要求
權杖需要以下權限：
- ✅ `repo` (全部)
- ✅ `workflow` (可選)

### 步驟3：驗證設置
1. 對 `elai` 倉庫做一個小修改
2. 查看 Actions 標籤頁：https://github.com/julian67chou/elai/actions
3. 檢查 `elai1` 倉庫是否更新：https://github.com/julian67chou/elai1

## 🔧 工作流程文件

### 主要工作流程
- `.github/workflows/auto-sync-vercel.yml` - 自動同步腳本
- `.github/workflows/sync-to-elai1.yml` - 備用同步腳本
- `.github/scripts/sync-to-elai1.sh` - 同步腳本

### 觸發條件
- 當 `main` 分支有推送時
- 排除 `.github/workflows/` 路徑，避免循環觸發

## 🚀 使用方法

### 正常更新流程：
```bash
# 1. 在本地修改 elai 項目
cd /workspace/elai-clinic

# 2. 提交更改
git add .
git commit -m "更新網站內容"

# 3. 推送到 GitHub
git push origin main

# 4. GitHub Actions 會自動：
#    - 檢測 elai 的更新
#    - 同步到 elai1 倉庫
#    - Vercel 自動部署 elai1
```

### 手動觸發同步：
1. 訪問 https://github.com/julian67chou/elai/actions
2. 選擇 "Auto Sync to elai1 (Vercel)" 工作流程
3. 點擊 **Run workflow**

## 🔍 監控與故障排除

### 檢查點：
1. **GitHub Actions 狀態**：https://github.com/julian67chou/elai/actions
2. **elai1 倉庫**：https://github.com/julian67chou/elai1
3. **Vercel 部署**：https://vercel.com/julian67chou

### 常見問題：
1. **同步失敗**：檢查 `ELAI1_SYNC_TOKEN` 是否有效
2. **權限不足**：確保權杖有 `repo` 權限
3. **循環觸發**：工作流程文件修改可能觸發自身

## 📁 文件結構
```
.github/
├── workflows/
│   ├── auto-sync-vercel.yml    # 主同步工作流程
│   └── sync-to-elai1.yml       # 備用同步
└── scripts/
    └── sync-to-elai1.sh        # 同步腳本
```

## ⚙️ 自定義配置

### 修改同步頻率（如果需要定時同步）：
```yaml
on:
  schedule:
    - cron: '0 */6 * * *'  # 每6小時同步一次
  push:
    branches: [ main ]
```

### 同步特定路徑：
```yaml
on:
  push:
    branches: [ main ]
    paths:
      - 'src/**'
      - 'public/**'
```

## 🔒 安全注意事項
1. **權杖安全**：不要將權杖提交到代碼中
2. **最小權限**：權杖只需 `repo` 權限
3. **定期更新**：每90天更新權杖

## 📞 支持
如有問題，檢查：
1. GitHub Actions 日誌
2. 權杖有效期
3. 倉庫權限設置

**設置完成後，您的 Vercel 部署將完全自動化！**