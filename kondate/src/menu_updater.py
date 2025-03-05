import google.generativeai as genai
from pathlib import Path
import pandas as pd
import random
import subprocess
import os
from datetime import datetime
from typing import Tuple, Dict, List
from dotenv import load_dotenv
import re

# .envファイルから環境変数を読み込む
load_dotenv()

# Gemini APIキーを設定
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

# プロジェクトのルートディレクトリを取得
ROOT_DIR = Path(__file__).parent.parent
DATA_DIR = ROOT_DIR / "data"

def generate_desserts_batch(menu_data: List[Dict]) -> List[Tuple[str, str]]:
    """複数のメニューに対するデザートをバッチ処理で生成"""
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        # バッチ処理用のプロンプトを作成
        prompt = """以下の複数の食事メニューに対して、それぞれに合ったデザートを提案してください。
各デザートは簡単に調理できるもの（市販のゼリーの素、ゼラチン、寒天、アガー、ホットケーキミックスなど）を使用し、
おしゃれなトッピング（ストロベリーソース、セルフィーユ、カラースプレー、エディブルフラワーなど）を取り入れてください。

"""
        
        # 各メニューの情報を追加
        for i, item in enumerate(menu_data):
            prompt += f"\n===== メニュー{i+1}: {item['meal_type']} =====\n"
            prompt += item['menu_text'] + "\n"
        
        prompt += """
各メニューに対して、以下の形式で出力してください：

===== デザート{番号} =====
デザート名

材料 (1人分):
  - [材料1]: [量]g/[45人分の量]g
  - [材料2]: [量]g/[45人分の量]g
  ...

彩り効果:
  - [色1]: [食材名]
  - [色2]: [食材名]
  ...

栄養価:
  - [栄養素1]
  - [栄養素2]
  ...
"""
        
        # LLMに一括でリクエスト
        response = model.generate_content(prompt)
        
        if not response.text:
            raise ValueError("LLMの応答が空です")
        
        # 応答を解析してデザート情報を抽出
        result = response.text.strip()
        dessert_sections = re.split(r'===== デザート\d+ =====', result)
        
        # 最初の空セクションを削除
        if dessert_sections and not dessert_sections[0].strip():
            dessert_sections = dessert_sections[1:]
        
        # 各デザートの情報を抽出
        desserts = []
        for section in dessert_sections:
            if not section.strip():
                continue
                
            parts = section.strip().split('\n\n')
            if not parts:
                continue
                
            name = parts[0].strip()
            ingredients = '\n'.join(parts[1:3]) if len(parts) >= 3 else ""
            
            desserts.append((name, ingredients))
        
        # メニュー数とデザート数が一致しない場合、足りない分をモックデータで補完
        while len(desserts) < len(menu_data):
            desserts.append(mock_llm_dessert_generator(menu_data[len(desserts)]['meal_type']))
        
        return desserts

    except Exception as e:
        print(f"バッチデザート生成エラー: {str(e)}")
        # エラー時はモックデータで全て補完
        return [mock_llm_dessert_generator(item['meal_type']) for item in menu_data]

