#!/usr/bin/env python
"""
献立管理システム配布パッケージ作成スクリプト
Windows版EXEファイルと設定ファイルを含むZIPアーカイブを作成します
"""

import os
import shutil
import zipfile
import sys
from datetime import datetime
import codecs

# 配布フォルダ名
DIST_DIR = "dist"
PACKAGE_DIR = "配布用パッケージ"

# 配布に含めるファイル
FILES_TO_INCLUDE = [
    # メインファイル
    {"source": os.path.join(DIST_DIR, "kondate_system.exe"), 
     "dest": "kondate_system.exe"},
    {"source": os.path.join(DIST_DIR, "app.py"), 
     "dest": "app.py"},
    {"source": os.path.join(DIST_DIR, "menu_updater.py"), 
     "dest": "menu_updater.py"},
    {"source": os.path.join(DIST_DIR, "nutrition_data.csv"), 
     "dest": "nutrition_data.csv"},
    # 環境設定ファイル
    {"source": os.path.join(DIST_DIR, ".env"), 
     "dest": ".env"},
    # 起動ファイル
    {"source": os.path.join(DIST_DIR, "run_menu.bat"), 
     "dest": "run_menu.bat"},
    {"source": os.path.join(DIST_DIR, "Start.bat"), 
     "dest": "Start.bat"},
    # 説明書
    {"source": "配布手順.md", 
     "dest": "README.txt"}
]

def main():
    print("献立管理システム配布パッケージ作成ツール")
    print("----------------------------------------")
    
    # ディレクトリ設定
    root_dir = os.path.dirname(os.path.abspath(__file__))
    dist_dir = os.path.join(root_dir, 'dist')
    exe_file = os.path.join(dist_dir, 'kondate_system.exe')
    
    # EXEファイルの存在確認
    if not os.path.exists(exe_file):
        print("エラー: EXEファイルが見つかりません。")
        print("先にビルドを実行してください: python build.py")
        return 1
    
    # 配布ファイルの確認
    required_files = [
        'kondate_system.exe',
        'app.py',
        'menu_updater.py',
        'nutrition_data.csv',
        'run_menu.bat',
        'Start.bat'
    ]
    
    missing_files = []
    for file in required_files:
        file_path = os.path.join(dist_dir, file)
        if not os.path.exists(file_path):
            missing_files.append(file)
    
    if missing_files:
        print("エラー: 以下のファイルが見つかりません:")
        for file in missing_files:
            print(f"- {file}")
        print("先にビルドを実行してください: python build.py")
        return 1
    
    # 配布パッケージの作成
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = f"kondate_system_{timestamp}.zip"
    
    # 配布用パッケージフォルダがなければ作成
    package_dir = os.path.join(root_dir, '配布用パッケージ')
    if not os.path.exists(package_dir):
        os.makedirs(package_dir)
    
    # 配布用パッケージフォルダに保存
    zip_path = os.path.join(package_dir, zip_filename)
    
    print(f"配布パッケージを作成中: {zip_filename}")
    
    # ZIPファイルの作成
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in os.listdir(dist_dir):
            file_path = os.path.join(dist_dir, file)
            if os.path.isfile(file_path):
                arcname = os.path.basename(file_path)
                print(f"追加: {arcname}")
                zipf.write(file_path, arcname)
    
    print(f"\n配布パッケージが作成されました: {zip_path}")
    print("\n使用方法:")
    print("1. ZIPファイルを展開")
    print("2. Start.batをダブルクリックして実行")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 