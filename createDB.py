import pandas as pd
import sqlite3
import os

try:
    csv_path = os.path.join(os.path.dirname(__file__), "..", "data", "prediction.csv")
    df = pd.read_csv(csv_path)
    
    conn = sqlite3.connect("churn.db")
    
    try:
        df.to_sql("customers", conn, if_exists="replace", index=False)
        print("Database Ready")
    except Exception as e:
        print(f"Error inserting data into database: {e}")
    finally:
        conn.close()
        print("Database connection closed")
        
except FileNotFoundError:
    print(f"Error: CSV file not found at path: {csv_path}")
except Exception as e:
    print(f"Error: {e}")
