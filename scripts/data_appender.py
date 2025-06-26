import pandas as pd
from scripts.config_loader import load_config

def append_and_deduplicate(df_master, df_new):
    config = load_config()
    dedup_enabled = config['deduplication']['enabled']
    dedup_columns = config['deduplication']['columns']

    # combine master and new data
    df_combined = pd.concat([df_master, df_new], ignore_index=True)
    print(f"Combined data rows: {len(df_combined)}")

    if dedup_enabled and dedup_columns:
        before_dedup = len(df_combined)
        df_combined = df_combined.drop_duplicates(subset=dedup_columns)
        after_dedup = len(df_combined)
        print(f"Deduplication applied. Removed {before_dedup - after_dedup} duplicates.")

    else:
        print("Deduplication skipped (disabled or no columns specified).")

    return df_combined

def save_updated_master(df_combined):
    config = load_config()
    output_path = config['output_file']

    try:
        df_combined.to_excel(output_path, index=False, engine='openpyxl')
        print(f"Updated master data saved to: {output_path}")
    except Exception as e:
        print(f"❌ Failed to save updated master data: {e}")

# test
if __name__ == "__main__":
    from scripts.master_loader import load_master_data
    from scripts.daily_loader import load_daily_data

    df_master = load_master_data()
    df_new = load_daily_data()

    if df_master is not None and df_new is not None:
        df_combined = append_and_deduplicate(df_master, df_new)
        save_updated_master(df_combined)
