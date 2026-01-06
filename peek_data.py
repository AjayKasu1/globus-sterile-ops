import pandas as pd
import os

base_dir = "Dataset"
files = {
    "inventory": "Medical Spare Parts/KL HKL - Spare Part Inventories.xlsx",
    "procurement": "Procurement KPI/Procurement KPI Analysis Dataset.csv",
    "production": "Production:Batch Scheduling/hybrid_manufacturing_categorical.csv"
}

for key, path in files.items():
    full_path = os.path.join(base_dir, path)
    print(f"--- {key.upper()} ({path}) ---")
    try:
        if path.endswith('.csv'):
            df = pd.read_csv(full_path, nrows=2)
        else:
            df = pd.read_excel(full_path, nrows=2)
        print(df.columns.tolist())
        print(df.head(2))
    except Exception as e:
        print(f"Error reading {path}: {e}")
    print("\n")