def generate_dessert_with_llm(meal_type: str, existing_menu: str) -> Tuple[str, str]:
    """その日のメニューに合わせたデザートとその材料を生成"""
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        prompt = f"""
以下の{meal_type}メニューに合わせたデザートを1つ提案してください：

現在のメニュー:
{existing_menu}

必須条件：
1. メニューとの調和
   - 上記の{meal_type}メニューの味や雰囲気と調和する
   - 食材の重複を避ける
   - 季節感を考慮する

2. 彩り要素（1つ以上）
   - 季節のフルーツ
   - エディブルフラワー
   - 食用ハーブ
   - 自然な色味の食材

3. 栄養面
   - 給食の栄養バランスを補完
   - 過度な糖分を避ける
   - 適度な食物繊維を含む

4. 提供面
   - 大量調理（45人分）が可能
   - 盛り付けが効率的
   - 常温で30分程度の品質維持が可能

5. 簡単に調理できるもの
   - 市販のゼリーの素
   - ゼラチン、寒天、アガー
   - ホットケーキミックス
   - 簡単に調理できる材料を使用

6. おしゃれなトッピング
   - ストロベリーソース
   - セルフィーユ
   - カラースプレー
   - エディブルフラワー
   - 少しおしゃれな要素を取り入れる

以下の形式で出力してください：
デザート名

材料 (1人分):
  - [材料1]: [量]g/[45人分の量]g
  - [材料2]: [量]g/[45人分の量]g
  ...

彩り効果:
  - [色1]: [食材名]
  - [色2]: [食材名]
  ...

栄養価:
  - [栄養素1]
  - [栄養素2]
  ...
"""
        
        response = model.generate_content(prompt)
        
        if response.text:
            result = response.text.strip()
            parts = result.split('\n\n')
            
            name = parts[0].strip()
            ingredients = '\n'.join(parts[1:3])  # 材料部分のみ抽出

            return name, ingredients

        raise ValueError("LLMの応答が不正な形式です")

    except Exception as e:
        print(f"デザート生成エラー: {str(e)}")
        return mock_llm_dessert_generator(meal_type)

def mock_llm_dessert_generator(meal_type: str) -> Tuple[str, str]:
    """
    LLMのバックアップとして、デザートとその材料のリストを生成する模擬関数
    """
    desserts = [
        {
            'name': '彩りフルーツヨーグルト with エディブルフラワー',
            'ingredients': '''
デザート材料 (1人分):
  - プレーンヨーグルト: 100g/4500g
  - 季節のフルーツ（イチゴ、キウイ、マンゴー）: 45g/2025g
  - 蜂蜜: 5g/225g
  - エディブルフラワー（ビオラ）: 2輪/90輪
  - ミントの葉: 1枚/45枚
  - グラノーラ: 10g/450g
色彩効果: 白(ヨーグルト)、赤(イチゴ)、緑(キウイ)、黄(マンゴー)、紫(ビオラ)
栄養価: タンパク質6g、食物繊維2g、カルシウム120mg
'''
        },
        {
            'name': '抹茶わらび餅 with 黒蜜と季節の花',
            'ingredients': '''
デザート材料 (1人分):
  - わらび餅粉: 20g/900g
  - 抹茶: 2g/90g
  - 黒蜜: 10g/450g
  - きな粉: 5g/225g
  - 食用パンジー: 1輪/45輪
  - ミントの葉: 1枚/45枚
色彩効果: 緑(抹茶)、茶(きな粉)、紫(パンジー)、緑(ミント)
栄養価: 食物繊維1g、鉄分0.5mg、カルシウム50mg
'''
        },
        {
            'name': 'レモンゼリー with ベリーソースとミント',
            'ingredients': '''
デザート材料 (1人分):
  - レモンゼリーの素: 15g/675g
  - 水: 100ml/4500ml
  - ミックスベリー: 20g/900g
  - ミントの葉: 1枚/45枚
  - はちみつ: 5g/225g
色彩効果: 黄(ゼリー)、赤(ベリー)、緑(ミント)
栄養価: ビタミンC 15mg、食物繊維1g
'''
        },
        {
            'name': 'ホットケーキミックスのカップケーキ with カラースプレー',
            'ingredients': '''
デザート材料 (1人分):
  - ホットケーキミックス: 30g/1350g
  - 牛乳: 20ml/900ml
  - 卵: 1/10個/45個
  - カラースプレー: 2g/90g
  - セルフィーユ: 1枝/45枝
色彩効果: 黄(ケーキ)、虹色(カラースプレー)、緑(セルフィーユ)
栄養価: タンパク質3g、カルシウム50mg
'''
        }
    ]
    selected = random.choice(desserts)
    return selected['name'], selected['ingredients']

