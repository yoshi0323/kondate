import pandas as pd
import datetime
from pathlib import Path

# プロジェクトのルートディレクトリを取得
ROOT_DIR = Path(__file__).parent.parent
DATA_DIR = ROOT_DIR / "data"

def create_sample_input():
    """サンプルの入力ファイルを作成"""
    data = {
        '日付': [
            datetime.date(2024, 4, 1),
            datetime.date(2024, 4, 2),
        ],
        '栄養素': [
            '総カロリー: 800kcal\nP:30g, F:25g, C:100g',
            '総カロリー: 750kcal\nP:28g, F:22g, C:95g',
        ],
        '朝食': [
            'ごはん、味噌汁、焼き魚',
            'パン、スープ、サラダ',
        ],
        '昼食 (主菜/副菜/汁物)': [
            '唐揚げ/ポテトサラダ/味噌汁',
            'ハンバーグ/温野菜/コーンスープ',
        ],
        '昼食：食材/1人分/45人分': [
            '鶏もも肉150g/6.75kg\nじゃがいも50g/2.25kg\n...',
            'ひき肉120g/5.4kg\n季節の野菜80g/3.6kg\n...',
        ],
        '夕食 (主菜/副菜/小鉢/汁物)': [
            '煮魚/おひたし/漬物/すまし汁',
            '肉じゃが/ほうれん草胡麻和え/漬物/味噌汁',
        ],
        '夕食：食材/1人分/45人分': [
            'さば100g/4.5kg\nほうれん草60g/2.7kg\n...',
            '牛肉100g/4.5kg\nじゃがいも80g/3.6kg\n...',
        ],
    }
    
    df = pd.DataFrame(data)
    
    # 出力先ディレクトリを作成
    output_path = DATA_DIR / "input" / "input_menu.xlsx"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # ファイルを保存
    df.to_excel(output_path, index=False)
    print(f'サンプル入力ファイルを作成しました: {output_path}')

if __name__ == "__main__":
    create_sample_input() 