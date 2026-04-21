#!/usr/bin/env python3
"""
專門處理左邊中央文字的工具
"""

import cv2
import numpy as np
import os

def remove_left_center_text(image_path):
    """移除左邊中央的文字"""
    print(f"🎯 處理左邊中央文字: {os.path.basename(image_path)}")
    
    # 讀取圖片
    img = cv2.imread(image_path)
    if img is None:
        print(f"❌ 無法讀取圖片: {image_path}")
        return None
    
    height, width = img.shape[:2]
    print(f"📏 圖片尺寸: {width}x{height}")
    
    # 左邊中央區域 (根據常見的醫師照片文字位置)
    # 通常文字在醫師白袍的左側胸部位置
    left_center_x1 = 50   # 距離左邊50像素
    left_center_x2 = 250  # 寬度200像素
    left_center_y1 = height // 2 - 100  # 中央偏上
    left_center_y2 = height // 2 + 100  # 中央偏下
    
    print(f"📍 左邊中央區域:")
    print(f"   X: {left_center_x1} 到 {left_center_x2}")
    print(f"   Y: {left_center_y1} 到 {left_center_y2}")
    print(f"   大小: {left_center_x2-left_center_x1}x{left_center_y2-left_center_y1}")
    
    # 創建預覽圖（標記區域）
    preview = img.copy()
    cv2.rectangle(preview, 
                  (left_center_x1, left_center_y1), 
                  (left_center_x2, left_center_y2), 
                  (0, 0, 255), 3)  # 紅色框
    
    # 添加文字標籤
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(preview, "左邊中央文字區域", 
                (left_center_x1, left_center_y1 - 10), 
                font, 0.7, (0, 0, 255), 2)
    cv2.putText(preview, "左邊中央文字區域", 
                (left_center_x1, left_center_y1 - 10), 
                font, 0.7, (255, 255, 255), 1)
    
    # 保存預覽圖
    preview_path = image_path.replace('.jpg', '_left_center_preview.jpg')
    cv2.imwrite(preview_path, preview)
    print(f"📍 預覽圖已保存: {preview_path}")
    
    # 複製原圖進行處理
    result = img.copy()
    
    # 處理左邊中央區域
    region = result[left_center_y1:left_center_y2, left_center_x1:left_center_x2].copy()
    
    if region.shape[0] > 0 and region.shape[1] > 0:
        print(f"🔄 處理左邊中央區域...")
        
        # 方法1: 檢測文字邊緣並修復
        gray_region = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)
        
        # 增強對比度以便更好地檢測文字
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(gray_region)
        
        # 邊緣檢測
        edges = cv2.Canny(enhanced, 50, 150)
        
        # 如果檢測到明顯邊緣（可能是文字）
        if np.sum(edges) > 500:
            print(f"✅ 檢測到文字邊緣，使用修復技術")
            
            # 擴大邊緣區域
            kernel = np.ones((2, 2), np.uint8)
            edges = cv2.dilate(edges, kernel, iterations=1)
            
            # 使用修復算法
            repaired = cv2.inpaint(region, edges, 3, cv2.INPAINT_TELEA)
            result[left_center_y1:left_center_y2, left_center_x1:left_center_x2] = repaired
            
        else:
            print(f"⚠️  未檢測到明顯文字邊緣，使用智能填充")
            
            # 方法2: 智能填充（複製周圍背景）
            # 獲取區域周圍的背景
            border_size = 5
            
            # 上邊界
            if left_center_y1 - border_size >= 0:
                top_border = img[left_center_y1-border_size:left_center_y1, 
                                left_center_x1:left_center_x2]
                if top_border.shape[0] > 0:
                    # 複製上邊界顏色
                    for i in range(min(region.shape[0], 20)):  # 只填充頂部20像素
                        alpha = i / 20.0
                        region[i] = cv2.addWeighted(region[i], 1-alpha, 
                                                   top_border[-1], alpha, 0)
            
            # 下邊界
            if left_center_y2 + border_size <= height:
                bottom_border = img[left_center_y2:left_center_y2+border_size, 
                                   left_center_x1:left_center_x2]
                if bottom_border.shape[0] > 0:
                    # 複製下邊界顏色
                    for i in range(min(region.shape[0], 20)):  # 只填充底部20像素
                        alpha = i / 20.0
                        idx = region.shape[0] - 1 - i
                        region[idx] = cv2.addWeighted(region[idx], 1-alpha, 
                                                     bottom_border[0], alpha, 0)
            
            # 左邊界（特別重要，因為是左側）
            if left_center_x1 - border_size >= 0:
                left_border = img[left_center_y1:left_center_y2, 
                                 left_center_x1-border_size:left_center_x1]
                if left_border.shape[1] > 0:
                    # 複製左邊界顏色（從左到右漸變）
                    for j in range(min(region.shape[1], 30)):  # 只填充左側30像素
                        alpha = j / 30.0
                        region[:, j] = cv2.addWeighted(region[:, j], 1-alpha, 
                                                      left_border[:, -1], alpha, 0)
            
            # 右邊界
            if left_center_x2 + border_size <= width:
                right_border = img[left_center_y1:left_center_y2, 
                                  left_center_x2:left_center_x2+border_size]
                if right_border.shape[1] > 0:
                    # 複製右邊界顏色（從右到左漸變）
                    for j in range(min(region.shape[1], 30)):  # 只填充右側30像素
                        alpha = j / 30.0
                        idx = region.shape[1] - 1 - j
                        region[:, idx] = cv2.addWeighted(region[:, idx], 1-alpha, 
                                                        right_border[:, 0], alpha, 0)
            
            # 放回原圖
            result[left_center_y1:left_center_y2, left_center_x1:left_center_x2] = region
    
    # 保存結果
    output_path = image_path.replace('.jpg', '_left_center_cleaned.jpg')
    cv2.imwrite(output_path, result)
    
    print(f"✅ 清理完成: {output_path}")
    print(f"📊 檔案大小: {os.path.getsize(output_path) / 1024:.1f} KB")
    
    return preview_path, output_path

