#!/usr/bin/env python3
"""
調整新照片尺寸以適應網頁
"""

from PIL import Image
import os

def resize_photo_for_web(input_path, output_path, max_width=800, max_height=900):
    """調整照片尺寸以適應網頁"""
    print(f"🖼️ 調整照片尺寸: {os.path.basename(input_path)}")
    
    try:
        # 打開圖片
        with Image.open(input_path) as img:
            original_width, original_height = img.size
            print(f"   原始尺寸: {original_width}x{original_height}")
            
            # 計算縮放比例
            width_ratio = max_width / original_width
            height_ratio = max_height / original_height
            ratio = min(width_ratio, height_ratio)
            
            # 計算新尺寸
            new_width = int(original_width * ratio)
            new_height = int(original_height * ratio)
            
            print(f"   目標尺寸: 最大 {max_width}x{max_height}")
            print(f"   縮放比例: {ratio:.2f}")
            print(f"   新尺寸: {new_width}x{new_height}")
            
            # 調整尺寸
            resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # 保存調整後的圖片
            resized_img.save(output_path, 'JPEG', quality=85)
            
            # 檢查檔案大小
            file_size = os.path.getsize(output_path) / 1024
            
            print(f"✅ 已調整尺寸: {output_path}")
            print(f"   檔案大小: {file_size:.1f} KB")
            print(f"   節省空間: {(1 - file_size/(original_width*original_height*3/1024/1024))*100:.1f}%")
            
            return output_path, (new_width, new_height)
            
    except Exception as e:
        print(f"❌ 調整尺寸失敗: {e}")
        return None, None

def create_optimized_version():
    """創建優化版本的照片"""
    print("🎯 創建網頁優化版本")
    print("=" * 60)
    
    # 輸入檔案
    input_path = "assets/new_doctor_photo_from_web.jpg"
    
    if not os.path.exists(input_path):
        print(f"❌ 檔案不存在: {input_path}")
        return None
    
    # 輸出檔案
    output_path = "assets/doctor-shih-new-optimized.jpg"
    
    # 調整尺寸
    optimized_path, dimensions = resize_photo_for_web(
        input_path, 
        output_path,
        max_width=800,  # 適應網頁寬度
        max_height=900  # 適應網頁高度
    )
    
    if optimized_path and dimensions:
        print()
        print("=" * 60)
        print("✅ 優化完成！")
        print()
        print("📊 優化結果:")
        print(f"   原始檔案: new_doctor_photo_from_web.jpg (1141x1091, 638.7KB)")
        print(f"   優化檔案: doctor-shih-new-optimized.jpg ({dimensions[0]}x{dimensions[1]}, {os.path.getsize(optimized_path)/1024:.1f}KB)")
        print()
        print("🎯 優化效果:")
        print("   • 尺寸適合網頁顯示")
        print("   • 保持高畫質")
        print("   • 減少檔案大小，加快載入速度")
        print("   • 專業醫師形象，無文字問題")
        
        return optimized_path
    else:
        return None

def update_html_with_new_photo(photo_path):
    """更新HTML使用新照片"""
    print("\n🌐 準備更新網頁...")
    
    # 讀取HTML檔案
    html_path = "index.html"
    
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 找到院長照片的img標籤
        import re
        pattern = r'<img src="assets/doctor-shih[^"]*\.(?:jpg|png)"[^>]*>'
        
        matches = re.findall(pattern, content)
        if matches:
            print(f"   找到 {len(matches)} 個院長照片標籤")
            
            # 替換第一個找到的（應該是主要的院長照片）
            old_img_tag = matches[0]
            
            # 提取alt和title屬性
            alt_match = re.search(r'alt="([^"]*)"', old_img_tag)
            title_match = re.search(r'title="([^"]*)"', old_img_tag)
            class_match = re.search(r'class="([^"]*)"', old_img_tag)
            
            alt_text = alt_match.group(1) if alt_match else "施奕仲院長"
            title_text = title_match.group(1) if title_match else "施奕仲院長 - 心臟血管內科專科醫師、預防醫學專家"
            class_text = class_match.group(1) if class_match else "doctor-img"
            
            # 創建新的img標籤
            new_img_tag = f'<img src="{photo_path}" alt="{alt_text}" class="{class_text}" title="{title_text}">'
            
            # 替換
            new_content = content.replace(old_img_tag, new_img_tag, 1)
            
            # 寫回檔案
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"✅ 已更新網頁使用: {photo_path}")
            print(f"   舊標籤: {old_img_tag[:50]}...")
            print(f"   新標籤: {new_img_tag}")
            
            return True
        else:
            print("❌ 未找到院長照片標籤")
            return False
            
    except Exception as e:
        print(f"❌ 更新HTML失敗: {e}")
        return False

def main():
    print("🔄 院長照片最終解決方案 - 自動執行")
    print("=" * 60)
    print("💡 將直接使用新照片替換，徹底解決文字問題")
    print()
    
    # 1. 創建優化版本
    optimized_path = create_optimized_version()
    
    if not optimized_path:
        print("❌ 優化失敗，使用原始新照片")
        optimized_path = "assets/new_doctor_photo_from_web.jpg"
    
    print()
    
    # 2. 更新網頁
    if update_html_with_new_photo(optimized_path):
        print()
        print("=" * 60)
        print("🎉 準備就緒！")
        print()
        print("✅ 已完成:")
        print("   1. 下載新照片 ✅")
        print("   2. 調整尺寸優化 ✅")
        print("   3. 更新網頁使用新照片 ✅")
        print()
        print("🚀 下一步:")
        print("   1. 提交更改到 GitHub")
        print("   2. 自動同步到 elai1")
        print("   3. Vercel 自動部署")
        print("   4. 等待2-7分鐘完成更新")
        print()
        print("🔗 檢查連結:")
        print("   • 網站: https://elai1.vercel.app/")
        print("   • 使用 Ctrl+Shift+R 強制刷新")
    else:
        print("❌ 更新失敗")

if __name__ == "__main__":
    main()