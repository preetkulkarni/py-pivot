import pandas as pd
import os
from scripts.config_loader import load_config

def load_master_data():
    config = load_config()
    master_path = config['master_file']
    sheet_name = config.get('sheet_name', 0) # first sheet default

    #check if file exists
    if not os.path.exists(master_path):
        print(f"Master file not found at: {master_path}.")
        return None
    
    try:
        df_master = pd.read_excel(master_path, sheet_name=sheet_name, engine='openpyxl')
        print(f"Loaded master file with {len(df_master)} rows.")
        return df_master
    except Exception as e:
        print(f"Failed to load Excel file: {e}")
        return None
    

# test
if __name__ == "__main__":
    df = load_master_data()
    if df is not None:
        print(df.head())