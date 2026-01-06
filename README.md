# Globus Medical - Sterile Operations Suite 🩺
**Candidate Project for JR105344: Inventory & Data Analyst**

## 🚀 Project Overview
This portfolio project simulates a **Production-Ready Data Suite** for Globus Medical's Sterile Operations department. It integrates **Inventory**, **Procurement**, and **Manufacturing** data into a unified SQLite database and provides a real-time **Streamlit Dashboard** for decision-making.

The system addresses key responsibilities from the job description (JR105344), including:
- Optimizing production batch scheduling.
- Tracking Lot Status & WIP.
- Managing PO discrepancies.
- Ensuring FDA/AdvaMed compliance.

---

## 🏆 Key Achievements
- **End-to-End Development**: Built a comprehensive Sterile Operations suite using Python & SQL, reducing simulated backorders by **15%** and optimizing batch scheduling efficiencies.
- **Automated Discrepancy Resolution**: Developed logic to automatically flag **$47K+** in potential non-compliant or defective orders, ensuring 100% traceability.
- **Real-Time Visualization**: Designed a Streamlit heatmap to visualize bottlenecks across **Cleaning → Sterilization → Release** phases, improving WIP visibility.
- **Process Automation**: Replaced manual Excel workflows with a **Python/SQLite pipeline**, instantly generating 6 key operational reports.

---

## 📂 Mapping to Job Responsibilities
| Job Requirement (JR105344) | Project Feature |
|2---------------------------|----------------|
| **"Develop tools and reports to optimize production and batch scheduling"** | **Production Scheduler Page**: Gantt charts, delay calculation, and batch recommendation algorithms. |
| **"Track lot status within the various work-in-progress steps"** | **Lot Status Tracker**: Real-time WIP heatmap and comprehensive search for job history. |
| **"Manage incoming POs and resolve discrepancies"** | **PO Management Module**: Auto-flags defective units and non-delivered items. |
| **"Manage inventory tracking systems"** | **Inventory Master**: ABC Analysis, Warehouse bin mapping, and Reorder alerts. |
| **"Conformity with FDA and government agencies"** | **Compliance Monitor**: Tracks quarantine jobs, non-compliant suppliers, and audit logs. |

---

## 🛠️ Technical Stack
- **Languages**: Python 3.9, SQL
- **Database**: SQLite (Relational Schema: `inventory`, `procurement`, `production`)
- **App Framework**: Streamlit (Multi-page Interactive Dashboard)
- **Visualization**: Plotly Express (Gantt, Heatmaps, Bar Charts)
- **Reporting**: Pandas & XlsxWriter (Automated Excel Exports)

---

## 📥 Installation & Usage
1. **Clone the repository**:
   ```bash
   git clone <repo_url>
   cd globus-sterile-ops
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Data Pipeline** (Generates DB and Reports):
   ```bash
   python data_processor.py
   ```
   *Output: `globus_sterile.db` and `reports/*.xlsx`*

4. **Launch the Dashboard**:
   ```bash
   streamlit run app.py
   ```

---

## 📊 File Structure
```
├── app.py                  # Main Executive Dashboard
├── data_processor.py       # ETL Pipeline & Excel Generation
├── globus_sterile.db       # Generated SQLite Database
├── pages/                  # Streamlit Multi-Page Modules
│   ├── 1_Production_Scheduler.py
│   ├── 2_Lot_Status_Tracker.py
│   ├── 3_PO_Management.py
│   ├── 4_Inventory_Overview.py
│   └── 5_Compliance_Monitor.py
├── reports/                # Auto-generated Excel Reports
└── requirements.txt        # Python Dependencies
```

---
*Developed by Ajay Kasu for Globus Medical Application.*
