import PyInstaller.__main__
import os
import sys
from pathlib import Path
import shutil

# アプリケーションのルートディレクトリ
root_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(root_dir, 'kondate', 'src')
data_dir = os.path.join(root_dir, 'kondate', 'data')
assets_dir = os.path.join(root_dir, 'kondate', 'assets')

# ビルドディレクトリを指定
build_dir = os.path.join(root_dir, 'build')
dist_dir = os.path.join(root_dir, 'dist')

print("=================================================")
print("     Menu Management System Builder")
print("=================================================")
print(f"Source directory: {src_dir}")
print(f"Building application...")

# ASCII名のバッチファイル作成
with open('run_menu.bat', 'w', encoding='ascii') as f:
    f.write('@echo off\n')
    f.write('setlocal\n\n')
    f.write('REM Change to script directory\n')
    f.write('cd /d "%~dp0"\n\n')
    f.write('REM Set paths\n')
    f.write('set EXEFILE=kondate_system.exe\n\n')
    f.write('REM Check files\n')
    f.write('if not exist "%EXEFILE%" (\n')
    f.write('    echo ERROR: %EXEFILE% not found.\n')
    f.write('    goto :ERROR\n')
    f.write(')\n\n')
    f.write('REM Run the application\n')
    f.write('echo Starting application...\n')
    f.write('echo Please wait for browser to open...\n\n')
    f.write('start "" "%EXEFILE%"\n\n')
    f.write('echo Application running! Do not close this window.\n')
    f.write('echo Press Ctrl+C to quit.\n')
    f.write('cmd /k\n\n')
    f.write(':ERROR\n')
    f.write('echo Application could not start. Please check files.\n')
    f.write('pause\n')

print("Created run_menu.bat")

# コピー先ディレクトリを作成/クリーン
for dir_path in [build_dir, dist_dir]:
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
    os.makedirs(dir_path)

print(f"Cleaned build directories")

# シンプルな方法でStart.batも作成
with open(os.path.join(dist_dir, 'Start.bat'), 'w', encoding='ascii') as f:
    f.write('@echo off\n')
    f.write('echo Menu Management System\n')
    f.write('echo =====================\n')
    f.write('echo Starting application...\n\n')
    f.write('cd /d "%~dp0"\n')
    f.write('run_menu.bat\n')

print("Created Start.bat")

# OSに合わせたパス区切り文字を設定
if sys.platform.startswith('win'):
    separator = ';'  # Windows
else:
    separator = ':'  # macOS/Linux

# 直接ディレクトリにコピーするファイル
important_files = {
    'app.py': os.path.join(src_dir, 'app.py'),
    'menu_updater.py': os.path.join(src_dir, 'menu_updater.py'),
    'nutrition_data.csv': os.path.join(src_dir, 'nutrition_data.csv')
}

# 必要なファイルを直接distディレクトリにコピー
for dest_name, src_path in important_files.items():
    if os.path.exists(src_path):
        dest_path = os.path.join(dist_dir, dest_name)
        shutil.copy2(src_path, dest_path)
        print(f"Copied {src_path} to {dest_path}")

# 環境設定ファイルをコピー
env_files = [
    os.path.join(root_dir, '.env'),
    os.path.join(root_dir, 'kondate', '.env')
]

for env_file in env_files:
    if os.path.exists(env_file):
        dest_path = os.path.join(dist_dir, os.path.basename(env_file))
        shutil.copy2(env_file, dest_path)
        print(f"Copied {env_file} to {dest_path}")

# ランチャーファイルをコピー
launcher_files = [
    'run_menu.bat'
]

for launcher in launcher_files:
    src_path = os.path.join(root_dir, launcher)
    if os.path.exists(src_path):
        dest_path = os.path.join(dist_dir, launcher)
        shutil.copy2(src_path, dest_path)
        print(f"Copied {src_path} to {dest_path}")

print("\nCompiling application with PyInstaller...")

# PyInstallerでコンパイル
PyInstaller.__main__.run([
    os.path.join(src_dir, 'run_app.py'),  # ラッパースクリプト
    '--name=kondate_system',  # ASCII名のアプリケーション名
    '--onefile',  # 単一の実行ファイルに
    '--clean',  # ビルド前にキャッシュをクリア
    '--paths=' + src_dir,  # ソースディレクトリを追加
    '--debug=all',  # デバッグ情報を表示
    '--hidden-import=streamlit',
    '--hidden-import=streamlit.runtime',
    '--hidden-import=streamlit.web',
    '--hidden-import=streamlit.web.cli',
    '--hidden-import=google.generativeai',
    '--hidden-import=pandas',
    '--hidden-import=openpyxl',
    '--hidden-import=xlsxwriter',
    '--hidden-import=python-dotenv',
    '--hidden-import=dotenv',
    '--distpath=' + dist_dir,  # 出力先ディレクトリを指定
    '--console',  # コンソールウィンドウを表示
])

print("\nBuild completed! Distribution files created in:")
print(dist_dir)
print("\nTo create a distribution package run:")
print("python create_distribution.py") 