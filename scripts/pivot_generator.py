import os
import yaml
import pandas as pd
from datetime import datetime
from scripts.config_loader import load_config

EXPORT_FOLDER = "exports"
CONFIG_PATH = "config/config.yaml"


def generate_pivot(df, index_cols, columns=None, values=None, aggfunc='sum', filters=None):
    """
    Generates a pivot table from the given DataFrame with optional filtering.
    """
    df_filtered = df.copy()

    # apply filters
    if filters:
        for col, val in filters.items():
            if col not in df_filtered.columns:
                print(f"⚠️ Skipping filter: Column '{col}' not found.")
                continue
            df_filtered = df_filtered[df_filtered[col] == val]

    # generate actual pivot
    pivot_df = pd.pivot_table(
        df_filtered,
        index=index_cols,
        columns=columns if columns else None,
        values=values if values else None,
        aggfunc=aggfunc,
        fill_value=0
    )

    return pivot_df


def export_pivot_to_excel(pivot_df):
    """
    Exports the pivot table to an Excel file in the exports folder.
    """
    if not os.path.exists(EXPORT_FOLDER):
        os.makedirs(EXPORT_FOLDER)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"pivot_{timestamp}.xlsx"
    export_path = os.path.join(EXPORT_FOLDER, filename)

    pivot_df.to_excel(export_path, engine="openpyxl")
    print(f"✅ Pivot table exported to: {export_path}")


def list_presets(config):
    """
    Lists saved pivot presets from config.
    """
    presets = config.get("pivot_presets", {})
    if not presets:
        print("\n⚠️ No presets found.")
    else:
        print("\n=== Saved Pivot Presets ===")
        for idx, preset_name in enumerate(presets, start=1):
            print(f"{idx}. {preset_name}")


def use_preset(df, preset_name, config):
    """
    Applies a saved preset to generate a pivot table.
    """
    presets = config.get("pivot_presets", {})
    preset = presets.get(preset_name)

    if not preset:
        print(f"❌ Preset '{preset_name}' not found.")
        return

    print(f"\n✅ Generating Pivot: {preset_name}\n")

    try:
        pivot = generate_pivot(
            df,
            index_cols=preset.get("index_cols"),
            columns=preset.get("columns") or None,
            values=preset.get("values") or None,
            aggfunc=preset.get("aggfunc", "sum"),
            filters=preset.get("filters")
        )

        print(pivot)

        export_choice = input("\n💾 Export this pivot to Excel? (y/n): ").strip().lower()
        if export_choice == "y":
            export_pivot_to_excel(pivot)

    except Exception as e:
        print(f"❌ Error generating pivot: {e}")


def save_config(config):
    """
    Saves the updated config to file.
    """
    with open(CONFIG_PATH, "w") as file:
        yaml.dump(config, file)
    print(f"✅ Preset saved to {CONFIG_PATH}")


def create_new_preset(df, config):
    """
    Interactive prompt to create a new pivot preset with column validation.
    """
    print("\n=== Create New Pivot Preset ===")
    print("Available columns:")
    print(df.columns.tolist())

    preset_name = input("📝 Preset name (no spaces): ").strip()

    while True:
        index_cols = input("📝 Rows (index columns, comma-separated): ").strip().split(",")
        index_cols = [col.strip() for col in index_cols if col.strip()]
        if all(col in df.columns for col in index_cols):
            break
        else:
            print("❌ Invalid columns. Please try again.")

    while True:
        columns = input("📝 Columns (optional, single column): ").strip()
        if not columns or columns in df.columns:
            break
        else:
            print("❌ Column not found. Please try again.")

    while True:
        values = input("📝 Values (data to aggregate, optional): ").strip()
        if not values or values in df.columns:
            break
        else:
            print("❌ Column not found. Please try again.")

    print("\nSupported aggregation functions: sum, count, mean, max, min")
    aggfunc = input("📝 Aggregation function [default=sum]: ").strip().lower()
    aggfunc = aggfunc if aggfunc else "sum"

    print("\nOptional filters (key=value), separate multiple with commas.")
    raw_filters = input("📝 Filters: ").strip()
    filters = {}
    if raw_filters:
        for pair in raw_filters.split(","):
            if "=" in pair:
                key, val = pair.split("=", 1)
                key = key.strip()
                val = val.strip()
                if key in df.columns:
                    filters[key] = val
                else:
                    print(f"⚠️ Skipping invalid filter column: {key}")

    if "pivot_presets" not in config:
        config["pivot_presets"] = {}

    config["pivot_presets"][preset_name] = {
        "index_cols": index_cols,
        "columns": columns,
        "values": values,
        "aggfunc": aggfunc,
        "filters": filters
    }

    save_config(config)
    print(f"✅ Preset '{preset_name}' added.")


