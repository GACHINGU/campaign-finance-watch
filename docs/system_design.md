# System Design – Campaign Finance Watch Tool

## Overview

The Campaign Finance Watch Tool is designed to monitor political financing in Kenya by combining data analysis, risk monitoring, and interactive visualizations.  
It follows a **modular design** to ensure clarity, maintainability, and scalability.

---

## Architecture

[Data Source: CSV / APIs]
│
▼
utils/data_loader.py
│
▼
utils/risk_engine.py
├─ calculate_hhi()
├─ detect_spike()
└─ classify_risk()
│
▼
app/main.py (Streamlit Dashboard)
├─ Sidebar Filters (Party, Region, Date, Donor)
├─ KPIs
├─ Risk Monitoring Panel
├─ Spending Over Time
├─ Donor & Party Visualizations
└─ Download Risk Report


---

## Modules

- **Data Loader (`utils/data_loader.py`)**  
  Loads CSV data and preprocesses for dashboard use.

- **Risk Engine (`utils/risk_engine.py`)**  
  Performs risk calculations:
  - **HHI:** Donor concentration  
  - **Z-score:** Detects abnormal spending spikes  
  - **Risk classification:** Combines HHI + Z-score  

- **Dashboard (`app/main.py`)**  
  Interactive Streamlit interface showing KPIs, risk metrics, and visualizations.  
  Dynamic filters allow users to explore by party, region, date, and donor.

- **Components (Optional for modular builds)**  
  - `charts.py` → chart functions  
  - `metrics.py` → KPI functions  
  - `filters.py` → sidebar filters

---

## Data Flow

1. **Data Loading:** CSV data is loaded into a Pandas DataFrame.  
2. **Filtering:** Sidebar filters narrow down data (Party, Region, Date, Donor).  
3. **Risk Analysis:** HHI and Z-score are computed on filtered data.  
4. **Visualization:** Interactive Plotly charts display trends, top donors, anomalies, and party comparisons.  
5. **Output:** Downloadable risk report summarizing key metrics.

---

## Scalability

- Additional data sources (e.g., APIs, government datasets) can be integrated easily.  
- New metrics and analytics (e.g., monthly averages, donor trends) can be added without restructuring the dashboard.  
- Modular components allow separate development of charts, KPIs, and risk computations.

