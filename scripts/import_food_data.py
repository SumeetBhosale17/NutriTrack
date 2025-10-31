import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
from sqlalchemy import create_engine
from config import Config

file_path = "data/Anuvaad_INDB_2024.11.xlsx"

df = pd.read_excel(file_path)

columns_to_keep = [
    'food_code', 'food_name', 'energy_kcal', 'protein_g', 'carb_g', 'fat_g',
    'fibre_g', 'iron_mg', 'calcium_mg', 'vitc_mg', 'sodium_mg', 'potassium_mg'
]

df = df[columns_to_keep]

df.columns = [c.strip().lower() for c in df.columns]

df.fillna(0, inplace=True)

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)

df.to_sql("indian_foods", engine, if_exists="replace", index=False)

print('Dataset imported successfully')