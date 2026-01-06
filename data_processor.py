import pandas as pd
import sqlite3
import os
from datetime import datetime
import numpy as np

# --- Configuration ---
DB_PATH = "globus_sterile.db"
REPORTS_DIR = "reports"
FILES = {
    "inventory": "Dataset/Medical Spare Parts/KL HKL - Spare Part Inventories.xlsx",
    "procurement": "Dataset/Procurement KPI/Procurement KPI Analysis Dataset.csv",
    "production": "Dataset/Production:Batch Scheduling/hybrid_manufacturing_categorical.csv"
}

# --- 1. Load Data ---
def load_data():
    print("Loading data...")
    try:
        inventory = pd.read_excel(FILES["inventory"])
        procurement = pd.read_csv(FILES["procurement"])
        production = pd.read_csv(FILES["production"])
        return inventory, procurement, production
    except Exception as e:
        print(f"Error loading data: {e}")
        return None, None, None

# --- 2. Transform Data ---
def transform_data(inventory, procurement, production):
    print("Transforming data...")

    # --- INVENTORY ---
    # Col mapping: 'Part No.' -> Part_ID, 'Current Stock Level' -> Stock_Quantity, 'Brand' -> Supplier
    inventory = inventory.rename(columns={
        'Part No.': 'Part_ID',
        'Part Description': 'Description',
        'Current Stock Level': 'Stock_Quantity',
        'Brand': 'Supplier',
        'Model': 'Category',
        'Location': 'Bin_Location',
        'Minimum Price Per Nos (RM)': 'Unit_Cost'
    })
    # Fill NaN
    inventory['Stock_Quantity'] = pd.to_numeric(inventory['Stock_Quantity'], errors='coerce').fillna(0)
    inventory['Unit_Cost'] = pd.to_numeric(inventory['Unit_Cost'], errors='coerce').fillna(0)
    
    # Calculate Value and Reorder Point
    inventory['Total_Value'] = inventory['Stock_Quantity'] * inventory['Unit_Cost']
    inventory['Reorder_Point'] = (inventory['Stock_Quantity'] * 0.3).astype(int) # Simple logic
    inventory['Reorder_Status'] = np.where(inventory['Stock_Quantity'] <= inventory['Reorder_Point'], 'Reorder Now', 'OK')

    # --- PROCUREMENT ---
    # PO_ID, Supplier, Order_Date, Delivery_Date, Order_Status, Defective_Units, Compliance
    procurement['Order_Date'] = pd.to_datetime(procurement['Order_Date'], errors='coerce')
    procurement['Delivery_Date'] = pd.to_datetime(procurement['Delivery_Date'], errors='coerce')
    
    # Discrepancy Logic
    procurement['Discrepancy_Flag'] = (procurement['Defective_Units'] > 0) | (procurement['Order_Status'] != 'Delivered')
    procurement['Days_To_Deliver'] = (procurement['Delivery_Date'] - procurement['Order_Date']).dt.days

    # --- PRODUCTION ---
    # Map Operation Steps
    op_map = {
        'Grinding': 'Cleaning',
        'Lathe': 'Packing',
        'Milling': 'Sterilization',
        'Drilling': 'Inspection',
        'Additive': 'Release',
        'Quality Control': 'QC' # Just in case
    }
    production['WIP_Step'] = production['Operation_Type'].map(op_map).fillna(production['Operation_Type'])

    # Dates
    date_cols = ['Scheduled_Start', 'Scheduled_End', 'Actual_Start', 'Actual_End']
    for col in date_cols:
        production[col] = pd.to_datetime(production[col], errors='coerce')
    
    # Delay Calculation (Hours)
    production['Delay_Hours'] = (production['Actual_End'] - production['Scheduled_End']).dt.total_seconds() / 3600
    production['Delay_Status'] = np.where(production['Delay_Hours'] > 0, 'Delayed', 'On Time')

    # Simulate Linking Production to Inventory (Part_ID)
    # We don't have a direct link, so we'll assign random Part_IDs from inventory to Jobs for the demo
    if 'Part_ID' in inventory.columns and not inventory.empty:
        part_ids = inventory['Part_ID'].unique()
        production['Part_ID'] = np.random.choice(part_ids, size=len(production))
    else:
        production['Part_ID'] = 'UNKNOWN'

    return inventory, procurement, production

