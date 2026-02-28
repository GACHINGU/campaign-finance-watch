import pandas as pd

def load_data():
    df = pd.read_csv("data/sample_data.csv")
    
    # Ensure proper types
    df["date"] = pd.to_datetime(df["date"])
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0)
    
    return df