def generate_nutrition_info() -> str:
    """栄養素情報を生成"""
    nutrients = [
        f"総カロリー: {random.randint(500, 700)}kcal",
        f"タンパク質: {random.randint(15, 25)}g",
        f"脂質: {random.randint(8, 12)}g",
        f"炭水化物: {random.randint(70, 90)}g",
        f"食物繊維: {random.randint(3, 6)}g",
        f"カルシウム: {random.randint(200, 300)}mg",
        f"鉄分: {random.randint(2, 4)}mg"
    ]
    return '\n'.join(nutrients)

def analyze_excel_structure(df: pd.DataFrame) -> dict:
    """LLMを使用してExcelの構造を解析"""
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        # 最初の10行を文字列として取得
        sample_data = df.head(10).to_string()
        print(f"解析対象データ:\n{sample_data}\n")
        
        prompt = """
入力された給食献立表のデータ構造を解析してください。
以下の点に注意して解析してください：

1. A列は色分けされており、朝食・昼食・夕食の区分を示しています
2. 献立名、食品名、重量(g)、総使用量(g)の列があります
3. 既存のメニューは変更せず、デザートのみを追加します

データ構造を解析し、以下の情報を特定してください：
1. 食事区分（朝食・昼食・夕食）の判定方法
2. 各列の役割（献立名、食材、分量など）
3. データの階層構造

応答は以下のJSON形式で返してください：
{
    "meal_indicators": {
        "breakfast": ["朝食", "朝"],
        "lunch": ["昼食", "昼"],
        "dinner": ["夕食", "夕", "夜"]
    },
    "columns": {
        "menu": "献立名",
        "ingredients": "食品名",
        "weight": "重量(g)",
        "total_weight": "総使用量(g)"
    }
}
"""
        
        print(f"LLMへのプロンプト:\n{prompt}\n")
        
        response = model.generate_content(prompt)
        print(f"LLMからの応答:\n{response.text}\n")
        
        # 応答をPythonの辞書に変換
        import json
        structure_info = json.loads(response.text)
        return structure_info
    
    except Exception as e:
        print(f"構造解析エラーの詳細: {str(e)}")
        print(f"エラーの種類: {type(e)}")
        import traceback
        print(f"スタックトレース:\n{traceback.format_exc()}")
        
        # デフォルトの構造情報を返す
        return {
            "meal_indicators": {
                "breakfast": ["朝食", "朝"],
                "lunch": ["昼食", "昼"],
                "dinner": ["夕食", "夕", "夜"]
            },
            "columns": {
                "menu": "献立名",
                "ingredients": "食品名",
                "weight": "重量(g)",
                "total_weight": "総使用量(g)"
            }
        }

def parse_menu_to_structured_data(df: pd.DataFrame) -> dict:
    """ExcelデータをCSV形式の構造化データに変換"""
    menu_structure = {
        'meals': [],
        'ingredients': []
    }
    
    try:
        current_meal = None
        current_dish = None
        
        # 朝食・昼食・夕食の基本メニューを追加（データがない場合のバックアップ）
        for meal in ['朝食', '昼食', '夕食']:
            menu_structure['meals'].append({
                'meal_type': meal,
                'dish_name': f'{meal}の基本メニュー'
            })
            
            # 基本的な食材も追加
            menu_structure['ingredients'].append({
                'meal_type': meal,
                'dish_name': f'{meal}の基本メニュー',
                'name': '米飯',
                'weight_per_person': '150g',
                'total_weight': '6750g'
            })
            
            menu_structure['ingredients'].append({
                'meal_type': meal,
                'dish_name': f'{meal}の基本メニュー',
                'name': '味噌汁',
                'weight_per_person': '200g',
                'total_weight': '9000g'
            })
        
        for idx, row in df.iterrows():
            # 各列のデータを取得（数字コードは除外）
            meal_type = str(row.iloc[0]).strip()
            menu_name = str(row.iloc[1]).strip() if pd.notna(row.iloc[1]) else ''
            ingredient_raw = str(row.iloc[2]).strip() if pd.notna(row.iloc[2]) else ''
            weight = str(row.iloc[3]).strip() if pd.notna(row.iloc[3]) else ''
            total = str(row.iloc[4]).strip() if pd.notna(row.iloc[4]) else ''
            
            # 食材名から数字コードを除去
            ingredient = ' '.join([part for part in ingredient_raw.split() if not part.isdigit()])
            
            # 食事区分の判定
            if any(key in meal_type for key in ['朝食', '昼食', '夕食']):
                current_meal = meal_type
                continue
            
            # メニュー名の処理
            if menu_name and menu_name != 'nan':
                current_dish = menu_name
                menu_structure['meals'].append({
                    'meal_type': current_meal,
                    'dish_name': menu_name
                })
            
            # 食材の処理
            if ingredient.strip() and ingredient != 'nan':
                menu_structure['ingredients'].append({
                    'meal_type': current_meal,
                    'dish_name': current_dish,
                    'name': ingredient.strip(),
                    'weight_per_person': weight,
                    'total_weight': total
                })
        
        return menu_structure
    
    except Exception as e:
        print(f"データ構造化エラー: {str(e)}")
        raise

