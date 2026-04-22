#!/usr/bin/env python3
"""
智能文字移除工具 - 只處理指定區域，避免影響臉部
"""

import cv2
import numpy as np
import os

def smart_text_removal(image_path, text_position, output_suffix=""):
    """
    智能移除指定位置的文字
    
    Args:
        image_path: 圖片路徑
        text_position: 文字位置描述
        output_suffix: 輸出檔案後綴
    """
    print(f"🖼️ 智能文字移除: {os.path.basename(image_path)}")
    print(f"📍 文字位置: {text_position}")
    
    # 讀取圖片
    img = cv2.imread(image_path)
    if img is None:
        print(f"❌ 無法讀取圖片: {image_path}")
        return None
    
    height, width = img.shape[:2]
    print(f"📏 圖片尺寸: {width}x{height}")
    
    # 根據文字位置定義處理區域
    # 使用較小的區域，避免影響臉部
    if text_position == "右下角":
        # 右下角小區域
        x1, y1 = width * 7 // 8, height * 7 // 8
        x2, y2 = width - 10, height - 10
        region_name = "bottom_right_corner"
    elif text_position == "底部中央":
        # 底部中央小區域
        x1, y1 = width // 2 - 50, height - 60
        x2, y2 = width // 2 + 50, height - 10
        region_name = "bottom_center"
    elif text_position == "左下角":
        # 左下角小區域
        x1, y1 = 10, height * 7 // 8
        x2, y2 = 100, height - 10
        region_name = "bottom_left_corner"
    elif text_position == "右上角":
        # 右上角小區域
        x1, y1 = width * 7 // 8, 10
        x2, y2 = width - 10, 100
        region_name = "top_right_corner"
    elif text_position == "右側中間":
        # 右側中間小區域
        x1, y1 = width - 100, height // 2 - 50
        x2, y2 = width - 10, height // 2 + 50
        region_name = "right_middle"
    else:
        # 默認：右下角小區域
        print(f"⚠️  未知位置，使用默認右下角")
        x1, y1 = width * 7 // 8, height * 7 // 8
        x2, y2 = width - 10, height - 10
        region_name = "default_bottom_right"
    
    print(f"🎯 處理區域: ({x1}, {y1}) 到 ({x2}, {y2})")
    print(f"📐 區域大小: {x2-x1}x{y2-y1} 像素")
    
    # 確保區域有效
    x1, y1 = max(0, x1), max(0, y1)
    x2, y2 = min(width, x2), min(height, y2)
    
    if x2 <= x1 or y2 <= y1:
        print(f"❌ 無效區域")
        return None
    
    # 複製原圖
    result = img.copy()
    
    # 只處理指定的小區域
    region = result[y1:y2, x1:x2].copy()
    
    if region.shape[0] > 0 and region.shape[1] > 0:
        print(f"🔄 處理區域中...")
        
        # 方法1: 使用周圍顏色平滑過渡
        # 獲取區域邊界的顏色
        border_colors = []
        
        # 上邊界
        if y1 > 0:
            border_colors.extend(img[y1-1, x1:x2].tolist())
        # 下邊界
        if y2 < height:
            border_colors.extend(img[y2, x1:x2].tolist())
        # 左邊界
        if x1 > 0:
            border_colors.extend(img[y1:y2, x1-1].tolist())
        # 右邊界
        if x2 < width:
            border_colors.extend(img[y1:y2, x2].tolist())
        
        if border_colors:
            # 計算平均顏色
            avg_color = np.mean(border_colors, axis=0).astype(np.uint8)
            
            # 創建漸變效果（從邊界到中心）
            h, w = region.shape[:2]
            gradient = np.zeros((h, w, 3), dtype=np.uint8)
            
            for i in range(h):
                for j in range(w):
                    # 計算到邊界的距離
                    dist_to_top = i
                    dist_to_bottom = h - 1 - i
                    dist_to_left = j
                    dist_to_right = w - 1 - j
                    
                    # 使用最近的邊界顏色
                    min_dist = min(dist_to_top, dist_to_bottom, dist_to_left, dist_to_right)
                    
                    if min_dist == dist_to_top and y1 > 0:
                        gradient[i, j] = img[y1-1, x1+j]
                    elif min_dist == dist_to_bottom and y2 < height:
                        gradient[i, j] = img[y2, x1+j]
                    elif min_dist == dist_to_left and x1 > 0:
                        gradient[i, j] = img[y1+i, x1-1]
                    elif min_dist == dist_to_right and x2 < width:
                        gradient[i, j] = img[y1+i, x2]
                    else:
                        gradient[i, j] = avg_color
            
            # 應用漸變
            result[y1:y2, x1:x2] = gradient
            
            print(f"✅ 使用漸變填充")
        else:
            # 方法2: 簡單的顏色填充
            # 獲取區域四個角的顏色
            corners = []
            if y1 > 0 and x1 > 0:
                corners.append(img[y1-1, x1-1])
            if y1 > 0 and x2 < width:
                corners.append(img[y1-1, x2])
            if y2 < height and x1 > 0:
                corners.append(img[y2, x1-1])
            if y2 < height and x2 < width:
                corners.append(img[y2, x2])
            
            if corners:
                avg_color = np.mean(corners, axis=0).astype(np.uint8)
                result[y1:y2, x1:x2] = avg_color
                print(f"✅ 使用平均顏色填充")
            else:
                # 方法3: 使用修復（但只針對文字）
                # 檢測區域內的邊緣（文字通常有邊緣）
                gray_region = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)
                edges = cv2.Canny(gray_region, 50, 150)
                
                if np.sum(edges) > 100:  # 如果有明顯邊緣
                    # 只修復邊緣區域
                    kernel = np.ones((2, 2), np.uint8)
                    edges = cv2.dilate(edges, kernel, iterations=1)
                    
                    repaired = cv2.inpaint(region, edges, 3, cv2.INPAINT_TELEA)
                    result[y1:y2, x1:x2] = repaired
                    print(f"✅ 使用邊緣檢測修復")
                else:
                    # 簡單填充
                    result[y1:y2, x1:x2] = region
                    print(f"⚠️  未檢測到明顯文字，保持原樣")
    
    # 保存結果
    if output_suffix:
        output_filename = f"{os.path.splitext(image_path)[0]}_{output_suffix}.jpg"
    else:
        output_filename = f"{os.path.splitext(image_path)[0]}_smart_{region_name}.jpg"
    
    cv2.imwrite(output_filename, result)
    
    print(f"💾 已保存: {output_filename}")
    print(f"📊 檔案大小: {os.path.getsize(output_filename) / 1024:.1f} KB")
    
    return output_filename

