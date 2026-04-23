#!/bin/bash
# 伊萊診所網站更新 SOP 提醒腳本
# 用法: ./follow_sop.sh 或 ./follow_sop.sh [步驟編號]

echo "================================================"
echo "  伊萊診所網站更新標準作業程序 (SOP) 提醒"
echo "================================================"
echo ""

# 檢查是否在正確的目錄
if [ ! -f "WEBSITE_UPDATE_SOP.md" ]; then
    echo "⚠️  警告: 不在伊萊診所網站目錄中"
    echo "請切換到 /workspace/elai-clinic 目錄"
    exit 1
fi

# 顯示 SOP 版本
SOP_VERSION=$(grep -i "^#.*版本" WEBSITE_UPDATE_SOP.md | head -1 | sed 's/#//g')
echo "📋 SOP 版本: $SOP_VERSION"
echo ""

# 如果沒有參數，顯示完整 SOP 摘要
if [ $# -eq 0 ]; then
    echo "📚 完整 SOP 摘要:"
    echo "----------------"
    echo "1. 更新前準備 (第2章)"
    echo "2. 標準修改流程 (第3章)"
    echo "3. 圖片資源管理 (第4章)"
    echo "4. 測試與驗證 (第5章)"
    echo "5. 標準部署流程 (第6章)"
    echo "6. 問題預防措施 (第7章)"
    echo "7. 緊急應變與回滾 (第8章)"
    echo ""
    echo "🔧 實用工具:"
    echo "  • ./check_website_resources.sh    - 資源完整性檢查"
    echo "  • ./test_website_locally.sh       - 本地功能測試"
    echo "  • ./pre_deployment_checklist.sh   - 部署前檢查"
    echo "  • ./deploy_elai_clinic.sh         - 標準部署"
    echo "  • ./rollback_website.sh           - 快速回滾"
    echo ""
    echo "📖 詳細文件:"
    echo "  • WEBSITE_UPDATE_SOP.md           - 完整 SOP"
    echo "  • README_WEBSITE_TOOLS.md         - 工具使用說明"
    echo ""
    echo "💡 提醒 Hermes Agent:"
    echo "  請遵循伊萊診所網站更新 SOP，特別是:"
    echo "  - 更新前運行資源檢查"
    echo "  - 修改後進行本地測試"
    echo "  - 部署前執行檢查清單"
    echo "  - 使用標準部署腳本"
    echo ""
    echo "🚀 快速開始:"
    echo "  ./deploy_elai_clinic.sh \"你的修改描述\""
    echo ""
    exit 0
fi

# 如果有參數，顯示特定步驟
STEP=$1
case $STEP in
    1|"準備"|"prep")
        echo "📝 第1步: 更新前準備"
        echo "------------------"
        echo "1. 檢查當前 Git 狀態"
        echo "2. 查看最近修改記錄"
        echo "3. 確認備份狀態"
        echo "4. 閱讀相關文件"
        echo ""
        echo "🔧 命令:"
        echo "  git status"
        echo "  git log --oneline -5"
        echo "  ls -la *.backup*"
        ;;
    2|"修改"|"modify")
        echo "📝 第2步: 標準修改流程"
        echo "------------------"
        echo "1. 小修改: 直接編輯檔案"
        echo "2. 中修改: 創建測試頁面"
        echo "3. 大修改: 創建分支開發"
        echo "4. 圖片修改: 使用圖片管理工具"
        echo ""
        echo "⚠️  重要提醒:"
        echo "  - 修改圖片路徑時，先確認目標檔案存在"
        echo "  - 避免直接修改生產環境檔案"
        echo "  - 保持修改原子性（一次只改一個功能）"
        ;;
    3|"圖片"|"images")
        echo "📝 第3步: 圖片資源管理"
        echo "------------------"
        echo "1. 圖片必須放在 assets/ 目錄"
        echo "2. 使用正確的檔案格式和大小"
        echo "3. 修改前先備份原圖"
        echo "4. 更新後驗證圖片路徑"
        echo ""
        echo "🔧 命令:"
        echo "  ./check_website_resources.sh"
        echo "  ls -la assets/*.jpg | head -10"
        ;;
    4|"測試"|"test")
        echo "📝 第4步: 測試與驗證"
        echo "------------------"
        echo "1. 運行資源完整性檢查"
        echo "2. 進行本地功能測試"
        echo "3. 檢查關鍵內容"
        echo "4. 驗證圖片載入"
        echo ""
        echo "🔧 命令:"
        echo "  ./check_website_resources.sh"
        echo "  ./test_website_locally.sh"
        echo "  grep -n \"施奕仲\" index.html"
        ;;
    5|"部署"|"deploy")
        echo "📝 第5步: 標準部署流程"
        echo "------------------"
        echo "1. 運行部署前檢查清單"
        echo "2. 使用標準部署腳本"
        echo "3. 提供清晰的提交訊息"
        echo "4. 驗證部署結果"
        echo ""
        echo "🔧 命令:"
        echo "  ./pre_deployment_checklist.sh"
        echo "  ./deploy_elai_clinic.sh \"修改描述\""
        echo "  ./verify_update.sh"
        ;;
    6|"回滾"|"rollback")
        echo "📝 第6步: 緊急應變與回滾"
        echo "------------------"
        echo "1. 查看 Git 提交記錄"
        echo "2. 選擇回滾目標版本"
        echo "3. 執行回滾腳本"
        echo "4. 驗證回滾結果"
        echo ""
        echo "🔧 命令:"
        echo "  git log --oneline -10"
        echo "  ./rollback_website.sh [commit-hash]"
        echo "  ./verify_update.sh"
        ;;
    *)
        echo "❌ 未知步驟: $STEP"
        echo "可用步驟: 1(準備), 2(修改), 3(圖片), 4(測試), 5(部署), 6(回滾)"
        ;;
esac

echo ""
echo "📖 詳細內容請參考: WEBSITE_UPDATE_SOP.md"
echo "💡 提醒: 每次修改網站前，請運行此腳本提醒 Hermes Agent 遵循 SOP"