def format_ingredients(ingredients_by_dish: dict) -> str:
    """食材情報を整形"""
    formatted = []
    for dish_name, ingredients in ingredients_by_dish.items():
        dish_text = [f"{dish_name}("]
        for ingredient in ingredients:
            # 食材コードを除去し、食材名と分量のみを表示
            name = ingredient['name']
            per_person = ingredient['weight_per_person']
            total = ingredient['total_weight']
            dish_text.append(f"  {name}: {per_person}/{total}")
        dish_text.append(")")
        formatted.append('\n'.join(dish_text))
    return '\n\n'.join(formatted)

def calculate_nutrition_with_llm(meals: dict, ingredients: dict) -> str:
    """メニューと食材から栄養価を計算"""
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        # メニューと食材情報を整形
        menu_text = []
        for meal_type in ['朝食', '昼食', '夕食']:
            menu_text.append(f"=== {meal_type} ===")
            menu_text.append("メニュー:")
            menu_text.extend(meals[meal_type])
            menu_text.append("食材と分量:")
            menu_text.extend(ingredients[meal_type])
            menu_text.append("")
        
        # メニュー情報を1つの文字列に結合
        menu_info = '\n'.join(menu_text)
        
        # プロンプトを個別の文字列として連結
        prompt = (
            "以下の給食メニューと食材から、1日分の栄養価を計算してください。\n"
            "高齢者向け給食の基準値を考慮して計算してください。\n\n"
        )
        
        # メニュー情報を追加
        prompt += menu_info + "\n\n"
        
        # 残りのプロンプトを追加
        prompt += (
            "計算の際の注意点：\n"
            "1. 各食材の栄養価を考慮\n"
            "2. 調理による栄養価の変化も考慮\n"
            "3. 高齢者向け給食の基準値を参考に\n\n"
            "以下の形式で出力してください：\n"
            "エネルギー: [数値]kcal\n"
            "タンパク質: [数値]g\n"
            "脂質: [数値]g\n"
            "炭水化物: [数値]g\n"
            "食物繊維: [数値]g\n"
            "カルシウム: [数値]mg\n"
            "鉄分: [数値]mg"
        )
        
        response = model.generate_content(prompt)
        return response.text.strip()
        
    except Exception as e:
        print(f"栄養価計算エラー: {str(e)}")
        return "栄養価計算エラー"

