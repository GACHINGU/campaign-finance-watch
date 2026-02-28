# Campaign Finance Watch Tool

**Build Tech. Expose Illicit Money. Protect Democracy.**

---

##  Project Overview

The **Campaign Finance Watch Tool** is an interactive dashboard designed to monitor political financing in Kenya.  
It enables transparency, tracks donor contributions, detects abnormal spending patterns, and assesses risk, supporting accountability ahead of the 2027 elections.  

This tool demonstrates how **tech and data** can strengthen anti-corruption frameworks and ensure fair political processes.

---

##  Key Features

- **Interactive Sidebar Filters:** Party, Region, Date Range, Donor  
- **KPIs:** Total Spending, Unique Donors  
- **Risk Monitoring Panel:** HHI (donor concentration), Spending Spike (Z-score), Overall Risk Level  
- **Party-level Risk Table:** Shows risk indicators for each party  
- **Spending Over Time:** Line chart with anomalies highlighted  
- **Top Donors & Donor Contribution Share:** Bar and pie charts  
- **Party Funding Comparison:** Bar chart per party  
- **Downloadable Risk Report:** Export risk summary for oversight purposes  

---

##  Methodology

1. **Data Handling:**  
   - Data is loaded from CSV (`data/sample_data.csv`) and filtered dynamically based on user inputs.
2. **Risk Analysis:**  
   - **HHI (Herfindahl-Hirschman Index):** Measures donor concentration per party.  
   - **Z-score:** Detects abnormal spending spikes over time.  
   - **Risk Classification:** Combines HHI and Z-score into a simple risk level (Low, Medium, High).  
3. **Visualization:**  
   - Interactive charts built using **Plotly** for dynamic exploration of trends, anomalies, and donor distribution.

---

## 🛠 Technology Stack

- **Python 3.11+**  
- **Streamlit:** Dashboard & interactivity  
- **Pandas:** Data manipulation  
- **Plotly:** Interactive charts  
- **NumPy:** Statistical calculations  

---

##  Project Structure

campaign-finance-watch/
│
├── README.md
├── requirements.txt
├── .gitignore
├── data/
├── app/
├── notebooks/
└── docs/


- `app/` → Dashboard code, components, and utilities  
- `data/` → Sample and processed datasets  
- `notebooks/` → Exploratory and anomaly detection analysis  
- `docs/` → System design & methodology documentation  

---

##  How to Run

1. Clone the repository:
```bash
git clone https://github.com/yourusername/campaign-finance-watch.git

2. pip install -r requirements.txt
3. streamlit run app/main.py

Team & Hackathon Info

- Team: Sigma Group

- Hackathon: Campaign Finance Watch Tool Hackathon 2026

- Objective: Enhance transparency and accountability in political financing in Kenya.

References:

- Political Finance Topic Guide – Transparency International

- OECD Recommendation on Public Integrity

- Open Government Partnership – Political Finance