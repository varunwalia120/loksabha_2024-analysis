import pandas as pd
from sqlalchemy import create_engine, text

# Replace yourpassword with your actual MySQL password
engine = create_engine("mysql+mysqlconnector://root:123456789@localhost/loksabha_2024")

# Clear the table
with engine.connect() as conn:
    conn.execute(text("TRUNCATE TABLE candidates"))
    conn.commit()
    print("Cleared")

# Load all 8362 rows
df = pd.read_csv("candidates_clean.csv")
df.to_sql("candidates", engine, if_exists="append", index=False, chunksize=500, method="multi")

# Verify
with engine.connect() as conn:
    count = conn.execute(text("SELECT COUNT(*) FROM candidates")).fetchone()[0]
    print("Rows loaded:", count)