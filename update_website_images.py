#!/usr/bin/env python3
"""
更新伊萊診所網站圖片
將原有的兩張圖片替換為符合宜蘭放鬆感和抗老化診所主題的新圖片
"""

import os
import urllib.request
import urllib.error
from pathlib import Path

# 設定
BASE_DIR = Path("/workspace/elai-clinic")
ASSETS_DIR = BASE_DIR / "assets"
INDEX_HTML = BASE_DIR / "index.html"

# 新圖片URL（來自Unsplash，免費使用）
NEW_IMAGES = {
    # 宜蘭風景 - 山景放鬆感
    "yilan-landscape.jpg": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80",
    
    # 現代醫療設備 - 高科技感
    "wellness-clinic.jpg": "https://images.unsplash.com/photo-1559757148-5c350d0d3c56?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80"
}

# 舊圖片映射（舊圖片名稱 -> 新圖片名稱）
REPLACEMENT_MAP = {
    "unsplash_1579684385127-1ef15d508118.jpg": "yilan-landscape.jpg",  # 醫療環境 -> 宜蘭風景
    "unsplash_1551601651-2a8555f1a136.jpg": "wellness-clinic.jpg"     # 團隊圖片 -> 健康診所
}

def download_image(url, filename):
    """下載圖片並保存到assets目錄"""
    filepath = ASSETS_DIR / filename
    
    try:
        print(f"📥 下載圖片: {filename}")
        print(f"  來源: {url}")
        
        # 下載圖片
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req) as response:
            image_data = response.read()
            
        # 保存圖片
        with open(filepath, 'wb') as f:
            f.write(image_data)
        
        print(f"✅ 圖片已保存: {filepath}")
        print(f"  大小: {len(image_data):,} bytes")
        
        return True
        
    except urllib.error.URLError as e:
        print(f"❌ 下載失敗: {e}")
        return False
    except Exception as e:
        print(f"❌ 錯誤: {e}")
        return False

def update_html():
    """更新index.html中的圖片路徑"""
    try:
        with open(INDEX_HTML, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 替換每個舊圖片
        changes_made = 0
        for old_img, new_img in REPLACEMENT_MAP.items():
            old_path = f"assets/{old_img}"
            new_path = f"assets/{new_img}"
            
            # 統計替換次數
            count = content.count(old_path)
            if count > 0:
                content = content.replace(old_path, new_path)
                changes_made += count
                print(f"🔄 替換: {old_img} -> {new_img} ({count}處)")
        
        if changes_made == 0:
            print("ℹ️ 未找到需要替換的圖片路徑")
            return False
        
        # 寫回文件
        with open(INDEX_HTML, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ 成功更新 {changes_made} 處圖片路徑")
        
        # 顯示變更摘要
        print("\n📋 變更摘要:")
        for old_img, new_img in REPLACEMENT_MAP.items():
            print(f"  • {old_img} → {new_img}")
        
        return True
        
    except Exception as e:
        print(f"❌ 更新HTML失敗: {e}")
        return False

def check_existing_images():
    """檢查現有圖片"""
    print("🔍 檢查現有圖片...")
    
    for old_img in REPLACEMENT_MAP.keys():
        old_path = ASSETS_DIR / old_img
        if old_path.exists():
            print(f"  ✓ {old_img} 存在 ({old_path.stat().st_size:,} bytes)")
        else:
            print(f"  ✗ {old_img} 不存在")
    
    print("🔍 檢查新圖片是否已存在...")
    for new_img in REPLACEMENT_MAP.values():
        new_path = ASSETS_DIR / new_img
        if new_path.exists():
            print(f"  ⚠️ {new_img} 已存在，將覆蓋")

def main():
    print("🔄 開始更新伊萊診所網站圖片")
    print("=" * 50)
    
    # 確保目錄存在
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    
    # 檢查現有圖片
    check_existing_images()
    
    print("\n" + "=" * 50)
    print("📥 下載新圖片...")
    
    # 下載新圖片
    download_success = True
    for filename, url in NEW_IMAGES.items():
        if not download_image(url, filename):
            download_success = False
    
    if not download_success:
        print("❌ 圖片下載失敗，中止更新")
        return
    
    print("\n" + "=" * 50)
    print("🔄 更新HTML文件...")
    
    # 更新HTML
    if update_html():
        print("\n" + "=" * 50)
        print("🎉 圖片更新完成！")
        print("\n📝 下一步:")
        print("  1. 檢查網站更新: https://elai1.vercel.app/")
        print("  2. 強制刷新瀏覽器 (Ctrl+Shift+R)")
        print("  3. 如果未顯示更新，等待Vercel自動部署")
        
        # 記錄到任務記憶
        try:
            import subprocess
            subprocess.run([
                "python3", "/workspace/memory_helper.py", "record",
                "--title", "完成伊萊診所圖片更換",
                "--description", "下載並替換兩張圖片，符合宜蘭放鬆感和抗老化診所主題",
                "--steps", "下載宜蘭風景圖片;下載健康診所圖片;更新HTML圖片路徑;測試更新",
                "--result", "圖片已更新，等待Vercel自動部署",
                "--tags", "伊萊診所,圖片更新,Unsplash,宜蘭主題"
            ], cwd="/workspace", check=False)
        except:
            pass
    else:
        print("❌ HTML更新失敗")

if __name__ == "__main__":
    main()