import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# Connect to MySQL
engine = create_engine("mysql+mysqlconnector://root:123456789@localhost/loksabha_2024")

# Pull margin data
df = pd.read_sql("SELECT margin FROM margins", engine)

# Build the histogram
plt.figure(figsize=(12, 5))
plt.hist(df["margin"], bins=50, color="steelblue", edgecolor="white")
plt.title("Distribution of Victory Margins — Lok Sabha 2024")
plt.xlabel("Margin of Victory (votes)")
plt.ylabel("Number of Constituencies")
plt.axvline(df["margin"].median(), color="red", linestyle="--", 
            label=f'Median: {int(df["margin"].median())}')
plt.legend()
plt.tight_layout()

# Save into visualizations folder
plt.savefig("visualizations/q5_margin_distribution.png", dpi=150)
plt.show()

print("Saved successfully")