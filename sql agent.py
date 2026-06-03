import sqlite3
from google import genai
import pandas as pd
import os
import re

# Use environment variable for API key
client = genai.Client(
    api_key=os.environ.get("GOOGLE_APIAIzaSyAnTzcVO0f2z3ESHZEEMczdBUIwMYVMlnE_KEY")
)


def is_safe_sql(sql):
    dangerous = [
        "DROP",
        "DELETE",
        "UPDATE",
        "INSERT",
        "ALTER",
        "CREATE",
        "TRUNCATE",
        "EXEC",
        "EXECUTE",
        "SHUTDOWN",
        "KILL",
    ]
    sql_upper = sql.upper()
    return not any(d in sql_upper for d in dangerous)


def extract_sql(text):
    """Strip markdown code blocks if AI wraps SQL in them."""
    match = re.search(r"```(?:sql)?\s*(.*?)```", text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return text.strip()


# Connect database
conn = sqlite3.connect("churn.db")

try:
    # Show columns to AI
    df = pd.read_sql_query("SELECT * FROM customers LIMIT 5", conn)

    print("Agent Ready")
    print("Ask about customer churn (type 'exit' to quit)")
    print("------------------------------------------------")

    while True:
        question = input("\nAsk question: ").strip()

        if not question:
            print("Please enter a question.")
            continue

        if question.lower() == "exit":
            break

        prompt = f"""
You are a data analyst working with a SQLite database.

Table name: customers

Columns:
{list(df.columns)}

Sample data:
{df.to_string(index=False)}

Write ONLY a valid SQLite SQL query to answer the following question.
Do not include explanations or markdown formatting.

Question: {question}
"""

        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash", contents=prompt
            )
            sql_query = extract_sql(response.text)
        except Exception as e:
            print(f"Error generating SQL: {e}")
            continue

        print("\nGenerated SQL:")
        print(sql_query)

        if not is_safe_sql(sql_query):
            print("⚠️  Generated SQL contains dangerous keywords. Skipping.")
            continue

        try:
            result = pd.read_sql_query(sql_query, conn)
            print("\nResult:")
            print(
                result.to_string(index=False)
                if not result.empty
                else "No results found."
            )
        except Exception as e:
            print(f"Error running SQL: {e}")

finally:
    conn.close()
    print("\nDatabase connection closed.")
