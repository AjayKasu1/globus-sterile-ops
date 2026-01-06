import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

st.set_page_config(page_title="PO Management", page_icon="📝", layout="wide")

st.title("📝 Procurement & PO Management")

conn = sqlite3.connect("globus_sterile.db")
df = pd.read_sql("SELECT * FROM procurement", conn)
conn.close()

# Discrepancy Dashboard
discrepancies = df[df['Discrepancy_Flag'] == 1]
st.error(f"⚠️ {len(discrepancies)} Active Discrepancies Found!")

tab1, tab2 = st.tabs(["🔥 Critical/Discrepancies", "📋 All Orders"])

with tab1:
    st.markdown("### Action Required: Discrepant POs")
    st.markdown("Rules: Defective Units > 0 OR Status != Delivered (if past due)")
    
    if not discrepancies.empty:
        st.dataframe(
            discrepancies[['PO_ID', 'Supplier', 'Order_Date', 'Item_Category', 'Defective_Units', 'Order_Status', 'Compliance']]
            .style.applymap(lambda x: 'background-color: #ffcccc' if x > 0 else '', subset=['Defective_Units']),
            use_container_width=True
        )
        
        # Vendor Analysis for Issues
        st.subheader("Worst Offenders (By Defective Units)")
        vendor_issues = discrepancies.groupby('Supplier')['Defective_Units'].sum().reset_index().sort_values('Defective_Units', ascending=False)
        fig_bar = px.bar(vendor_issues.head(10), x='Supplier', y='Defective_Units', 
                         title="Top Suppliers with Quality Issues", color='Defective_Units', color_continuous_scale='Reds')
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.success("No discrepancies found. Good job!")

with tab2:
    st.markdown("### Full PO History")
    st.dataframe(df, use_container_width=True)
