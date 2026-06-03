import os
import sqlite3
from google import genai
import pandas as pd

# Initialize client with new SDK
client = genai.Client(api_key=os.environ.get("AIzaSyAnTzcVO0f2z3ESHZEEMczdBUIwMYVMlnE"))

conn = sqlite3.connect("churn.db")

try:
    cursor = conn.cursor()

    question = input("Ask about churn: ")

    if not question.strip():
        print("Error: Question cannot be empty")
    else:
        cursor.execute("SELECT * FROM customers LIMIT 50")
        columns = [description[0] for description in cursor.description]
        rows = cursor.fetchall()

        df = pd.DataFrame(rows, columns=columns)

        cursor.execute("PRAGMA table_info(customers)")
        schema = cursor.fetchall()

        prompt = f"""
You are a data analyst specializing in customer churn analysis.

Table schema:
{schema}

Customer data sample (first 50 rows):
{df.to_string(index=False)}

Answer this question based on the data above:
{question}
"""

        try:
            # New SDK uses client.models.generate_content()
            response = client.models.generate_content(
                model="gemini-2.0-flash", contents=prompt
            )
            print( response.text)
        except Exception as e:
            print(f"Error generating response: {e}")

finally:
    conn.close()
    print("Database connection closed.")
