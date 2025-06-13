from pyspark.sql.functions import col, count, when, mean, hour, dayofweek, sum
import pandas as pd
from pyspark.sql import DataFrame
import seaborn as sns
import matplotlib.pyplot as plt
import os
import numpy as np
import dask.dataframe as dd

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    # Convert to Dask DataFrame
    df_dask = dd.from_pandas(df, npartitions=4)  # Adjust partitions based on data size
    # Remplir les valeurs manquantes
    df_dask = df_dask.fillna({
        "RatecodeID": 1,
        "store_and_fwd_flag": "N",  # Vous pouvez choisir "N" ou "Y"
        "congestion_surcharge": 2.5,
        "Airport_fee": 0
    })
    # Remplacer les valeurs manquantes de `passenger_count` par la moyenne
    mean_passenger_count = df_dask["passenger_count"].mean().compute()
    df_dask = df_dask.assign(passenger_count=df_dask["passenger_count"].fillna(mean_passenger_count))
    # Filtrer les trajets aberrants
    # Filter out trips with extreme fare amounts and trip distances
    df = df[(df['fare_amount'] >= 2) & (df['trip_distance'] <= 100) & (df['trip_distance'] >= 0.5)]

    return df_dask.compute()

def enrich_with_time_features(df: pd.DataFrame) -> pd.DataFrame:
    df_dask = dd.from_pandas(df, npartitions=4)  # Adjust partitions based on data size
    """Add time-based features"""
    # Convertir les dates en datetime
    df_dask["tpep_pickup_datetime"] = dd.to_datetime(df_dask["tpep_pickup_datetime"])
    df_dask["tpep_dropoff_datetime"] = dd.to_datetime(df_dask["tpep_dropoff_datetime"])
    return df


def generate_trips_by_hour_plot(df: pd.DataFrame) -> str:
    """Generate and save fare by hour plot"""
    try:
        clean_data(df)
        df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
        df['hour'] = df['tpep_pickup_datetime'].dt.hour
        df_trips = df.groupby('hour').size().reset_index(name='count')

        plt.figure(figsize=(12, 6))
        plt.plot(df_trips.index, df_trips.values, marker='o', linestyle='-', color='b', label="Number of Trips")
        plt.xlabel("Hour of the Day")
        plt.ylabel("Number of Trips")
        plt.title("Number of Trips per Hour of the Day")
        plt.xticks(range(0, 24))
        plt.grid(True)
        plt.legend()

        os.makedirs("static/plot", exist_ok=True)
        plot_path = "static/plot/plotTripsbyhour.png"
        plt.savefig(plot_path, bbox_inches='tight', dpi=300)
        plt.close()

        return plot_path
    except Exception as e:
        plt.close()
        raise e

def generate_trips_price_by_hour_plot(df: pd.DataFrame) -> str:
    try:
        df_dask = dd.from_pandas(df, npartitions=4)
        # We can know the average fare for each hour of the day .
        df_dask["hour"] = df_dask["tpep_pickup_datetime"].dt.hour
        df_dask["day_of_week"] = df_dask["tpep_pickup_datetime"].dt.dayofweek

        df_agg = df_dask.groupby("hour")["fare_amount"].mean().compute()

        plt.figure(figsize=(12, 6))
        plt.plot(df_agg.index, df_agg.values, marker='o', linestyle='-', color='r', label="Tax mean")
        plt.xlabel("Hour of the Day")
        plt.ylabel("Tax mean ($)")
        plt.title("Evolution of tax mean per hour")
        plt.xticks(range(0, 24))
        plt.grid(True)
        plt.legend()

        os.makedirs("static/plot", exist_ok=True)
        plot_path = "static/plot/plotTripspricebyhour.png"
        plt.savefig(plot_path, bbox_inches='tight', dpi=300)
        plt.close()


        return plot_path
    except Exception as e:
        plt.close()
        raise e


def bestHourWork(df: pd.DataFrame) -> str:
    # Convert to Dask DataFrame
    df_dask = dd.from_pandas(df, npartitions=4)

    # Ensure fare_amount is of float type
    df_dask["fare_amount"] = df_dask["fare_amount"].astype(float)

    # Convert pickup datetime to proper datetime type
    df_dask["tpep_pickup_datetime"] = dd.to_datetime(df_dask["tpep_pickup_datetime"])

    # Extract hour from pickup time
    df_dask["hour"] = df_dask["tpep_pickup_datetime"].dt.hour

    # Group by hour and calculate total revenue and count
    df_revenue = df_dask.groupby("hour").agg(
        total_revenue=("fare_amount", "sum"),
        count=("fare_amount", "count")
    )

    # Compute the results into a Pandas DataFrame
    df_revenue = df_revenue.compute()

    # Get the best hour (highest total revenue)
    best_hour = df_revenue.loc[df_revenue["total_revenue"].idxmax()]

    # Prepare the result message
    best_hour_message = f"The best hour of the day for payment is {best_hour.name} with a total revenue of {best_hour['total_revenue']:.0f} $."

    return best_hour_message
