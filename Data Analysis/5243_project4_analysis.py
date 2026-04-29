import os
import pandas as pd
import matplotlib.pyplot as plt

# File path
DATA_PATH = "citibike_station_day_clean.csv"

# Output folder for figures and summary tables
OUTPUT_DIR = "eda_outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 1. Load data
df = pd.read_csv(DATA_PATH)

# Convert date column to datetime format
df["date"] = pd.to_datetime(df["date"])

# Create time-related variables
df["day_of_week"] = df["date"].dt.day_name()
df["is_weekend"] = df["date"].dt.dayofweek >= 5
df["day_type"] = df["is_weekend"].map({True: "Weekend", False: "Weekday"})

# 2. Basic data summary
print("===== Data Overview =====")
print(f"Number of rows: {df.shape[0]}")
print(f"Number of columns: {df.shape[1]}")
print(f"Date range: {df['date'].min().date()} to {df['date'].max().date()}")
print(f"Number of stations: {df['station_id'].nunique()}")
print(f"Total trips: {df['daily_trip_count'].sum()}")

print("\n===== Missing Values =====")
print(df.isna().sum())

print("\n===== Daily Trip Count Summary =====")
print(df["daily_trip_count"].describe())

# Save descriptive summary
summary_stats = df[[
    "daily_trip_count",
    "casual_share",
    "member_share",
    "classic_bike_share",
    "electric_bike_share",
    "mean_temperature",
    "precipitation_sum",
    "max_wind_speed"
]].describe()

summary_stats.to_csv(os.path.join(OUTPUT_DIR, "summary_statistics.csv"))

# 3. Overall daily demand trend
daily_demand = (
    df.groupby("date")["daily_trip_count"]
    .sum()
    .reset_index()
    .rename(columns={"daily_trip_count": "total_daily_trips"})
)

plt.figure(figsize=(10, 5))
plt.plot(daily_demand["date"], daily_demand["total_daily_trips"], marker="o")
plt.title("Overall Daily Citi Bike Demand")
plt.xlabel("Date")
plt.ylabel("Total Daily Trips")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "daily_demand_trend.png"), dpi=300)
plt.close()

print("\n===== Overall Daily Demand =====")
print(daily_demand["total_daily_trips"].describe())

# 4. Demand distribution
plt.figure(figsize=(8, 5))
plt.hist(df["daily_trip_count"], bins=40)
plt.title("Distribution of Station-Day Demand")
plt.xlabel("Daily Trip Count")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "demand_distribution_histogram.png"), dpi=300)
plt.close()

plt.figure(figsize=(8, 5))
plt.boxplot(df["daily_trip_count"], vert=False)
plt.title("Boxplot of Station-Day Demand")
plt.xlabel("Daily Trip Count")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "demand_distribution_boxplot.png"), dpi=300)
plt.close()

# 5. Weekday vs weekend analysis
weekday_summary = (
    df.groupby("day_type")["daily_trip_count"]
    .agg(["count", "mean", "median", "std"])
    .reset_index()
)

weekday_summary.to_csv(os.path.join(OUTPUT_DIR, "weekday_weekend_summary.csv"), index=False)

plt.figure(figsize=(7, 5))
df.boxplot(column="daily_trip_count", by="day_type")
plt.title("Station-Day Demand: Weekday vs Weekend")
plt.suptitle("")
plt.xlabel("Day Type")
plt.ylabel("Daily Trip Count")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "weekday_weekend_boxplot.png"), dpi=300)
plt.close()

daily_demand_with_type = (
    df.groupby(["date", "day_type"])["daily_trip_count"]
    .sum()
    .reset_index()
)

day_type_avg = (
    daily_demand_with_type.groupby("day_type")["daily_trip_count"]
    .mean()
    .reset_index()
    .rename(columns={"daily_trip_count": "average_total_daily_trips"})
)

plt.figure(figsize=(6, 5))
plt.bar(day_type_avg["day_type"], day_type_avg["average_total_daily_trips"])
plt.title("Average Total Daily Trips: Weekday vs Weekend")
plt.xlabel("Day Type")
plt.ylabel("Average Total Daily Trips")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "weekday_weekend_average_total_trips.png"), dpi=300)
plt.close()

print("\n===== Weekday vs Weekend Summary =====")
print(weekday_summary)

# 6. Weather impact analysis
weather_daily = (
    df.groupby("date")
    .agg(
        total_daily_trips=("daily_trip_count", "sum"),
        mean_temperature=("mean_temperature", "first"),
        precipitation_sum=("precipitation_sum", "first"),
        max_wind_speed=("max_wind_speed", "first")
    )
    .reset_index()
)

plt.figure(figsize=(7, 5))
plt.scatter(weather_daily["mean_temperature"], weather_daily["total_daily_trips"])
plt.title("Daily Demand vs Mean Temperature")
plt.xlabel("Mean Temperature")
plt.ylabel("Total Daily Trips")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "demand_vs_temperature.png"), dpi=300)
plt.close()

plt.figure(figsize=(7, 5))
plt.scatter(weather_daily["precipitation_sum"], weather_daily["total_daily_trips"])
plt.title("Daily Demand vs Precipitation")
plt.xlabel("Precipitation Sum")
plt.ylabel("Total Daily Trips")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "demand_vs_precipitation.png"), dpi=300)
plt.close()

weather_corr = weather_daily[[
    "total_daily_trips",
    "mean_temperature",
    "precipitation_sum",
    "max_wind_speed"
]].corr()

weather_corr.to_csv(os.path.join(OUTPUT_DIR, "weather_correlation.csv"))

print("\n===== Weather Correlation with Total Daily Demand =====")
print(weather_corr["total_daily_trips"])

# 7. Station-level demand comparison
station_summary = (
    df.groupby("station_name")
    .agg(
        total_trips=("daily_trip_count", "sum"),
        average_daily_trips=("daily_trip_count", "mean"),
        active_days=("date", "nunique")
    )
    .reset_index()
    .sort_values("total_trips", ascending=False)
)

station_summary.to_csv(os.path.join(OUTPUT_DIR, "station_demand_summary.csv"), index=False)

top_10_stations = station_summary.head(10)

plt.figure(figsize=(10, 6))
plt.barh(top_10_stations["station_name"], top_10_stations["total_trips"])
plt.title("Top 10 Busiest Stations")
plt.xlabel("Total Trips")
plt.ylabel("Station Name")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "top_10_busiest_stations.png"), dpi=300)
plt.close()

print("\n===== Top 10 Busiest Stations =====")
print(top_10_stations)

# 8. Correlation heatmap
corr_vars = [
    "daily_trip_count",
    "casual_share",
    "member_share",
    "classic_bike_share",
    "electric_bike_share",
    "mean_temperature",
    "precipitation_sum",
    "max_wind_speed"
]

corr_matrix = df[corr_vars].corr()
corr_matrix.to_csv(os.path.join(OUTPUT_DIR, "correlation_matrix.csv"))

plt.figure(figsize=(8, 6))
plt.imshow(corr_matrix, aspect="auto")
plt.colorbar(label="Correlation")
plt.xticks(range(len(corr_vars)), corr_vars, rotation=45, ha="right")
plt.yticks(range(len(corr_vars)), corr_vars)
plt.title("Correlation Matrix")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "correlation_heatmap.png"), dpi=300)
plt.close()

print("\n===== Correlation with Station-Day Demand =====")
print(corr_matrix["daily_trip_count"].sort_values(ascending=False))

print("\nEDA completed. Figures and summary tables are saved in the 'eda_outputs' folder.")

