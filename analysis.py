import pandas as pd
import matplotlib.pyplot as plt
from db_utils import get_all_currencies

currencies = get_all_currencies()

df = pd.DataFrame(currencies)

print("Currency Data:")
print(df)

df["usd_rate"] = df["usd_rate"].astype(float)

print("\nHighest USD rates:")
print(df.sort_values("usd_rate", ascending=False).head())

plt.figure(figsize=(10, 5))
plt.bar(df["currency_code"], df["usd_rate"])
plt.title("Currency Exchange Rates Against USD")
plt.xlabel("Currency")
plt.ylabel("USD Rate")
plt.tight_layout()
plt.show()