def create_preview_with_marker(image_path, text_position):
    """創建帶有標記的預覽圖"""
    img = cv2.imread(image_path)
    height, width = img.shape[:2]
    
    # 根據位置繪製標記
    if text_position == "右下角":
        center = (width - 50, height - 50)
    elif text_position == "底部中央":
        center = (width // 2, height - 50)
    elif text_position == "左下角":
        center = (50, height - 50)
    elif text_position == "右上角":
        center = (width - 50, 50)
    elif text_position == "右側中間":
        center = (width - 50, height // 2)
    else:
        center = (width - 50, height - 50)
    
    # 繪製圓圈標記
    cv2.circle(img, center, 30, (0, 0, 255), 3)
    cv2.circle(img, center, 32, (255, 255, 255), 1)
    
    # 添加文字標籤
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, f"文字位置: {text_position}", 
                (center[0] - 100, center[1] - 40), 
                font, 0.7, (0, 0, 255), 2)
    cv2.putText(img, f"文字位置: {text_position}", 
                (center[0] - 100, center[1] - 40), 
                font, 0.7, (255, 255, 255), 1)
    
    # 保存預覽圖
    preview_path = image_path.replace('.jpg', f'_preview_{text_position}.jpg')
    cv2.imwrite(preview_path, img)
    
    print(f"📍 位置預覽圖: {preview_path}")
    return preview_path

def main():
    print("🎯 智能文字移除工具")
    print("=" * 60)
    print("💡 特點: 只處理指定小區域，避免影響臉部")
    print()
    
    # 圖片路徑
    image_path = "assets/doctor-shih-with-bg.jpg"
    
    if not os.path.exists(image_path):
        print(f"❌ 圖片不存在: {image_path}")
        return
    
    print("📋 請選擇文字位置:")
    print("1. 右下角 (bottom right)")
    print("2. 底部中央 (bottom center)")
    print("3. 左下角 (bottom left)")
    print("4. 右上角 (top right)")
    print("5. 右側中間 (right middle)")
    print()
    
    # 默認嘗試所有位置
    positions = ["右下角", "底部中央", "左下角", "右上角", "右側中間"]
    
    print("🔄 嘗試所有可能位置...")
    print()
    
    results = []
    
    for position in positions:
        print(f"🔍 嘗試位置: {position}")
        
        # 創建位置預覽
        preview = create_preview_with_marker(image_path, position)
        
        # 智能移除
        cleaned = smart_text_removal(image_path, position, f"smart_{position}")
        
        if cleaned:
            results.append({
                "position": position,
                "preview": preview,
                "cleaned": cleaned
            })
        
        print()
    
    print("=" * 60)
    print("📊 處理完成!")
    print()
    
    if results:
        print("✅ 生成的檔案:")
        for i, result in enumerate(results, 1):
            print(f"{i}. 位置: {result['position']}")
            print(f"   預覽圖: {os.path.basename(result['preview'])}")
            print(f"   清理版: {os.path.basename(result['cleaned'])}")
            print()
        
        print("🎯 建議:")
        print("1. 查看預覽圖確認文字位置")
        print("2. 選擇對應的清理版本")
        print("3. 更新網頁使用正確的版本")
        print("4. 如果都不對，請提供更精確的位置描述")
    else:
        print("❌ 處理失敗")
        print("💡 請提供文字的具體位置描述")

if __name__ == "__main__":
    main()