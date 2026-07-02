import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sqlalchemy import create_engine

engine = create_engine("mysql+mysqlconnector://root:123456789@localhost/loksabha_2024")

# Join turnout and margins on PC Name
df = pd.read_sql("""
    SELECT t.Turnout_Pct AS turnout_pct, m.margin
    FROM turnout t
    JOIN margins m ON t.`PC Name` = m.`PC Name`
""", engine)

plt.figure(figsize=(10, 6))
plt.scatter(df["turnout_pct"], df["margin"], alpha=0.4, color="steelblue")

# Add trend line
z = np.polyfit(df["turnout_pct"], df["margin"], 1)
p = np.poly1d(z)
sorted_x = sorted(df["turnout_pct"])
plt.plot(sorted_x, p(sorted_x), "r--", label="Trend line")

plt.title("Voter Turnout vs Margin of Victory — Lok Sabha 2024")
plt.xlabel("Turnout (%)")
plt.ylabel("Margin of Victory (votes)")
plt.legend()
plt.tight_layout()

plt.savefig("visualizations/q7_turnout_vs_margin.png", dpi=150)
plt.show()

correlation = df["turnout_pct"].corr(df["margin"])
print(f"Correlation coefficient: {correlation:.3f}")
print("Saved successfully")