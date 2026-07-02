import pandas as pd
from sqlalchemy import create_engine, text

engine = create_engine("mysql+mysqlconnector://root:123456789@localhost/loksabha_2024")

df = pd.read_csv("candidates_clean.csv")

constituencies = df[["PC Name", "State Name"]].drop_duplicates()
constituencies = constituencies[constituencies["PC Name"].notna()]
constituencies = constituencies[constituencies["State Name"].notna()]
constituencies.columns = ["pc_name", "state"]

print("Loading:", len(constituencies), "constituencies")

constituencies.to_sql("constituencies", engine, if_exists="append", index=False)

with engine.connect() as conn:
    count = conn.execute(text("SELECT COUNT(*) FROM constituencies")).fetchone()[0]
    print("Loaded:", count)