# --- 3. Save to SQLite ---
def save_to_db(inventory, procurement, production):
    print(f"Saving to {DB_PATH}...")
    conn = sqlite3.connect(DB_PATH)
    
    inventory.to_sql('inventory', conn, if_exists='replace', index=False)
    procurement.to_sql('procurement', conn, if_exists='replace', index=False)
    production.to_sql('production', conn, if_exists='replace', index=False)
    
    conn.close()
    print("Database saved.")

# --- 4. Generate Reports ---
def generate_reports(inventory, procurement, production):
    print("Generating Excel reports...")
    if not os.path.exists(REPORTS_DIR):
        os.makedirs(REPORTS_DIR)

    # 1. Production Schedule
    with pd.ExcelWriter(f"{REPORTS_DIR}/Production_Schedule.xlsx", engine='xlsxwriter') as writer:
        sched = production[['Job_ID', 'Part_ID', 'WIP_Step', 'Scheduled_Start', 'Scheduled_End', 'Delay_Status']]
        sched.to_excel(writer, sheet_name='Schedule', index=False)
        # Recommendations (Simulated)
        recs = production[production['Job_Status'] == 'Pending'].head(20)
        recs.to_excel(writer, sheet_name='Batch_Recommendations', index=False)

    # 2. Lot Status Tracker
    with pd.ExcelWriter(f"{REPORTS_DIR}/Lot_Status_Tracker.xlsx", engine='xlsxwriter') as writer:
        lot_status = production[['Job_ID', 'Part_ID', 'WIP_Step', 'Job_Status', 'Delay_Hours']]
        lot_status.sort_values(['Job_ID', 'WIP_Step']).to_excel(writer, sheet_name='Lot_Tracker', index=False)

    # 3. PO Discrepancies
    with pd.ExcelWriter(f"{REPORTS_DIR}/PO_Discrepancies.xlsx", engine='xlsxwriter') as writer:
        issues = procurement[procurement['Discrepancy_Flag'] == True]
        issues.to_excel(writer, sheet_name='Discrepancies', index=False)
        # Work Schedule (Top 10 urgents)
        issues.head(10).to_excel(writer, sheet_name='Work_Queue', index=False)

    # 4. Inventory Master
    with pd.ExcelWriter(f"{REPORTS_DIR}/Inventory_Master.xlsx", engine='xlsxwriter') as writer:
        inv_view = inventory[['Part_ID', 'Description', 'Category', 'Stock_Quantity', 'Reorder_Point', 'Reorder_Status', 'Total_Value']]
        inv_view.to_excel(writer, sheet_name='Master_List', index=False)
        # Low Stock
        low_stock = inv_view[inv_view['Stock_Quantity'] <= inv_view['Reorder_Point']]
        low_stock.to_excel(writer, sheet_name='Reorder_List', index=False)

    # 5. Compliance Report
    with pd.ExcelWriter(f"{REPORTS_DIR}/Compliance_Report.xlsx", engine='xlsxwriter') as writer:
        non_compliant = procurement[procurement['Compliance'] == 'No']
        non_compliant.to_excel(writer, sheet_name='Non_Compliant_POs', index=False)
        # Failed Jobs (Quarantine)
        failed_jobs = production[production['Job_Status'] == 'Failed']
        failed_jobs.to_excel(writer, sheet_name='Quarantined_Lots', index=False)

    print(f"Reports generated in {REPORTS_DIR}/")

def main():
    inv, proc, prod = load_data()
    if inv is not None:
        inv, proc, prod = transform_data(inv, proc, prod)
        save_to_db(inv, proc, prod)
        generate_reports(inv, proc, prod)
        print("Data processing complete! Ready for Streamlit.")

if __name__ == "__main__":
    main()
