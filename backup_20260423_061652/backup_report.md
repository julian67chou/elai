# 部署前備份報告

## 備份資訊
- **備份時間**: Thu Apr 23 06:16:52 UTC 2026
- **備份目錄**: backup_20260423_061652
- **部署版本**: 30013ee
- **提交訊息**: 更新健康資訊區塊的部落格圖片，根據顏色主題匹配：紅色調用於心臟健康、藍色調用於預防醫學、綠色調用於營養飲食

## 備份內容
- index.html
- css/style.css
- assets/ 目錄

## 檔案清單
- backup_20260423_061652/assets/blog-heart-health.jpg
- backup_20260423_061652/assets/blog-nutrition.jpg
- backup_20260423_061652/assets/blog-preventive-care.jpg
- backup_20260423_061652/assets/doctor-photo.jpg
- backup_20260423_061652/assets/doctor-profile.jpg
- backup_20260423_061652/assets/doctor-shih-backup.jpg
- backup_20260423_061652/assets/doctor-shih-cleaned.jpg
- backup_20260423_061652/assets/doctor-shih-new-optimized.jpg
- backup_20260423_061652/assets/doctor-shih-thumbnail.jpg
- backup_20260423_061652/assets/doctor-shih-transparent.png
- backup_20260423_061652/assets/doctor-shih-with-bg-backup.jpg
- backup_20260423_061652/assets/doctor-shih-with-bg.jpg
- backup_20260423_061652/assets/doctor-shih-with-bg_inpainted.jpg
- backup_20260423_061652/assets/doctor-shih-with-bg_left_center_cleaned.jpg
- backup_20260423_061652/assets/doctor-shih-with-bg_left_center_comparison.jpg
- backup_20260423_061652/assets/doctor-shih-with-bg_left_center_preview.jpg
- backup_20260423_061652/assets/doctor-shih-with-bg_manual_右下角.jpg
- backup_20260423_061652/assets/doctor-shih-with-bg_manual_底部中央.jpg
- backup_20260423_061652/assets/doctor-shih-with-bg_preview_右上角.jpg
- backup_20260423_061652/assets/doctor-shih-with-bg_preview_右下角.jpg
- backup_20260423_061652/assets/doctor-shih-with-bg_preview_右側中間.jpg
- backup_20260423_061652/assets/doctor-shih-with-bg_preview_左下角.jpg
- backup_20260423_061652/assets/doctor-shih-with-bg_preview_底部中央.jpg
- backup_20260423_061652/assets/doctor-shih-with-bg_smart_filled.jpg
- backup_20260423_061652/assets/doctor-shih-with-bg_smart_右上角.jpg
- backup_20260423_061652/assets/doctor-shih-with-bg_smart_右下角.jpg
- backup_20260423_061652/assets/doctor-shih-with-bg_smart_右側中間.jpg
- backup_20260423_061652/assets/doctor-shih-with-bg_smart_左下角.jpg
- backup_20260423_061652/assets/doctor-shih-with-bg_smart_底部中央.jpg
- backup_20260423_061652/assets/doctor-shih-with-bg_text_detection.jpg
- backup_20260423_061652/assets/doctor-shih.jpg
- backup_20260423_061652/assets/favicon.png
- backup_20260423_061652/assets/favicon.svg
- backup_20260423_061652/assets/logo-original.png
- backup_20260423_061652/assets/logo-small.png
- backup_20260423_061652/assets/logo.png
- backup_20260423_061652/assets/logo.svg
- backup_20260423_061652/assets/new_doctor_photo_from_web.jpg
- backup_20260423_061652/assets/unsplash_1551601651-2a8555f1a136.jpg
- backup_20260423_061652/assets/unsplash_1579684385127-1ef15d508118.jpg
- backup_20260423_061652/assets/unsplash_1622253692010-333f2da6031d.jpg
- backup_20260423_061652/assets/unsplash_1622253692010-333f2da6031d.jpg.backup
- backup_20260423_061652/assets/wellness-clinic-backup.jpg
- backup_20260423_061652/assets/wellness-clinic.jpg
- backup_20260423_061652/assets/yilan-landscape.jpg
- backup_20260423_061652/backup_report.md
- backup_20260423_061652/index.html
- backup_20260423_061652/style.css

## 備份目的
此備份用於部署失敗時快速恢復。

## 恢復指令
```bash
# 恢復 index.html
cp backup_20260423_061652/index.html .

# 恢復 CSS
cp backup_20260423_061652/style.css css/

# 恢復圖片
cp -r backup_20260423_061652/assets/* assets/ 2>/dev/null || true
```
