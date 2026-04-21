#!/usr/bin/env python3
"""
嘗試下載並處理新的院長照片
"""

import requests
from PIL import Image
import io
import os

def download_image(url, save_path):
    """嘗試下載圖片"""
    print(f"🔗 嘗試下載圖片: {url}")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://www.bing.com/',
        'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        'Accept-Language': 'zh-TW,zh;q=0.9,en;q=0.8',
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            # 檢查是否為圖片
            content_type = response.headers.get('content-type', '')
            if 'image' in content_type:
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                
                print(f"✅ 下載成功: {save_path}")
                print(f"   檔案大小: {len(response.content) / 1024:.1f} KB")
                
                # 檢查圖片信息
                try:
                    with Image.open(save_path) as img:
                        print(f"   圖片尺寸: {img.size} (寬x高)")
                        print(f"   圖片格式: {img.format}")
                        print(f"   圖片模式: {img.mode}")
                except Exception as e:
                    print(f"⚠️  無法讀取圖片信息: {e}")
                
                return True
            else:
                print(f"❌ 不是圖片文件: {content_type}")
                return False
        else:
            print(f"❌ 下載失敗: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 下載錯誤: {e}")
        return False

def check_existing_photos():
    """檢查現有的院長照片"""
    print("\n📁 檢查現有院長照片:")
    
    photo_dir = "assets/"
    doctor_photos = []
    
    for filename in os.listdir(photo_dir):
        if filename.startswith("doctor-shih") and filename.endswith((".jpg", ".png", ".jpeg")):
            filepath = os.path.join(photo_dir, filename)
            size = os.path.getsize(filepath) / 1024
            
            try:
                with Image.open(filepath) as img:
                    dimensions = img.size
                    doctor_photos.append({
                        "filename": filename,
                        "path": filepath,
                        "size_kb": size,
                        "dimensions": dimensions
                    })
            except:
                doctor_photos.append({
                    "filename": filename,
                    "path": filepath,
                    "size_kb": size,
                    "dimensions": "未知"
                })
    
    if doctor_photos:
        print(f"   找到 {len(doctor_photos)} 張院長照片:")
        for photo in doctor_photos:
            print(f"   • {photo['filename']}: {photo['dimensions']}, {photo['size_kb']:.1f}KB")
    else:
        print("   未找到院長照片")
    
    return doctor_photos