def format_menu_output(structured_data: dict) -> dict:
    """構造化データを出力形式に変換"""
    output = {
        '項目': [
            '栄養素',
            '朝食',
            '朝食：食材',
            '昼食 (主菜/副菜/汁物)',
            '昼食：食材/1人分/45人分',
            '夕食 (主菜/副菜/小鉢/汁物)',
            '夕食：食材/1人分/45人分'
        ],
        '3/1': [''] * 7
    }
    
    # 栄養素情報の生成
    output['3/1'][0] = calculate_nutrition_with_llm(structured_data['meals'], structured_data['ingredients'])
    
    # 朝食・昼食・夕食のメニューと食材を整形
    for meal_type, menu_idx, ingredients_idx in [
        ('朝食', 1, 2),
        ('昼食', 3, 4),
        ('夕食', 5, 6)
    ]:
        # メニュー名を収集
        menu_items = [
            meal['dish_name'] 
            for meal in structured_data['meals'] 
            if meal['meal_type'] == meal_type
        ]
        output['3/1'][menu_idx] = '\n'.join(menu_items)
        
        # 食材情報を整形
        ingredients_by_dish = {}
        for ing in structured_data['ingredients']:
            if ing['meal_type'] == meal_type:
                if ing['dish_name'] not in ingredients_by_dish:
                    ingredients_by_dish[ing['dish_name']] = []
                ingredients_by_dish[ing['dish_name']].append(
                    f"{ing['name']}: {ing['weight_per_person']}/{ing['total_weight']}"
                )
        
        # 食材情報を文字列に変換
        ingredients_text = []
        for dish, ingredients in ingredients_by_dish.items():
            ingredients_text.append(f"{dish}(\n" + '\n'.join(f"  {ing}" for ing in ingredients) + "\n)")
        output['3/1'][ingredients_idx] = '\n\n'.join(ingredients_text)
    
    return output

def process_excel_sheet(df: pd.DataFrame) -> dict:
    try:
        print("=== メニュー処理開始 ===")
        
        # データのクリーニングと前処理
        df = df.fillna('')
        df = df.astype(str)
        
        # 食事区分ごとのデータ収集
        current_section = None
        meals = {'朝食': [], '昼食': [], '夕食': []}
        ingredients = {'朝食': [], '昼食': [], '夕食': []}

        # 列のインデックス
        meal_type_col = 0  # A列 = 0
        menu_col = 1      # B列 = 1
        food_col = 3      # D列 = 3（食品名）
        weight_col = 4    # E列 = 4（重量）
        total_col = 5     # F列 = 5（総使用量）

        for idx, row in df.iterrows():
            meal_type = str(row.iloc[meal_type_col]).strip()
            menu_item = str(row.iloc[menu_col]).strip()
            food_item = str(row.iloc[food_col]).strip()
            weight = str(row.iloc[weight_col]).strip()
            total = str(row.iloc[total_col]).strip()

            # 合計行をスキップ
            if '合　計' in food_item or '合計' in food_item:
                continue

            # 食事区分の判定
            if '朝食' in meal_type:
                current_section = '朝食'
            elif '昼食' in meal_type:
                current_section = '昼食'
            elif '夕食' in meal_type:
                current_section = '夕食'

            if current_section:
                # メニュー項目の追加
                if menu_item and menu_item != 'nan':
                    if menu_item not in meals[current_section]:
                        meals[current_section].append(menu_item)

                # 食材情報の追加
                if food_item and food_item != 'nan' and weight and weight != 'nan':
                    # 食品番号と分類を除去して食材名のみを抽出
                    if ':' in food_item:
                        food_name = food_item.split(':')[1].strip()
                    else:
                        food_name = food_item

                    # 分類情報を除去
                    if '/' in food_name:
                        food_name = food_name.split('/')[0].strip()

                    # 末尾のgを除去
                    if food_name.endswith('g'):
                        food_name = food_name[:-1].strip()

                    # 重量から数値のみを抽出
                    weight_num = float(weight.replace('g', '').strip())
                    
                    # 45人分の総量を計算
                    total_weight = weight_num * 45

                    # 食材情報を整形
                    ingredient = f"{food_name}: {weight_num}g/{total_weight}g"
                    ingredients[current_section].append(ingredient)

        # 戻り値の構造を変更
        return {
            'meals': meals,
            'ingredients': ingredients,
            'data': [
                '',  # 栄養素（後で計算）
                '\n'.join(meals['朝食']),
                '\n'.join(ingredients['朝食']),
                '\n'.join(meals['昼食']),
                '\n'.join(ingredients['昼食']),
                '\n'.join(meals['夕食']),
                '\n'.join(ingredients['夕食'])
            ]
        }

    except Exception as e:
        print(f"\n!!! エラーが発生しました: {str(e)}")
        raise

