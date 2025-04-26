# Windowsでの実行ファイル作成手順

## 必要な環境

- Windows 10/11
- Python 3.8以上
- Git（任意、ダウンロードでも可）

## 準備手順

1. リポジトリを取得します（2つの方法があります）
   
   **方法1: Gitを使用する場合**
   ```
   git clone https://github.com/yoshi0323/menu.git
   cd menu
   ```

   **方法2: ZIPダウンロードの場合**
   - GitHub（https://github.com/yoshi0323/menu）から「Code」→「Download ZIP」でダウンロード
   - ダウンロードしたZIPファイルを展開
   - コマンドプロンプトで展開したフォルダに移動

2. Python環境をセットアップします
   ```
   pip install -r kondate/requirements.txt
   pip install pyinstaller
   ```

   もし上記のコマンドでエラーが出る場合は、以下を試してください：
   ```
   python -m pip install -r kondate/requirements.txt
   python -m pip install pyinstaller
   ```

3. APIキーの確認
   - `kondate/.env` ファイルを開き、`GOOGLE_API_KEY=AIzaSyBXrDBFIIsMQgCwf4u8P-4RFZb9trnGTWE` の値が入っていることを確認します。

## ビルド実行

1. 以下のコマンドを実行して、Windowsアプリケーションをビルドします：
   ```
   python build.py
   ```

   または
   ```
   python -m build
   ```

2. ビルドには数分かかります。完了すると、`dist` フォルダに `献立管理システム.exe` が生成されます。

## 配布用パッケージの作成

1. 以下のファイルを一つのフォルダにまとめます：
   - `dist/献立管理システム.exe` - 実行ファイル
   - `kondate/.env` - APIキーを含む環境設定ファイル（コピーして.exeと同じフォルダに入れます）

2. このフォルダを圧縮（ZIP形式など）して配布します。

## お客様への説明

- 実行ファイルと.envファイルは必ず同じフォルダに配置する必要があります
- 詳細は「配布手順.md」を参照してください

## トラブルシューティング

ビルド中にエラーが発生した場合：

1. Pythonのバージョンが3.8以上であることを確認
   ```
   python --version
   ```

2. 必要なパッケージがすべてインストールされていることを確認
   ```
   pip list
   ```

3. エラーメッセージを確認し、必要に応じて不足しているパッケージを追加インストール 