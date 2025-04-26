import PyInstaller.__main__
import os
import sys

# アプリケーションのルートディレクトリ
root_dir = os.path.dirname(os.path.abspath(__file__))

# OSに合わせたパス区切り文字を設定
if sys.platform.startswith('win'):
    separator = ';'  # Windows
else:
    separator = ':'  # macOS/Linux

PyInstaller.__main__.run([
    'kondate/src/app.py',  # メインスクリプト
    '--name=献立管理システム',  # アプリケーション名
    '--onefile',  # 単一の実行ファイルに
    '--windowed',  # コンソール画面を表示しない
    f'--add-data=kondate/data{separator}data',  # OSに合わせたパス区切り
    '--icon=kondate/assets/icon.ico',  # アイコン
    '--clean',  # ビルド前にキャッシュをクリア
    '--hidden-import=streamlit',
    '--hidden-import=google.generativeai',
    '--hidden-import=pandas',
    '--hidden-import=openpyxl',
    '--hidden-import=xlsxwriter',
    '--hidden-import=importlib.metadata',
    '--hidden-import=python-dotenv',
    '--hidden-import=dotenv',
]) 