def process_all_sheets(df_dict: dict) -> dict:
    """全シートのデータを処理して1つの辞書にまとめる"""
    try:
        print("=== 全シートの処理開始 ===")
        
        # 全日分のメニューと食材を収集
        all_meals = {}
        all_ingredients = {}
        
        # 基本データ構造の初期化
        combined_data = {
            '項目': [
                '栄養素',
                '朝食',
                '朝食：食材',
                '昼食 (主菜/副菜/汁物)',
                '昼食：食材/1人分/45人分',
                '夕食 (主菜/副菜/小鉢/汁物)',
                '夕食：食材/1人分/45人分'
            ]
        }

        # 各シートを処理
        for sheet_name, df in df_dict.items():
            try:
                # シート名から月と日を抽出
                match = re.search(r'(\d+)月(\d+)日', sheet_name)
                if match:
                    month = int(match.group(1))
                    day = int(match.group(2))
                    date_col = f"{month}/{day}"
                    
                    # シートのデータを処理
                    processed_data = process_excel_sheet(df)
                    
                    # メニューと食材を保存
                    all_meals[date_col] = processed_data['meals']
                    all_ingredients[date_col] = processed_data['ingredients']
                    
                    # 結果を結合データに追加
                    combined_data[date_col] = processed_data['data']
                    
            except Exception as e:
                print(f"シート '{sheet_name}' の処理中にエラーが発生: {str(e)}")
                continue

        # 全日分の栄養価を一括計算
        nutrition_by_date = calculate_nutrition_for_all_days(all_meals, all_ingredients)
        
        # 栄養価を各日付のデータに設定
        for date_col in all_meals.keys():
            if date_col in nutrition_by_date:
                combined_data[date_col][0] = nutrition_by_date[date_col]
        
        # デザートを一括で生成して追加
        add_desserts_to_combined_data(combined_data, all_meals)

        return combined_data

    except Exception as e:
        print(f"\n!!! 全シート処理でエラーが発生しました: {str(e)}")
        raise

def add_desserts_to_combined_data(combined_data: dict, all_meals: dict):
    """全日分のデータにデザートを一括で追加"""
    try:
        # バッチ処理用のメニューデータを準備
        batch_menu_data = []
        
        for date_col in [col for col in combined_data.keys() if col != '項目']:
            # 昼食と夕食のメニューを取得
            lunch_menu_idx = 3  # 昼食メニューのインデックス
            dinner_menu_idx = 5  # 夕食メニューのインデックス
            
            lunch_menu = combined_data[date_col][lunch_menu_idx]
            dinner_menu = combined_data[date_col][dinner_menu_idx]
            
            # バッチ処理用のデータに追加
            batch_menu_data.append({
                'date': date_col,
                'meal_type': '昼食',
                'menu_text': lunch_menu,
                'menu_idx': lunch_menu_idx,
                'ingredients_idx': lunch_menu_idx + 1
            })
            
            batch_menu_data.append({
                'date': date_col,
                'meal_type': '夕食',
                'menu_text': dinner_menu,
                'menu_idx': dinner_menu_idx,
                'ingredients_idx': dinner_menu_idx + 1
            })
        
        # バッチでデザートを生成
        print(f"デザートをバッチ処理で生成中... ({len(batch_menu_data)}件)")
        desserts = generate_desserts_batch(batch_menu_data)
        
        # 生成したデザートをデータに追加
        for i, menu_item in enumerate(batch_menu_data):
            if i < len(desserts):
                dessert_name, dessert_ingredients = desserts[i]
                date_col = menu_item['date']
                menu_idx = menu_item['menu_idx']
                ingredients_idx = menu_item['ingredients_idx']
                
                # デザートをメニューに追加
                combined_data[date_col][menu_idx] += f"\n\n【デザート】\n{dessert_name}"
                combined_data[date_col][ingredients_idx] += f"\n\n【デザート材料】\n{dessert_ingredients}"
        
        print(f"デザートの追加が完了しました。")
        
    except Exception as e:
        print(f"デザート追加エラー: {str(e)}")

