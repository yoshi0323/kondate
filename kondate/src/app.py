import streamlit as st
import pandas as pd
from menu_updater import update_menu_with_desserts
import tempfile
import os
from pathlib import Path

# プロジェクトのルートディレクトリを取得
ROOT_DIR = Path(__file__).parent.parent
DATA_DIR = ROOT_DIR / "data"

st.set_page_config(
    page_title="給食AI自動生成システム",
    page_icon="🍰",
    layout="wide"
)

st.title("給食AI自動生成システム 🍰")

st.write("""
## 使い方
1. Excelファイル（input_menu.xlsx）をアップロードしてください
2. 「出力」ボタンをクリックすると処理が開始されます
3. 処理が完了すると、更新されたファイルが自動で開きます
""")

uploaded_file = st.file_uploader("メニューファイルを選択してください", type=['xlsx'])

if uploaded_file is not None:
    if st.button("出力"):
        with st.spinner("デザートを追加中..."):
            try:
                # 一時ファイルとして保存
                with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_input:
                    tmp_input.write(uploaded_file.getvalue())
                    input_path = tmp_input.name

                # 出力用の一時ファイル名を生成
                output_path = str(Path(input_path).with_name('updated_menu.xlsx'))
                
                # メニュー更新処理を実行
                update_menu_with_desserts(input_path, output_path)

                # 一時入力ファイルを削除
                os.unlink(input_path)

                # 出力ファイルは自動で開かれるので、削除はしない
                # ユーザーが必要に応じて保存できる

            except Exception as e:
                st.error(f"エラーが発生しました: {str(e)}")

st.sidebar.write("""
### 機能説明
- 既存のメニューにデザートを自動追加
- 栄養バランスを考慮
- 彩りの良い食材を使用
- 予算内で実現可能なメニュー
""") 