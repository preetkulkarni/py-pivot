import os
import pandas as pd
from datetime import datetime
from scripts.config_loader import load_config

def get_latest_file(path):
    # get recent excel file
    excel_files = [
        os.path.join(path, f)
        for f in os.listdir(path)
        if f.endswith(".xlsx") or f.endswith(".xls")
    ]

    if not excel_files:
        print("No Excel files found in dump folder.")
        return None
    
    latest_file = max(excel_files, key=os.path.getmtime)
    return latest_file

def load_daily_data():
    config = load_config()
    daily_folder = config['daily_data_folder']

    if not os.path.exists(daily_folder):
        print("Daily dump dolder not found: {daily_folder}")
        return None
    
    latest_file = get_latest_file(daily_folder)

    if not latest_file:
        return None
    
    try:
        df_daily = pd.read_excel(latest_file, engine='openpyxl')
        print(f"Load daily file: {os.path.basename(latest_file)} with {len(df_daily)} rows.")
        return df_daily
    except Exception as e:
        print(f"Failed to read daily file: {e}")
        return None
    

# test
if __name__ == "__main__":
    df = load_daily_data()
    if df is not None:
        print(df.head())