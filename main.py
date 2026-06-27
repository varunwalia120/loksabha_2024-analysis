import pandas as pd

# STEP 1: LOAD THE FILE

df = pd.read_excel("lok_sabha.xlsx", header=2)

print("Raw shape:", df.shape)
print(df.head(3))

# STEP 2: DROP TRAILING JUNK ROWS

df = df[df["State Name"].notna()].copy()
print("After dropping trailing junk:", df.shape)

# STEP 3: STRIP WHITESPACE FROM ALL STRING COLUMNS

str_cols = ["State Name", "PC Name", "Candidate Name", "Gender", "Party Name", "Category"]
df[str_cols] = df[str_cols].apply(lambda x: x.str.strip())

# STEP 4: REMOVE THE STRAY REPEATED HEADER ROW

stray_count = (df["Gender"] == "Gender").sum()
print(f"Stray header rows found: {stray_count}")
df = df[df["Gender"] != "Gender"].copy()

# STEP 5: FIX NUMERIC COLUMN TYPES

numeric_cols = [
    "Total Votes Polled In\nThe Constituency",
    "Valid Votes",
    "General",
    "Postal",
    "Total",
    "Total Electors"
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Check if coerce created any new NaNs — if yes, investigate
print("NaNs after numeric conversion:")
print(df[numeric_cols].isnull().sum())

# Check dtypes are now numeric
print(df[numeric_cols].dtypes)


# STEP 6: SEPARATE NOTA ROWS FROM CANDIDATE ROWS

nota_df = df[df["Party Name"] == "NOTA"].copy()
candidate_df = df[df["Party Name"] != "NOTA"].copy()

print(f"Total rows: {len(df)}")
print(f"Candidate rows: {len(candidate_df)}")
print(f"NOTA rows: {len(nota_df)}")


# STEP 7: IDENTIFY WINNER PER CONSTITUENCY

winner_idx = candidate_df.groupby("PC Name")["Total"].idxmax()
winner_df = candidate_df.loc[winner_idx].copy()
winner_df["is_winner"] = True

print("Winners identified:", len(winner_df))
print(winner_df[["State Name", "PC Name", "Candidate Name", "Party Name", "Total"]].head())


# STEP 8: CALCULATE MARGIN OF VICTORY

top2 = (
    candidate_df
    .sort_values(["PC Name", "Total"], ascending=[True, False])
    .groupby("PC Name")
    .head(2)
)

margin_df = (
    top2
    .groupby("PC Name")["Total"]
    .apply(lambda x: x.iloc[0] - x.iloc[1])
    .reset_index()
)
margin_df.columns = ["PC Name", "Margin"]

print("Margin calculated for constituencies:", len(margin_df))
print(margin_df.sort_values("Margin", ascending=False).head(5))


# STEP 9: CALCULATE TURNOUT PER CONSTITUENCY

turnout_df = (
    df.groupby("PC Name")
    .agg(
        State=("State Name", "first"),
        Total_Electors=("Total Electors", "first"),
        Total_Votes_Polled=("Total Votes Polled In\nThe Constituency", "first")
    )
    .reset_index()
)
turnout_df["Turnout_Pct"] = (
    turnout_df["Total_Votes_Polled"] / turnout_df["Total_Electors"] * 100
).round(2)

print("Turnout calculated for constituencies:", len(turnout_df))
print(turnout_df.sort_values("Turnout_Pct", ascending=False).head(5))


# STEP 10: FINAL SANITY CHECK

print("\n--- SANITY CHECKS ---")
print("Unique constituencies:", df["PC Name"].nunique())
print("Unique states:", df["State Name"].nunique())
print("Unique parties (after strip):", candidate_df["Party Name"].nunique())
print("Duplicate winners:", winner_df["PC Name"].duplicated().sum())
print("Gender distribution of winners:")
print(winner_df["Gender"].value_counts())


# STEP 11: EXPORT CLEANED DATAFRAMES TO CSV

candidate_df.to_csv("candidates_clean.csv", index=False)
winner_df.to_csv("winners_clean.csv", index=False)
margin_df.to_csv("margins_clean.csv", index=False)
turnout_df.to_csv("turnout_clean.csv", index=False)
nota_df.to_csv("nota_clean.csv", index=False)

print("\nAll CSVs exported successfully.")