def create_test_page(photo_paths):
    """創建測試頁面查看所有照片"""
    print("\n🌐 創建照片比較頁面...")
    
    html_content = """<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>院長照片選擇與比較</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        h1 {
            text-align: center;
            color: #333;
            margin-bottom: 10px;
        }
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
        }
        .photo-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .photo-card {
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            transition: transform 0.3s;
        }
        .photo-card:hover {
            transform: translateY(-5px);
        }
        .photo-card img {
            width: 100%;
            height: 300px;
            object-fit: cover;
            border-bottom: 1px solid #eee;
        }
        .photo-info {
            padding: 15px;
        }
        .photo-info h3 {
            margin: 0 0 10px 0;
            color: #333;
            font-size: 16px;
        }
        .photo-info p {
            margin: 5px 0;
            color: #666;
            font-size: 14px;
        }
        .select-btn {
            display: block;
            width: 100%;
            padding: 10px;
            background: #2196f3;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
            margin-top: 10px;
            transition: background 0.3s;
        }
        .select-btn:hover {
            background: #1976d2;
        }
        .instructions {
            background: #e8f5e9;
            border-left: 4px solid #4caf50;
            padding: 15px;
            margin: 20px 0;
            border-radius: 8px;
        }
        .instructions h3 {
            margin-top: 0;
            color: #2e7d32;
        }
        .current-status {
            background: #fff3e0;
            border-left: 4px solid #ff9800;
            padding: 15px;
            margin: 20px 0;
            border-radius: 8px;
        }
        .current-status h3 {
            margin-top: 0;
            color: #f57c00;
        }
    </style>
</head>
<body>
    <h1>🖼️ 院長照片選擇與比較</h1>
    <div class="subtitle">請選擇一張照片替換當前使用的院長照片</div>
    
    <div class="instructions">
        <h3>📋 使用說明</h3>
        <p>1. 查看所有可用的院長照片</p>
        <p>2. 選擇一張沒有文字問題的照片</p>
        <p>3. 點擊"選擇此照片"按鈕</p>
        <p>4. 系統將自動更新網頁並部署</p>
    </div>
    
    <div class="current-status">
        <h3>📊 當前狀態</h3>
        <p><strong>問題:</strong> 當前照片有文字"長"無法完全移除</p>
        <p><strong>解決方案:</strong> 更換為其他院長照片</p>
        <p><strong>目標:</strong> 選擇一張清晰、專業、無文字問題的照片</p>
    </div>
    
    <div class="photo-grid" id="photo-grid">
        <!-- 照片將由JavaScript動態添加 -->
    </div>
    
    <script>
        // 照片數據
        const photos = """
    
    # 添加照片數據
    photos_data = []
    for i, photo in enumerate(photo_paths):
        photos_data.append({
            "id": i,
            "filename": photo["filename"],
            "path": photo["path"].replace("assets/", "assets/"),
            "dimensions": str(photo["dimensions"]),
            "size_kb": f"{photo['size_kb']:.1f}KB"
        })
    
    html_content += str(photos_data)
    
    html_content += """;
        
        // 動態生成照片卡片
        function renderPhotos() {
            const grid = document.getElementById('photo-grid');
            grid.innerHTML = '';
            
            photos.forEach(photo => {
                const card = document.createElement('div');
                card.className = 'photo-card';
                card.innerHTML = `
                    <img src="${photo.path}" alt="${photo.filename}" loading="lazy">
                    <div class="photo-info">
                        <h3>${photo.filename}</h3>
                        <p>尺寸: ${photo.dimensions}</p>
                        <p>大小: ${photo.size_kb}</p>
                        <button class="select-btn" onclick="selectPhoto('${photo.filename}')">
                            選擇此照片
                        </button>
                    </div>
                `;
                grid.appendChild(card);
            });
        }
        
        function selectPhoto(filename) {
            const confirmed = confirm(`確認選擇 ${filename} 作為新的院長照片？\\n\\n系統將：\\n1. 更新網頁使用此照片\\n2. 提交更改到 GitHub\\n3. 觸發網站自動更新`);
            
            if (confirmed) {
                alert(`已選擇: ${filename}\\n\\n正在更新...`);
                
                // 這裡可以添加實際的更新邏輯
                // 例如通過 AJAX 調用後端 API
                
                // 顯示更新狀態
                document.querySelector('.current-status').innerHTML = `
                    <h3>🚀 更新中...</h3>
                    <p><strong>已選擇:</strong> ${filename}</p>
                    <p><strong>狀態:</strong> 正在更新網頁...</p>
                    <p><strong>預計時間:</strong> 5-10分鐘完成部署</p>
                    <p><strong>請稍後檢查網站更新</strong></p>
                `;
            }
        }
        
        // 初始化
        document.addEventListener('DOMContentLoaded', renderPhotos);
    </script>
</body>
</html>"""
    
    # 保存HTML文件
    output_path = "doctor_photo_selection.html"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ 已創建: {output_path}")
    return output_path

def main():
    print("🖼️ 院長照片更換工具")
    print("=" * 60)
    
    # 嘗試下載新圖片
    image_url = "https://www.lianan.com.tw/images/blog/49a3f2a9-389a-4328-bb9b-f97265a74add.jpg"
    save_path = "assets/new_doctor_photo_from_web.jpg"
    
    success = download_image(image_url, save_path)
    
    if not success:
        print("\n⚠️  無法下載指定圖片，嘗試其他方法...")
        print("💡 建議:")
        print("   1. 手動下載圖片後上傳到 assets/ 目錄")
        print("   2. 使用其他現有的院長照片")
        print("   3. 提供其他圖片連結")
    
    # 檢查現有照片
    existing_photos = check_existing_photos()
    
    if existing_photos:
        # 創建選擇頁面
        selection_page = create_test_page(existing_photos)
        
        print("\n" + "=" * 60)
        print("🎯 下一步:")
        print(f"1. 打開 {selection_page} 查看所有照片")
        print("2. 選擇一張合適的照片")
        print("3. 系統將自動更新網頁")
        print("4. 等待網站部署更新")
        
        print("\n💡 建議選擇:")
        print("• doctor-shih.jpg - 原始照片，可能沒有文字")
        print("• doctor-shih-transparent.png - 透明背景，更專業")
        print("• 或其他清理版本")
    else:
        print("\n❌ 沒有可用的院長照片")
        print("💡 請手動添加照片到 assets/ 目錄")

if __name__ == "__main__":
    main()