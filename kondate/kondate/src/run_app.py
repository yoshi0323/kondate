import os
import sys
import traceback
import time
import subprocess
import webbrowser

def main():
    try:
        print("=================================================")
        print("     Menu Management System Launcher")
        print("=================================================")
        print("\nChecking environment...")
        
        # アプリケーションのパスを取得
        if getattr(sys, 'frozen', False):
            # PyInstallerでバンドルされた場合
            base_dir = os.path.dirname(sys.executable)
            app_path = os.path.join(base_dir, 'app.py')
            print(f"Mode: Bundled executable")
            print(f"Directory: {base_dir}")
            print(f"App path: {app_path}")
        else:
            # 通常の実行時
            base_dir = os.path.dirname(os.path.abspath(__file__))
            app_path = os.path.join(base_dir, 'app.py')
            print(f"Mode: Development")
            print(f"Directory: {base_dir}")
            print(f"App path: {app_path}")
            
        print("\nSystem paths:")
        for p in sys.path:
            print(f"- {p}")
            
        # 必要なファイルが存在するか確認
        print("\nChecking required files:")
        required_files = ['app.py', 'menu_updater.py', 'nutrition_data.csv']
        missing_files = []
        
        for file in required_files:
            file_path = os.path.join(base_dir, file)
            if os.path.exists(file_path):
                print(f"✓ {file} found: {file_path}")
            else:
                print(f"✗ {file} not found: {file_path}")
                missing_files.append(file)
                
        if missing_files:
            print("\nWarning: Some required files are missing!")
            for file in missing_files:
                print(f"- {file}")
                
            # ファイルを検索してみる
            print("\nSearching for files...")
            found_files = {}
            for root, dirs, files in os.walk(base_dir):
                for file in files:
                    if file in required_files:
                        found_files[file] = os.path.join(root, file)
                        print(f"! Found {file}: {found_files[file]}")
                        
            # 見つかったファイルを使用
            if 'app.py' in found_files:
                app_path = found_files['app.py']
                print(f"\nUsing found app.py: {app_path}")
        
        print("\nLaunching Streamlit application...")
        print(f"App path: {app_path}")
        
        # パラメータの設定 - 127.0.0.1 と 別ポートを指定
        port = 8502
        host = "127.0.0.1"
        
        # カレントディレクトリをアプリのディレクトリに変更
        os.chdir(os.path.dirname(app_path))
        print(f"Changed working directory to: {os.getcwd()}")
        
        # Streamlit起動のコマンド行を構築 (バンドルモードかどうかで変更)
        if getattr(sys, 'frozen', False):
            # 実行可能ファイルの場合は直接pythonを呼び出す
            streamlit_cmd = [
                "python",
                "-m",
                "streamlit",
                "run",
                os.path.basename(app_path),
                f"--server.port={port}",
                f"--server.address={host}",
                "--server.headless=true"
            ]
        else:
            # 開発環境の場合
            streamlit_cmd = [
                sys.executable,
                "-m",
                "streamlit",
                "run",
                app_path,
                f"--server.port={port}",
                f"--server.address={host}",
                "--server.headless=true"
            ]
        
        print(f"\nCommand: {' '.join(streamlit_cmd)}")
        
        # Streamlitをサブプロセスとして起動 (シェルモードでの実行)
        process = subprocess.Popen(
            streamlit_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            shell=True  # シェル経由で実行
        )
        
        # サーバー起動を待つ
        print("\nWaiting for Streamlit server to start...")
        time.sleep(10)  # 十分な待機時間を確保
        
        # ブラウザを自動的に開く
        url = f"http://{host}:{port}"
        print(f"Opening browser at {url}")
        webbrowser.open(url)
        
        print("\nStreamlit server started. Browser should open automatically.")
        print("DO NOT close this window while using the application.")
        print("\nLog output:")
        
        # 出力をリアルタイムで表示
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())
                
        # エラー出力を確認
        stderr = process.stderr.read()
        if stderr:
            print("\nErrors occurred:")
            print(stderr)
            
        return process.poll()
        
    except Exception as e:
        print("\n" + "!" * 50)
        print("   Error occurred")
        print("!" * 50)
        print(f"\nError: {str(e)}")
        print("\nDetailed error information:")
        traceback.print_exc()
        
        print("\nSystem information:")
        print(f"Python path: {sys.executable}")
        print(f"Python version: {sys.version}")
        print(f"Working directory: {os.getcwd()}")
        
        print("\nFile listing:")
        try:
            for root, dirs, files in os.walk(os.getcwd(), topdown=True):
                if len(root.split(os.sep)) > 3:  # 深すぎるディレクトリはスキップ
                    continue
                print(f"\nDirectory: {root}")
                for file in files:
                    print(f"- {file}")
                if len(dirs) > 0:
                    print("Subdirectories:")
                    for dir in dirs:
                        print(f"[DIR] {dir}")
        except Exception as list_err:
            print(f"Error listing directory: {str(list_err)}")
            
        print("\nTroubleshooting:")
        print("1. Ensure all files are extracted")
        print("2. Try running as administrator")
        print("3. Check firewall settings (allow Python/Streamlit through firewall)")
        print("4. Make sure no other application is using port 8502")
        print("5. Try manually running: streamlit run app.py")
        
        input("\nPress Enter to exit...")
        return 1

if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        traceback.print_exc()
        input("\nPress Enter to exit...")
        sys.exit(1) 