def create_comparison(preview_path, cleaned_path, original_path):
    """創建對比圖"""
    print(f"📸 創建對比圖...")
    
    original = cv2.imread(original_path)
    preview = cv2.imread(preview_path)
    cleaned = cv2.imread(cleaned_path)
    
    # 調整大小為相同高度
    target_height = 400
    
    def resize_to_height(img, height):
        h, w = img.shape[:2]
        ratio = height / h
        new_w = int(w * ratio)
        return cv2.resize(img, (new_w, height))
    
    original_resized = resize_to_height(original, target_height)
    preview_resized = resize_to_height(preview, target_height)
    cleaned_resized = resize_to_height(cleaned, target_height)
    
    # 創建對比網格
    grid = np.hstack([original_resized, preview_resized, cleaned_resized])
    
    # 添加標籤
    font = cv2.FONT_HERSHEY_SIMPLEX
    labels = ["原圖", "標記區域", "清理後"]
    label_width = original_resized.shape[1]
    
    for i, label in enumerate(labels):
        x = i * label_width + 20
        y = 30
        cv2.putText(grid, label, (x, y), font, 0.8, (255, 255, 255), 3)
        cv2.putText(grid, label, (x, y), font, 0.8, (0, 0, 0), 1)
    
    # 保存對比圖
    comparison_path = original_path.replace('.jpg', '_left_center_comparison.jpg')
    cv2.imwrite(comparison_path, grid)
    
    print(f"✅ 對比圖已保存: {comparison_path}")
    return comparison_path

def main():
    print("🎯 左邊中央文字移除工具")
    print("=" * 60)
    print("💡 專門處理醫師照片左邊中央的文字（通常在白袍上）")
    print()
    
    # 圖片路徑
    image_path = "assets/doctor-shih-with-bg.jpg"
    
    if not os.path.exists(image_path):
        print(f"❌ 圖片不存在: {image_path}")
        return
    
    # 處理左邊中央文字
    preview_path, cleaned_path = remove_left_center_text(image_path)
    
    if preview_path and cleaned_path:
        print()
        
        # 創建對比圖
        comparison_path = create_comparison(preview_path, cleaned_path, image_path)
        
        print()
        print("=" * 60)
        print("✅ 處理完成！")
        print()
        print("📁 生成的檔案:")
        print(f"1. 預覽圖: {os.path.basename(preview_path)}")
        print(f"2. 清理版: {os.path.basename(cleaned_path)}")
        print(f"3. 對比圖: {os.path.basename(comparison_path)}")
        print()
        print("🎯 下一步:")
        print("1. 查看對比圖確認效果")
        print("2. 更新網頁使用清理版本")
        print("3. 提交更改到 GitHub")
        print("4. 等待網站更新")
        
    else:
        print("❌ 處理失敗")

if __name__ == "__main__":
    main()