import numpy as np
import pandas as pd

# -------------------------
# 1️⃣ Herfindahl-Hirschman Index (HHI)
# -------------------------
def calculate_hhi(df):
    donor_totals = df.groupby("donor")["amount"].sum()
    total = donor_totals.sum()
    
    if total == 0:
        return 0
    
    shares = donor_totals / total
    hhi = (shares ** 2).sum()
    return round(hhi, 4)


# -------------------------
# 2️⃣ Spending Spike Detection (Z-score)
# -------------------------
def detect_spike(df):
    daily_spending = df.groupby("date")["amount"].sum()
    
    if len(daily_spending) < 2:
        return 0
    
    mean = daily_spending.mean()
    std = daily_spending.std()
    
    if std == 0:
        return 0
    
    latest_value = daily_spending.iloc[-1]
    z_score = (latest_value - mean) / std
    
    return round(z_score, 2)


# -------------------------
# 3️⃣ Risk Classification
# -------------------------
def classify_risk(hhi, z_score):
    risk_score = 0
    
    # Concentration risk
    if hhi > 0.25:
        risk_score += 1
    
    # Spike risk
    if abs(z_score) > 2:
        risk_score += 1
    
    if risk_score == 0:
        return "Low"
    elif risk_score == 1:
        return "Medium"
    else:
        return "High"