def calculate_nutrition_for_all_days(all_meals: dict, all_ingredients: dict) -> dict:
    """全日分の栄養価を一括で計算"""
    try:
        # 日本食品標準成分表2020年版（八訂）のデータ
        nutrition_data = {
            # 主食
            '米': {'エネルギー': 342, 'タンパク質': 6.7, '脂質': 0.9, '炭水化物': 77.1, 'カルシウム': 8, '鉄分': 0.8},
            'パン': {'エネルギー': 264, 'タンパク質': 9.0, '脂質': 4.2, '炭水化物': 49.0, 'カルシウム': 35, '鉄分': 1.2},
            
            # 主菜
            '豚肉': {'エネルギー': 395, 'タンパク質': 19.0, '脂質': 35.0, '炭水化物': 0.0, 'カルシウム': 3, '鉄分': 0.8},
            '鶏肉': {'エネルギー': 200, 'タンパク質': 17.0, '脂質': 14.0, '炭水化物': 0.0, 'カルシウム': 5, '鉄分': 0.4},
            '魚': {'エネルギー': 130, 'タンパク質': 22.0, '脂質': 4.0, '炭水化物': 0.0, 'カルシウム': 40, '鉄分': 0.9},
            
            # 副菜（野菜類）
            '人参': {'エネルギー': 35, 'タンパク質': 0.7, '脂質': 0.2, '炭水化物': 8.2, 'カルシウム': 27, '鉄分': 0.3},
            '玉ねぎ': {'エネルギー': 33, 'タンパク質': 1.0, '脂質': 0.1, '炭水化物': 7.9, 'カルシウム': 23, '鉄分': 0.3},
            '大根': {'エネルギー': 15, 'タンパク質': 0.6, '脂質': 0.1, '炭水化物': 3.4, 'カルシウム': 16, '鉄分': 0.3},
            
            # 汁物の具材
            '味噌': {'エネルギー': 195, 'タンパク質': 12.6, '脂質': 6.3, '炭水化物': 25.5, 'カルシウム': 57, '鉄分': 2.6},
            '豆腐': {'エネルギー': 73, 'タンパク質': 6.6, '脂質': 4.2, '炭水化物': 2.0, 'カルシウム': 120, '鉄分': 1.2},
            'わかめ': {'エネルギー': 15, 'タンパク質': 2.0, '脂質': 0.2, '炭水化物': 3.0, 'カルシウム': 150, '鉄分': 1.5}
        }

        # 3食の基本栄養価（1日分）
        base_nutrition = {
            'エネルギー': 1800,  # kcal
            'タンパク質': 70,    # g
            '脂質': 50,         # g
            '炭水化物': 280,    # g
            'カルシウム': 600,  # mg
            '鉄分': 7          # mg
        }

        nutrition_by_date = {}
        
        for date, meals_dict in all_meals.items():
            # 基本栄養価をコピー
            total_nutrition = base_nutrition.copy()
            
            # 各食事の食材から栄養価を計算
            for meal_type in ['朝食', '昼食', '夕食']:
                ingredients_list = all_ingredients[date][meal_type]
                
                for ingredient_info in ingredients_list:
                    if ':' in ingredient_info:
                        food_name, amounts = ingredient_info.split(':')
                        food_name = food_name.strip()
                        
                        # 重量を抽出 (1人分)
                        weight_match = re.search(r'(\d+\.?\d*)g', amounts)
                        if weight_match:
                            weight = float(weight_match.group(1))
                            
                            # 食材の栄養価を加算
                            if food_name in nutrition_data:
                                for nutrient, value in nutrition_data[food_name].items():
                                    total_nutrition[nutrient] += value * weight / 100
            
            # 栄養価を整形して保存
            nutrition_text = (
                f"エネルギー: {int(total_nutrition['エネルギー'])}kcal\n"
                f"タンパク質: {int(total_nutrition['タンパク質'])}g\n"
                f"脂質: {int(total_nutrition['脂質'])}g\n"
                f"炭水化物: {int(total_nutrition['炭水化物'])}g\n"
                f"カルシウム: {int(total_nutrition['カルシウム'])}mg\n"
                f"鉄分: {int(total_nutrition['鉄分'])}mg"
            )
            
            nutrition_by_date[date] = nutrition_text
        
        return nutrition_by_date
        
    except Exception as e:
        print(f"栄養価計算エラー: {str(e)}")
        return {date: (
            "エネルギー: 1800kcal\n"
            "タンパク質: 70g\n"
            "脂質: 50g\n"
            "炭水化物: 280g\n"
            "カルシウム: 600mg\n"
            "鉄分: 7mg"
        ) for date in all_meals.keys()}

