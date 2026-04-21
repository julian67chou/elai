#!/usr/bin/env python3
"""
精確的圖片文字辨識與移除工具
使用 OpenCV 進行文字檢測和修復
"""

import os
import cv2
import numpy as np
from PIL import Image
import sys

def detect_text_regions(image_path):
    """使用 OpenCV 檢測文字區域"""
    print(f"🔍 檢測圖片中的文字區域: {os.path.basename(image_path)}")
    
    # 讀取圖片
    img = cv2.imread(image_path)
    if img is None:
        print(f"❌ 無法讀取圖片: {image_path}")
        return []
    
    # 轉換為灰度圖
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 應用二值化
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    
    # 尋找輪廓
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # 過濾輪廓（只保留可能是文字的）
    text_regions = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        
        # 過濾條件：大小、長寬比
        if w > 10 and h > 10 and w < 200 and h < 100:
            # 計算輪廓面積
            area = cv2.contourArea(contour)
            if area > 50:
                text_regions.append((x, y, w, h))
    
    print(f"   找到 {len(text_regions)} 個可能的文字區域")
    return text_regions, img

def visualize_text_regions(image_path, text_regions):
    """可視化文字區域"""
    img = cv2.imread(image_path)
    
    # 繪製矩形框
    for (x, y, w, h) in text_regions:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
    
    # 保存可視化結果
    output_path = image_path.replace('.jpg', '_text_detection.jpg')
    cv2.imwrite(output_path, img)
    print(f"📊 文字檢測可視化已保存: {output_path}")
    
    return output_path

def remove_text_with_inpainting(image_path, text_regions):
    """使用修復技術移除文字"""
    print(f"🔄 使用修復技術移除文字...")
    
    img = cv2.imread(image_path)
    mask = np.zeros(img.shape[:2], dtype=np.uint8)
    
    # 創建遮罩（文字區域為白色）
    for (x, y, w, h) in text_regions:
        # 稍微擴大區域以確保完全覆蓋
        x1 = max(0, x - 2)
        y1 = max(0, y - 2)
        x2 = min(img.shape[1], x + w + 2)
        y2 = min(img.shape[0], y + h + 2)
        mask[y1:y2, x1:x2] = 255
    
    # 使用修復算法
    result = cv2.inpaint(img, mask, 3, cv2.INPAINT_TELEA)
    
    # 保存結果
    output_path = image_path.replace('.jpg', '_inpainted.jpg')
    cv2.imwrite(output_path, result)
    
    print(f"✅ 修復完成: {output_path}")
    print(f"   原圖大小: {os.path.getsize(image_path) / 1024:.1f} KB")
    print(f"   新圖大小: {os.path.getsize(output_path) / 1024:.1f} KB")
    
    return output_path

def remove_text_with_smart_fill(image_path, text_regions):
    """使用智能填充移除文字"""
    print(f"🎨 使用智能填充移除文字...")
    
    img = cv2.imread(image_path)
    
    for (x, y, w, h) in text_regions:
        print(f"   處理區域: ({x}, {y}, {w}, {h})")
        
        # 擴大區域以獲取更多上下文
        expand = 5
        x1 = max(0, x - expand)
        y1 = max(0, y - expand)
        x2 = min(img.shape[1], x + w + expand)
        y2 = min(img.shape[0], y + h + expand)
        
        # 獲取區域
        region = img[y1:y2, x1:x2].copy()
        
        # 方法1: 使用周圍像素平均
        if region.shape[0] > 0 and region.shape[1] > 0:
            # 創建邊界區域
            border_size = 3
            border = cv2.copyMakeBorder(region, border_size, border_size, border_size, border_size, 
                                       cv2.BORDER_REPLICATE)
            
            # 創建遮罩（中間部分為0，邊界為1）
            mask = np.zeros(border.shape[:2], dtype=np.uint8)
            mask[border_size:-border_size, border_size:-border_size] = 255
            
            # 使用修復
            repaired = cv2.inpaint(border, mask, 3, cv2.INPAINT_TELEA)
            
            # 取回中心部分
            center = repaired[border_size:-border_size, border_size:-border_size]
            
            # 放回原圖
            img[y1:y2, x1:x2] = center
    
    # 保存結果
    output_path = image_path.replace('.jpg', '_smart_filled.jpg')
    cv2.imwrite(output_path, img)
    
    print(f"✅ 智能填充完成: {output_path}")
    return output_path

