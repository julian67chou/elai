#!/usr/bin/env python3
"""
伊萊診所網站管理腳本
使用 Hermes Agent 透過自然語言更新網站內容

功能：
1. 更新診所聯絡資訊
2. 新增/修改健康資訊文章
3. 管理醫師團隊資料
4. 部署網站到 GitHub Pages/Netlify
5. 生成 PDF 文件
"""

import json
import os
import re
import sys
import argparse
import shutil
from pathlib import Path
from datetime import datetime
import markdown
import yaml

# 設定路徑
BASE_DIR = Path(__file__).parent
CONTENT_DIR = BASE_DIR / "content"
BLOG_DIR = BASE_DIR / "blog"
ASSETS_DIR = BASE_DIR / "assets"

# 確保目錄存在
CONTENT_DIR.mkdir(exist_ok=True)
BLOG_DIR.mkdir(exist_ok=True)
ASSETS_DIR.mkdir(exist_ok=True)

class ClinicSiteManager:
    def __init__(self):
        self.clinic_info_file = BASE_DIR / "clinic_info.json"
        self.load_clinic_info()
    
    def load_clinic_info(self):
        """載入診所資訊"""
        if self.clinic_info_file.exists():
            with open(self.clinic_info_file, 'r', encoding='utf-8') as f:
                self.clinic_info = json.load(f)
        else:
            # 預設診所資訊
            self.clinic_info = {
                "name": "伊萊診所",
                "location": "宜蘭市",
                "address": "宜蘭市中山路二段123號",
                "phone": "(03) 123-4567",
                "email": "contact@elai-clinic.tw",
                "hours": {
                    "weekday": "09:00 - 18:00",
                    "saturday": "09:00 - 12:00",
                    "sunday": "休診"
                },
                "services": ["自然醫學", "整合醫學", "預防醫學", "能量醫學"],
                "doctors": [
                    {"name": "陳醫師", "title": "自然醫學專家", "specialties": ["營養治療", "草本醫學"]},
                    {"name": "林醫師", "title": "整合醫學主任", "specialties": ["中西醫整合", "功能醫學"]},
                    {"name": "王醫師", "title": "預防醫學專家", "specialties": ["健康檢查", "風險評估"]},
                    {"name": "張治療師", "title": "能量醫學治療師", "specialties": ["能量檢測", "頻率療法"]}
                ]
            }
            self.save_clinic_info()
    
    def save_clinic_info(self):
        """儲存診所資訊"""
        with open(self.clinic_info_file, 'w', encoding='utf-8') as f:
            json.dump(self.clinic_info, f, ensure_ascii=False, indent=2)
        print(f"診所資訊已更新至 {self.clinic_info_file}")
    
    def update_contact_info(self, field, value):
        """更新聯絡資訊"""
        # 支援的欄位
        contact_fields = {
            'name': '診所名稱',
            'address': '地址',
            'phone': '電話',
            'email': '電子郵件'
        }
        
        if field in self.clinic_info:
            self.clinic_info[field] = value
            self.save_clinic_info()
            print(f"{contact_fields.get(field, field)} 已更新為: {value}")
            
            # 更新 HTML 檔案
            self.update_html_contact(field, value)
        else:
            print(f"不支援的欄位: {field}")
    
    def update_html_contact(self, field, value):
        """更新 HTML 檔案中的聯絡資訊"""
        html_file = BASE_DIR / "index.html"
        if not html_file.exists():
            return
        
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 根據欄位替換
        replacements = {
            'phone': {
                'pattern': r'\(03\) 123-4567',
                'replacement': value
            },
            'address': {
                'pattern': r'宜蘭市中山路二段123號',
                'replacement': value
            },
            'email': {
                'pattern': r'contact@elai-clinic\.tw',
                'replacement': value
            }
        }
        
        if field in replacements:
            pattern = replacements[field]['pattern']
            replacement = replacements[field]['replacement']
            content = re.sub(pattern, replacement, content)
            
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"HTML 檔案已更新 {field}")
    
    def add_health_article(self, title, content, category="一般", author="伊萊診所"):
        """新增健康資訊文章"""
        # 建立 Markdown 檔案
        slug = self.create_slug(title)
        date_str = datetime.now().strftime("%Y-%m-%d")
        
        # Frontmatter
        frontmatter = f"""---
title: "{title}"
date: {date_str}
author: "{author}"
category: "{category}"
tags: ["{category}", "健康"]
---

"""
        
        article_content = frontmatter + content
        
        # 儲存文章
        article_file = CONTENT_DIR / f"{date_str}-{slug}.md"
        with open(article_file, 'w', encoding='utf-8') as f:
            f.write(article_content)
        
        print(f"文章已建立: {article_file}")
        
        # 更新部落格索引
        self.update_blog_index()
        
        # 生成 HTML 版本
        self.generate_article_html(article_file)
    
    def create_slug(self, text):
        """建立 URL 友好的 slug"""
        slug = text.lower()
        slug = re.sub(r'[^\w\s-]', '', slug)  # 移除標點符號
        slug = re.sub(r'[\s_-]+', '-', slug)  # 替換空格為連字符
        slug = slug.strip('-')
        return slug
    
    def update_blog_index(self):
        """更新部落格索引"""
        # 取得所有文章
        articles = []
        for md_file in CONTENT_DIR.glob("*.md"):
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 解析 Frontmatter
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    frontmatter = parts[1]
                    try:
                        meta = yaml.safe_load(frontmatter)
                        meta['slug'] = md_file.stem
                        articles.append(meta)
                    except:
                        continue
        
        # 依日期排序
        articles.sort(key=lambda x: x.get('date', ''), reverse=True)
        
        # 更新 JSON 索引
        index_file = BLOG_DIR / "index.json"
        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump(articles, f, ensure_ascii=False, indent=2)
        
        print(f"部落格索引已更新: {index_file}")
    
    def generate_article_html(self, md_file):
        """從 Markdown 生成 HTML"""
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 解析 Frontmatter
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                frontmatter = parts[1]
                body = parts[2]
                
                # 轉換 Markdown 為 HTML
                html_content = markdown.markdown(body, extensions=['extra'])
                
                # 建立 HTML 檔案
                html_file = BLOG_DIR / f"{md_file.stem}.html"
                
                # 建立完整的 HTML 頁面
                html_template = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <title>{md_file.stem} - 伊萊診所健康資訊</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css">
    <link rel="stylesheet" href="/css/style.css">
