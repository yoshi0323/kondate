#!/usr/bin/env python
"""
献立管理システム配布パッケージ作成スクリプト
Windows版EXEファイルと設定ファイルを含むZIPアーカイブを作成します
"""

import os
import shutil
import zipfile
import sys
import datetime

# 配布フォルダ名
DIST_DIR = "dist"
PACKAGE_DIR = "配布用パッケージ"

# 配布に含めるファイル
FILES_TO_INCLUDE = [
    # EXEファイル
    {"source": os.path.join(DIST_DIR, "献立管理システム.exe"), 
     "dest": "献立管理システム.exe"},
    # 環境設定ファイル
    {"source": "kondate/.env", 
     "dest": ".env"},
    # 説明書
    {"source": "配布手順.md", 
     "dest": "README.md"}
]

def create_distribution_package():
    """配布用パッケージを作成する"""
    print("献立管理システム配布パッケージ作成ツール")
    print("-" * 40)
    
    # EXEファイルが存在するか確認
    if not os.path.exists(os.path.join(DIST_DIR, "献立管理システム.exe")):
        print("エラー: EXEファイルが見つかりません。")
        print("先にビルドを実行してください: python build.py")
        return False
    
    # .envファイルが存在するか確認
    if not os.path.exists("kondate/.env"):
        print("エラー: 環境設定ファイル(.env)が見つかりません。")
        return False
    
    # 配布用フォルダを作成
    if os.path.exists(PACKAGE_DIR):
        shutil.rmtree(PACKAGE_DIR)
    os.makedirs(PACKAGE_DIR)
    
    # ファイルをコピー
    for file_info in FILES_TO_INCLUDE:
        src = file_info["source"]
        dest = os.path.join(PACKAGE_DIR, file_info["dest"])
        
        if os.path.exists(src):
            print(f"コピー中: {src} -> {dest}")
            shutil.copy2(src, dest)
        else:
            print(f"警告: {src} が見つかりません。スキップします。")
    
    # ZIPアーカイブを作成
    today = datetime.datetime.now().strftime("%Y%m%d")
    zip_filename = f"献立管理システム_{today}.zip"
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(PACKAGE_DIR):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, PACKAGE_DIR)
                print(f"ZIPに追加: {file_path} -> {arcname}")
                zipf.write(file_path, arcname)
    
    print("-" * 40)
    print(f"配布パッケージを作成しました: {zip_filename}")
    print("このZIPファイルをお客様に提供してください。")
    return True

if __name__ == "__main__":
    success = create_distribution_package()
    if not success:
        sys.exit(1) 