def manual_text_removal(image_path, text_position="右下角"):
    """手動指定文字位置進行移除"""
    print(f"🛠️ 手動移除文字（位置: {text_position}）...")
    
    img = cv2.imread(image_path)
    height, width = img.shape[:2]
    
    # 根據文字位置定義區域
    if text_position == "右下角":
        # 右下角區域
        x1, y1 = width * 3 // 4, height * 3 // 4
        x2, y2 = width, height
    elif text_position == "底部中央":
        # 底部中央區域
        x1, y1 = width // 3, height * 7 // 8
        x2, y2 = width * 2 // 3, height
    elif text_position == "右上角":
        # 右上角區域
        x1, y1 = width * 3 // 4, 0
        x2, y2 = width, height // 4
    else:
        print(f"❌ 未知位置: {text_position}")
        return None
    
    print(f"   處理區域: ({x1}, {y1}) 到 ({x2}, {y2})")
    
    # 獲取區域
    region = img[y1:y2, x1:x2].copy()
    
    if region.shape[0] > 0 and region.shape[1] > 0:
        # 使用修復技術
        mask = np.ones(region.shape[:2], dtype=np.uint8) * 255
        
        # 檢測區域內的邊緣（文字通常有邊緣）
        gray_region = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray_region, 50, 150)
        
        # 擴大邊緣區域
        kernel = np.ones((3, 3), np.uint8)
        edges = cv2.dilate(edges, kernel, iterations=1)
        
        # 將邊緣作為遮罩
        mask = edges
        
        # 修復
        repaired = cv2.inpaint(region, mask, 3, cv2.INPAINT_TELEA)
        
        # 放回原圖
        img[y1:y2, x1:x2] = repaired
    
    # 保存結果
    output_path = image_path.replace('.jpg', f'_manual_{text_position}.jpg')
    cv2.imwrite(output_path, img)
    
    print(f"✅ 手動移除完成: {output_path}")
    return output_path

def create_comparison_grid(original_path, cleaned_paths):
    """創建對比網格"""
    print(f"📸 創建對比網格...")
    
    # 讀取圖片
    original = cv2.imread(original_path)
    cleaned_images = [cv2.imread(path) for path in cleaned_paths if os.path.exists(path)]
    
    if not cleaned_images:
        print("❌ 沒有清理後的圖片")
        return
    
    # 調整大小為相同高度
    target_height = 400
    original_resized = resize_to_height(original, target_height)
    cleaned_resized = [resize_to_height(img, target_height) for img in cleaned_images]
    
    # 創建網格
    rows = []
    row1 = np.hstack([original_resized] + cleaned_resized[:2])
    
    if len(cleaned_resized) > 2:
        row2 = np.hstack(cleaned_resized[2:])
        # 補齊空白
        if len(cleaned_resized[2:]) < 2:
            blank = np.zeros_like(cleaned_resized[2])
            row2 = np.hstack([row2, blank])
        rows = [row1, row2]
        grid = np.vstack(rows)
    else:
        grid = row1
    
    # 添加標籤
    font = cv2.FONT_HERSHEY_SIMPLEX
    labels = ["原圖"] + [f"方法{i+1}" for i in range(len(cleaned_images))]
    
    for i, label in enumerate(labels):
        x = i * original_resized.shape[1] + 10
        y = 30
        cv2.putText(grid, label, (x, y), font, 0.7, (255, 255, 255), 2)
        cv2.putText(grid, label, (x, y), font, 0.7, (0, 0, 0), 1)
    
    # 保存網格
    output_path = original_path.replace('.jpg', '_comparison.jpg')
    cv2.imwrite(output_path, grid)
    
    print(f"✅ 對比網格已保存: {output_path}")
    return output_path

def resize_to_height(img, target_height):
    """按高度調整大小"""
    h, w = img.shape[:2]
    ratio = target_height / h
    new_w = int(w * ratio)
    return cv2.resize(img, (new_w, target_height))

def main():
    print("🖼️ 精確圖片文字移除工具")
    print("=" * 60)
    
    # 圖片路徑
    image_path = "assets/doctor-shih-with-bg.jpg"
    
    if not os.path.exists(image_path):
        print(f"❌ 圖片不存在: {image_path}")
        return
    
    # 1. 檢測文字區域
    text_regions, img = detect_text_regions(image_path)
    
    if text_regions:
        print(f"\n📊 文字區域詳細信息:")
        for i, (x, y, w, h) in enumerate(text_regions):
            print(f"   區域{i+1}: 位置({x}, {y}), 大小({w}x{h})")
        
        # 可視化
        viz_path = visualize_text_regions(image_path, text_regions)
        
        # 2. 嘗試多種移除方法
        cleaned_paths = []
        
        # 方法1: 修復技術
        inpainted_path = remove_text_with_inpainting(image_path, text_regions)
        cleaned_paths.append(inpainted_path)
        
        # 方法2: 智能填充
        smart_path = remove_text_with_smart_fill(image_path, text_regions)
        cleaned_paths.append(smart_path)
        
        # 方法3: 手動移除（針對"長"字）
        manual_path = manual_text_removal(image_path, "右下角")
        if manual_path:
            cleaned_paths.append(manual_path)
        
        # 方法4: 手動移除底部中央
        manual_bottom = manual_text_removal(image_path, "底部中央")
        if manual_bottom:
            cleaned_paths.append(manual_bottom)
        
        # 3. 創建對比網格
        comparison_path = create_comparison_grid(image_path, cleaned_paths)
        
        print(f"\n🎯 建議:")
        print("1. 檢查對比網格選擇最佳結果")
        print("2. 更新網頁使用最佳圖片")
        print("3. 如果效果不理想，請提供文字具體位置")
        
    else:
        print(f"\n⚠️  未檢測到明顯文字區域")
        print("💡 可能原因:")
        print("   1. 文字顏色與背景相似")
        print("   2. 文字太小或太大")
        print("   3. 需要手動指定位置")
        
        # 仍然嘗試手動移除
        manual_path = manual_text_removal(image_path, "右下角")
        if manual_path:
            print(f"\n✅ 已創建手動清理版本: {manual_path}")

if __name__ == "__main__":
    main()