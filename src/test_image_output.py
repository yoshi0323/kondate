#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from pathlib import Path
from menu_updater import generate_menu_image_output

def main():
    """
    画像出力機能のテスト用スクリプト
    """
    # 現在のディレクトリを取得
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # プロジェクトのルートディレクトリを取得
    root_dir = Path(current_dir).parent
    
    # 入力ファイルパスを指定（ユーザー指定または引数から取得）
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        # デフォルトのサンプルファイル
        input_file = os.path.join(root_dir, "data", "input", "04.xlsx")
        
        if not os.path.exists(input_file):
            print(f"指定されたファイルが見つかりません: {input_file}")
            print("使用法: python test_image_output.py [Excelファイルのパス]")
            sys.exit(1)
    
    print(f"入力ファイル: {input_file}")
    
    # 出力ファイル名を生成
    output_file = os.path.join(os.path.dirname(input_file), "menu_image_output.png")
    
    # 画像出力処理を実行
    try:
        result = generate_menu_image_output(input_file, output_file)
        if result:
            print(f"画像出力が完了しました: {result}")
        else:
            print("画像出力に失敗しました")
    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")
        import traceback
        print(traceback.format_exc())

if __name__ == "__main__":
    main() 