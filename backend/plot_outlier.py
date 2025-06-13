import matplotlib.pyplot as plt
import seaborn as sns
import dask.dataframe as dd

from backend.analysis import clean_data,enrich_with_time_features

df = dd.read_parquet(r"C:\Users\fftt7\PycharmProjects\taxiNewYork\backend\uploads\yellow_tripdata_2024-01.parquet")
df = clean_data(df.compute())  # clean with your custom function
df = enrich_with_time_features(df)
df = dd.from_pandas(df)
# Compute a sample from the full dataset to keep plotting fast
sample_df = df[['trip_distance', 'fare_amount']].sample(frac=0.1).compute()

# Optional: filter to a reasonable range for better visualization
sample_df = sample_df[(sample_df['trip_distance'] <= 30) & (sample_df['fare_amount'] <= 100)]

# Scatter plot
plt.figure(figsize=(10, 6))
sns.scatterplot(data=sample_df, x='trip_distance', y='fare_amount', alpha=0.5, edgecolor=None)
plt.title("Trip Distance vs Fare Amount (with potential outliers)")
plt.xlabel("Trip Distance (miles)")
plt.ylabel("Fare Amount ($)")
plt.grid(True)
plt.tight_layout()
plt.show()
