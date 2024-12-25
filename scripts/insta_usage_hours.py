import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

file_path = '/Users/berinayzumrasariel/Desktop/extracted_likes_timestamps.csv'  
likes_df = pd.read_csv(file_path)

likes_df["timestamp"] = pd.to_datetime(likes_df["timestamp"], errors="coerce")
likes_df.dropna(subset=["timestamp"], inplace=True)
likes_df["hour"] = likes_df["timestamp"].dt.hour

academic_periods = {
    "Feb 2023 - June 2023": (pd.Timestamp("2023-02-01"), pd.Timestamp("2023-06-30")),
    "Oct 2023 - Jan 2024": (pd.Timestamp("2023-10-01"), pd.Timestamp("2024-01-31")),
    "Feb 2024 - June 2024": (pd.Timestamp("2024-02-01"), pd.Timestamp("2024-06-30")),
    "Oct 2024 - Now": (pd.Timestamp("2024-10-01"), likes_df["timestamp"].max()) }

for period, (start, end) in academic_periods.items():
    period_likes = likes_df[(likes_df["timestamp"] >= start) & (likes_df["timestamp"] <= end)]
    likes_count = Counter(period_likes["hour"])

    hours_sorted = sorted(likes_count.keys())
    likes_sorted = [likes_count[hour] for hour in hours_sorted]

    print(f"\nHourly Likes for {period}:")
    for hour, count in zip(hours_sorted, likes_sorted):
        print(f"{hour:02d}:00–{hour:02d}:59: {count} likes")

    plt.figure(figsize=(12, 6))
    plt.bar(hours_sorted, likes_sorted, color="pink", alpha=0.8)
    plt.xticks(hours_sorted, [f"{hour:02d}:00" for hour in hours_sorted], rotation=45)
    plt.xlabel("Hour of the Day")
    plt.ylabel("Number of Likes")
    plt.title(f"Hourly Likes for {period}")
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    output_chart_path = f"/Users/berinayzumrasariel/Desktop/hourly_likes_{period.replace(' ', '_').replace('-', '_')}.png"
    plt.savefig(output_chart_path)
    plt.show()
    print(f"Chart saved to {output_chart_path}")
