import os
import sys
from pathlib import Path
import streamlit as st

# アプリケーションのタイトルと説明
st.set_page_config(
    page_title="給食AI自動生成システム",
    page_icon="🍰",
    layout="wide"
)

# カスタムCSS
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
.stDeployButton {display:none;}
.block-container {padding-top: 2rem;}
</style>
""", unsafe_allow_html=True)

# アプリタイトル
st.title("給食AI自動生成システム 🍰")

# アプリ概要説明
st.write("""
## 使い方
1. Excelファイル（input_menu.xlsx）をアップロードしてください
2. 「通常出力」ボタン：デザート追加と栄養計算を行います
3. 「献立並び替え」ボタン：選択した戦略に基づいて献立を並び替えます
4. 処理が完了すると、更新されたファイルが自動で開かれます
""")

# 注意メッセージ
st.warning("API設定が必要です。.envファイルにAPIキーを設定してください。")

# タブを作成して機能を分ける
tab1, tab2, tab3 = st.tabs(["既存献立の管理", "一週間献立の自動生成", "発注書作成"])

with tab1:
    # 既存の機能（ファイルアップロード、デザート追加、並び替え）
    uploaded_file = st.file_uploader("メニューファイルを選択してください", type=['xlsx'], key="menu_file")

    # ファイルがアップロードされた場合の処理
    if uploaded_file is not None:
        col1, col2 = st.columns(2)
        
        with col1:
            # 出力オプションの選択ラジオボタン
            output_option = st.radio(
                "出力形式を選択してください",
                ["Excel出力", "画像出力"],
                index=0
            )
            
            if st.button("メニュー出力", key="normal_output"):
                st.info("APIキーが必要です。.envファイルを設定してください。")
        
        with col2:
            # 並び替え基本戦略のプルダウン
            reorder_options = [
                "栄養バランス優先並び替え", 
                "ランダム並び替え",
                "曜日指定並び替え"
            ]
            reorder_selection = st.selectbox(
                "並び替えタイプを選択してください:",
                reorder_options
            )
            
            # 曜日指定が選択された場合、曜日とジャンルの追加選択肢を表示
            if reorder_selection == "曜日指定並び替え":
                col_weekday, col_genre = st.columns(2)
                
                with col_weekday:
                    weekday_options = ["月曜日", "火曜日", "水曜日", "木曜日", "金曜日", "土曜日", "日曜日"]
                    selected_weekday = st.selectbox("曜日を選択:", weekday_options)
                
                with col_genre:
                    genre_options = [
                        "麺類", "中華料理", "魚料理", "肉料理", "和食", "洋食", 
                        "丼物", "揚げ物", "シチュー", "カレー"
                    ]
                    selected_genre = st.selectbox("ジャンルを選択:", genre_options)
            
            if st.button("並び替えプレビュー"):
                st.info("APIキーが必要です。.envファイルを設定してください。")

with tab2:
    st.write("## 一週間分の献立を自動生成")
    st.info("この機能にはAPIキーの設定が必要です")

with tab3:
    st.write("## 発注書作成")
    st.info("この機能にはAPIキーの設定が必要です") 