# PowerShellスクリプト版のメニュー起動スクリプト
# 現在のディレクトリに移動
Set-Location -Path $PSScriptRoot

# 実行ファイルのパス設定
$EXEFILE = "kondate_system.exe"

# ファイルの存在を確認
if (-not (Test-Path $EXEFILE)) {
    Write-Host "ERROR: $EXEFILE not found." -ForegroundColor Red
    Write-Host "Application could not start. Please check files." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# アプリケーションの起動
Write-Host "Starting application..." -ForegroundColor Green
Write-Host "Please wait for browser to open..." -ForegroundColor Yellow

Start-Process -FilePath $EXEFILE

Write-Host "Application running! Do not close this window." -ForegroundColor Cyan
Write-Host "Press Ctrl+C to quit." -ForegroundColor Cyan

# ユーザーが Ctrl+C を押すまで待機
try {
    while ($true) {
        Start-Sleep -Seconds 1
    }
} finally {
    Write-Host "Exiting..." -ForegroundColor Yellow
} 