def interactive_pivot(df):
    """
    Fully interactive prompt to generate a custom pivot table.
    """
    print("\n=== 📊 Pivot Table Generator ===")
    print("Available columns:")
    print(df.columns.tolist())
    print("Leave optional fields blank to skip them.")

    while True:
        index_cols = input("📝 Rows (index columns, comma-separated): ").strip().split(",")
        index_cols = [col.strip() for col in index_cols if col.strip()]
        if all(col in df.columns for col in index_cols):
            break
        else:
            print("❌ Invalid columns. Please try again.")

    while True:
        columns = input("📝 Columns (optional, single column): ").strip()
        if not columns or columns in df.columns:
            break
        else:
            print("❌ Column not found. Please try again.")

    while True:
        values = input("📝 Values (data to aggregate, optional): ").strip()
        if not values or values in df.columns:
            break
        else:
            print("❌ Column not found. Please try again.")

    print("\nSupported aggregation functions: sum, count, mean, max, min")
    aggfunc = input("📝 Aggregation function [default=sum]: ").strip().lower()
    aggfunc = aggfunc if aggfunc else "sum"

    print("\nOptional filters (key=value), separate multiple with commas.")
    raw_filters = input("📝 Filters: ").strip()
    filters = {}
    if raw_filters:
        for pair in raw_filters.split(","):
            if "=" in pair:
                key, val = pair.split("=", 1)
                key = key.strip()
                val = val.strip()
                if key in df.columns:
                    filters[key] = val
                else:
                    print(f"⚠️ Skipping invalid filter column: {key}")

    try:
        pivot = generate_pivot(df, index_cols, columns, values, aggfunc, filters)
        print("\n✅ Generated Pivot Table:\n")
        print(pivot)

        export_choice = input("\n💾 Export this pivot to Excel? (y/n): ").strip().lower()
        if export_choice == "y":
            export_pivot_to_excel(pivot)

    except Exception as e:
        print(f"❌ Error generating pivot table: {e}")


# === Main Interactive Menu ===
if __name__ == "__main__":
    from scripts.master_loader import load_master_data
    from scripts.daily_loader import load_daily_data
    from scripts.data_appender import append_and_deduplicate

    config = load_config()

    df_master = load_master_data()
    df_new = load_daily_data()

    if df_master is not None and df_new is not None:
        df_combined = append_and_deduplicate(df_master, df_new)
        print(f"\nTotal rows after append: {len(df_combined)}")

        while True:
            print("\n=== Pivot Table Menu ===")
            print("1. Generate Pivot Table (interactive)")
            print("2. Use Pivot Preset")
            print("3. Create New Preset")
            print("4. Exit")

            choice = input("Select an option: ").strip()

            if choice == "1":
                interactive_pivot(df_combined)
            elif choice == "2":
                list_presets(config)
                preset_name = input("Enter preset name: ").strip()
                use_preset(df_combined, preset_name, config)
            elif choice == "3":
                create_new_preset(df_combined, config)
            elif choice == "4":
                print("Exiting...")
                break
            else:
                print("❌ Invalid choice. Please try again.")
