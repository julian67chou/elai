#!/usr/bin/env python3
"""
檢查和編輯院長照片，去除文字"長"
"""

import os
from PIL import Image, ImageDraw, ImageFont
import sys

def check_image_info(image_path):
    """檢查圖片信息"""
    try:
        with Image.open(image_path) as img:
            print(f"📊 圖片信息: {os.path.basename(image_path)}")
            print(f"   格式: {img.format}")
            print(f"   尺寸: {img.size} (寬x高)")
            print(f"   模式: {img.mode}")
            print(f"   檔案大小: {os.path.getsize(image_path) / 1024:.1f} KB")
            return img
    except Exception as e:
        print(f"❌ 無法打開圖片 {image_path}: {e}")
        return None

def analyze_text_position(img, image_name):
    """分析文字可能的位置"""
    width, height = img.size
    
    print(f"\n🔍 分析 {image_name} 的文字位置:")
    print(f"   圖片尺寸: {width}x{height}")
    
    # 文字通常出現在這些位置
    possible_positions = [
        ("左上角", (0, 0, width//4, height//4)),
        ("右上角", (width*3//4, 0, width, height//4)),
        ("左下角", (0, height*3//4, width//4, height)),
        ("右下角", (width*3//4, height*3//4, width, height)),
        ("底部中央", (width//4, height*7//8, width*3//4, height)),
        ("頂部中央", (width//4, 0, width*3//4, height//8)),
    ]
    
    print("   可能的文字位置:")
    for name, (x1, y1, x2, y2) in possible_positions:
        print(f"   • {name}: ({x1},{y1})-({x2},{y2})")
    
    return possible_positions

def remove_text_from_image(input_path, output_path, text_areas):
    """嘗試去除文字"""
    try:
        with Image.open(input_path) as img:
            draw = ImageDraw.Draw(img)
            
            print(f"\n🔄 嘗試去除文字...")
            
            # 根據文字位置，使用周圍顏色填充
            for area_name, (x1, y1, x2, y2) in text_areas:
                print(f"   處理 {area_name} 區域...")
                
                # 獲取區域周圍的顏色
                sample_x = max(0, x1 - 10)
                sample_y = max(0, y1 - 10)
                
                # 取樣顏色
                if sample_x < img.width and sample_y < img.height:
                    sample_color = img.getpixel((sample_x, sample_y))
                    
                    # 如果是RGBA模式，只取RGB
                    if len(sample_color) == 4:
                        sample_color = sample_color[:3]
                    
                    # 填充矩形區域
                    draw.rectangle([x1, y1, x2, y2], fill=sample_color)
            
            # 保存圖片
            img.save(output_path, quality=95)
            print(f"✅ 已保存到: {output_path}")
            print(f"   新檔案大小: {os.path.getsize(output_path) / 1024:.1f} KB")
            
            return True
            
    except Exception as e:
        print(f"❌ 編輯失敗: {e}")
        return False

def main():
    print("🖼️ 院長照片文字去除工具")
    print("=" * 50)
    
    # 檢查兩張圖片
    images_to_check = [
        ("doctor-shih-with-bg.jpg", "原圖（可能有文字'長'）"),
        ("doctor-shih.jpg", "替代圖（檢查是否有文字）")
    ]
    
    for filename, description in images_to_check:
        filepath = f"assets/{filename}"
        if os.path.exists(filepath):
            img = check_image_info(filepath)
            if img:
                analyze_text_position(img, filename)
                print()
    
    print("\n🎯 建議操作:")
    print("1. 直接編輯 doctor-shih-with-bg.jpg 去除文字")
    print("2. 或使用 doctor-shih.jpg（如果沒有文字）")
    print("3. 或手動編輯圖片")
    
    # 嘗試編輯原圖
    input_image = "assets/doctor-shih-with-bg.jpg"
    output_image = "assets/doctor-shih-cleaned.jpg"
    
    if os.path.exists(input_image):
        print(f"\n🛠️ 嘗試編輯 {input_image}...")
        
        with Image.open(input_image) as img:
            # 假設文字在右下角（常見位置）
            width, height = img.size
            text_areas = [
                ("右下角文字區域", (width*3//4, height*3//4, width, height)),
                ("底部文字區域", (width//3, height*7//8, width*2//3, height)),
            ]
            
            if remove_text_from_image(input_image, output_image, text_areas):
                print(f"\n✅ 已創建清理版本: {output_image}")
                print("💡 請檢查清理效果，然後更新網頁使用此圖片")
            else:
                print("❌ 清理失敗")

if __name__ == "__main__":
    main()