def update_menu_with_desserts(input_file: str, output_file: str):
    """メニューファイルを読み込み、デザートを追加して一時ファイルとして保存"""
    try:
        # 全シートを読み込む
        df_dict = pd.read_excel(input_file, sheet_name=None)
        
        # 全シートのデータを処理（デザート追加処理も含む）
        combined_menu_data = process_all_sheets(df_dict)
        
        # 一時ファイルのパスを生成
        temp_dir = Path(os.getenv('TEMP', '/tmp'))
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        temp_file = temp_dir / f'menu_with_desserts_{timestamp}.xlsx'
        
        # DataFrameを作成
        output_df = pd.DataFrame(combined_menu_data)
        
        # 列の順序を整理（日付順）
        date_cols = [col for col in output_df.columns if col != '項目']
        date_cols.sort(key=lambda x: tuple(map(int, x.split('/'))))
        ordered_cols = ['項目'] + date_cols
        
        output_df = output_df[ordered_cols]
        
        # ExcelWriterを使用してスタイルを適用
        with pd.ExcelWriter(temp_file, engine='xlsxwriter') as writer:
            # DataFrameをExcelに書き出し
            output_df.to_excel(writer, index=False, sheet_name='Sheet1')
            
            # ワークブックとワークシートを取得
            workbook = writer.book
            worksheet = writer.sheets['Sheet1']
            
            # フォーマットを設定
            cell_format = workbook.add_format({
                'font_size': 8,
                'font_name': 'MS Gothic',
                'text_wrap': True,
                'align': 'left',
                'valign': 'top'
            })
            
            # 列幅を自動調整
            for col_num, col in enumerate(output_df.columns):
                # 各セルの内容を改行で分割し、最大幅を計算
                max_width = 0
                for cell in output_df[col].astype(str):
                    # 改行で分割して各行の長さを確認
                    lines = cell.split('\n')
                    for line in lines:
                        # 全角文字は2文字分としてカウント
                        width = sum(2 if ord(c) > 127 else 1 for c in line)
                        max_width = max(max_width, width)
                
                # ヘッダーの幅も考慮
                header_width = sum(2 if ord(c) > 127 else 1 for c in str(col))
                max_width = max(max_width, header_width)
                
                # フォントサイズ8ptを考慮して幅を調整（0.9は微調整係数）
                column_width = max_width * 0.9
                
                # 最小幅と最大幅を設定
                column_width = max(10, min(column_width, 50))  # 10～50の範囲に制限
                
                worksheet.set_column(col_num, col_num, column_width)
            
            # 全セルに書式を適用
            for row in range(len(output_df) + 1):
                worksheet.set_row(row, None, cell_format)
        
        print(f'メニューを一時ファイルに保存しました: {temp_file}')
        
        # 一時ファイルを自動で開く
        if os.path.exists(temp_file):
            if os.name == 'posix':  # macOSまたはLinux
                subprocess.run(["open", str(temp_file)])
            elif os.name == 'nt':   # Windows
                subprocess.run(["start", str(temp_file)], shell=True)
        
    except Exception as e:
        print(f'エラーが発生しました: {str(e)}')
        raise 