</head>
<body>
    <div class="container py-5">
        <article>
            <h1>{md_file.stem}</h1>
            <div class="article-content">
                {html_content}
            </div>
        </article>
    </div>
</body>
</html>"""
                
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(html_template)
                
                print(f"HTML 文章已生成: {html_file}")
    
    def list_articles(self):
        """列出所有文章"""
        index_file = BLOG_DIR / "index.json"
        if index_file.exists():
            with open(index_file, 'r', encoding='utf-8') as f:
                articles = json.load(f)
            
            print("健康資訊文章列表:")
            for i, article in enumerate(articles, 1):
                print(f"{i}. {article.get('title', '無標題')}")
                print(f"   日期: {article.get('date', '未知')}")
                print(f"   類別: {article.get('category', '未分類')}")
                print()
        else:
            print("尚無文章")
    
    def generate_pdf(self):
        """生成網站 PDF 文件（需安裝 wkhtmltopdf）"""
        try:
            import pdfkit
            # 轉換 HTML 為 PDF
            html_file = BASE_DIR / "index.html"
            pdf_file = BASE_DIR / "伊萊診所資訊.pdf"
            
            options = {
                'page-size': 'A4',
                'margin-top': '0.75in',
                'margin-right': '0.75in',
                'margin-bottom': '0.75in',
                'margin-left': '0.75in',
                'encoding': "UTF-8",
                'no-outline': None
            }
            
            pdfkit.from_file(str(html_file), str(pdf_file), options=options)
            print(f"PDF 已生成: {pdf_file}")
            
        except ImportError:
            print("請先安裝 pdfkit 和 wkhtmltopdf")
            print("安裝指令: pip install pdfkit")
            print("macOS: brew install wkhtmltopdf")
            print("Ubuntu: sudo apt-get install wkhtmltopdf")
        except Exception as e:
            print(f"生成 PDF 失敗: {e}")
    
    def serve_local(self, port=8000):
        """啟動本地測試伺服器"""
        import http.server
        import socketserver
        
        os.chdir(BASE_DIR)
        
        handler = http.server.SimpleHTTPRequestHandler
        with socketserver.TCPServer(("", port), handler) as httpd:
            print(f"伺服器啟動於 http://localhost:{port}")
            print("按 Ctrl+C 停止")
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\n伺服器已停止")
    
    def deploy_github_pages(self):
        """部署到 GitHub Pages"""
        print("部署到 GitHub Pages...")
        print("1. 建立 GitHub 倉庫")
        print("2. 初始化 Git")
        print("3. 設定 GitHub Actions")
        print("4. 推送程式碼")
        print("5. 啟用 GitHub Pages")
        print()
        print("請執行以下指令：")
        print()
        print("cd /workspace/elai-clinic")
        print("git init")
        print("git add .")
        print('git commit -m "初始提交"')
        print("git branch -M main")
        print("git remote add origin https://github.com/你的帳號/elai-clinic.git")
        print("git push -u origin main")
        print()
        print("然後到 GitHub 設定中啟用 GitHub Pages")

def main():
    parser = argparse.ArgumentParser(description="伊萊診所網站管理工具")
    subparsers = parser.add_subparsers(dest="command", help="指令")
    
    # 更新聯絡資訊
    contact_parser = subparsers.add_parser("update-contact", help="更新聯絡資訊")
    contact_parser.add_argument("field", help="欄位 (name, address, phone, email)")
    contact_parser.add_argument("value", help="新的值")
    
    # 新增文章
    article_parser = subparsers.add_parser("add-article", help="新增健康資訊文章")
    article_parser.add_argument("title", help="文章標題")
    article_parser.add_argument("--content", help="文章內容", default="")
    article_parser.add_argument("--category", help="文章分類", default="一般")
    article_parser.add_argument("--author", help="作者", default="伊萊診所")
    
    # 列出文章
    subparsers.add_parser("list-articles", help="列出所有文章")
    
    # 生成 PDF
    subparsers.add_parser("generate-pdf", help="生成網站 PDF")
    
    # 本地伺服器
    serve_parser = subparsers.add_parser("serve", help="啟動本地測試伺服器")
    serve_parser.add_argument("--port", type=int, default=8000, help="連接埠")
    
    # 部署
    subparsers.add_parser("deploy", help="部署到 GitHub Pages")
    
    # 幫助
    subparsers.add_parser("help", help="顯示幫助")
    
    args = parser.parse_args()
    
    manager = ClinicSiteManager()
    
    if args.command == "update-contact":
        manager.update_contact_info(args.field, args.value)
    
    elif args.command == "add-article":
        if not args.content:
            # 從 stdin 讀取內容
            print("請輸入文章內容 (結束請按 Ctrl+D):")
            content_lines = []
            try:
                while True:
                    line = input()
                    content_lines.append(line)
            except EOFError:
                pass
            args.content = "\n".join(content_lines)
        manager.add_health_article(args.title, args.content, args.category, args.author)
    
    elif args.command == "list-articles":
        manager.list_articles()
    
    elif args.command == "generate-pdf":
        manager.generate_pdf()
    
    elif args.command == "serve":
        manager.serve_local(args.port)
    
    elif args.command == "deploy":
        manager.deploy_github_pages()
    
    elif args.command == "help" or args.command is None:
        parser.print_help()
        print()
        print("使用範例:")
        print("  python3 manage_site.py update-contact phone '(03) 9876-5432'")
        print("  python3 manage_site.py add-article '冬季保健注意事項' --category '預防醫學'")
        print("  python3 manage_site.py serve --port 8080")
        print("  python3 manage_site.py generate-pdf")

if __name__ == "__main__":
    main()