@echo off
REM 給食AI自動生成システムの起動スクリプト

echo === 給食AI自動生成システム 起動中 ===
echo.

REM Pythonが利用可能かチェック
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo エラー: Pythonが見つかりません。インストールしてから再実行してください。
    pause
    exit /b 1
)

REM 必要なパッケージをインストール
echo 必要なパッケージを確認しています...
cd /d "%~dp0"
python -m pip install -r requirements.txt

REM Streamlitアプリケーションを起動
echo アプリケーションを起動しています...
cd /d "%~dp0src"
start "" streamlit run app.py

echo.
echo ブラウザが自動的に開かない場合は、次のURLにアクセスしてください:
echo http://localhost:8501
echo.
echo ウィンドウを閉じるとアプリケーションが終了します。

timeout /t 5 