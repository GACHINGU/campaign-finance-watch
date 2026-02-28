# Methodology – Campaign Finance Watch Tool

## Objective

To identify risks in political financing, monitor donor concentration, detect spending spikes, and ensure transparency in political campaigns.

---

## Step 1 – Data Preprocessing

- Data is loaded from `data/sample_data.csv`.  
- Columns include: `party`, `region`, `donor`, `date`, `amount`.  
- Filters applied dynamically:
  - Party  
  - Region  
  - Date Range  
  - Donor  

---

## Step 2 – Risk Analysis

### 2.1 HHI (Herfindahl-Hirschman Index)

- Measures donor concentration per party.  
- Formula:  

\[
HHI = \sum_{i=1}^{N} s_i^2
\]

Where \(s_i\) = share of total donations contributed by donor i.  

- Interpretation:
  - Low HHI → funds evenly distributed  
  - High HHI → few donors dominate  

### 2.2 Z-score (Spending Spike Detection)

- Calculates normalized deviation of daily/periodic spending:

\[
Z = \frac{x - \mu}{\sigma}
\]

Where:
- \(x\) = spending on a given date  
- \(\mu\) = mean spending  
- \(\sigma\) = standard deviation  

- |Z| > 2 → anomaly detected  

### 2.3 Risk Classification

- Combines HHI and Z-score into **Low / Medium / High** risk.  
- Example logic:
  - Low HHI + no spikes → Low risk  
  - High HHI or spike detected → Medium/High risk  

---

## Step 3 – Visualization

- **Spending Trends:** Line chart with anomalies in red.  
- **Top Donors & Donor Share:** Bar & pie charts for donor concentration.  
- **Party Funding Comparison:** Bar chart by party totals.  
- **Party-level Risk Table:** Shows risk per party dynamically.  

---

## Step 4 – Output

- **Downloadable Risk Report:**  
  - Summarizes HHI, Z-score, overall risk, and interpretation.  
- **Interactive dashboard:**  
  - Users can filter and explore trends in real time.

---

## References

- [Transparency International – Political Finance Guide](https://knowledgehub.transparency.org/guide/topic-guide-on-political-finance/5186)  
- [OECD Recommendation on Public Integrity](https://www.idea.int/sites/default/files/publications/political-finance-reforms.pdf)  
- [Open Government Partnership – Political Finance](https://www.opengovpartnership.org/policy-area/political-finance/)
