import pandas as pd
import matplotlib.pyplot as plt

file_path = '/Users/berinayzumrasariel/Desktop/extracted_likes_timestamps.csv'  
data = pd.read_csv(file_path)

data["timestamp"] = pd.to_datetime(data["timestamp"], errors="coerce")
data.dropna(subset=["timestamp"], inplace=True)

academic_periods = {
    "Feb 2023 - June 2023": (pd.Timestamp("2023-02-01"), pd.Timestamp("2023-06-30")),
    "Oct 2023 - Jan 2024": (pd.Timestamp("2023-10-01"), pd.Timestamp("2024-01-31")),
    "Feb 2024 - June 2024": (pd.Timestamp("2024-02-01"), pd.Timestamp("2024-06-30")),
    "Oct 2024 - Now": (pd.Timestamp("2024-10-01"), data["timestamp"].max())
}

for period_name, (start_date, end_date) in academic_periods.items():
    period_data = data[(data["timestamp"] >= start_date) & (data["timestamp"] <= end_date)].copy()
    if period_data.empty:
        print(f"No data available for {period_name}.")
        continue

    period_data["day_of_week"] = period_data["timestamp"].dt.day_name()
    weekly_likes = period_data.groupby("day_of_week").size()

    ordered_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    weekly_likes = weekly_likes.reindex(ordered_days, fill_value=0)

    plt.figure(figsize=(10, 6))
    plt.bar(weekly_likes.index, weekly_likes.values, color="skyblue", alpha=0.8)
    plt.xlabel("Day of the Week")
    plt.ylabel("Number of Likes")
    plt.title(f"Instagram Likes by Day of the Week for {period_name}")
    plt.tight_layout()

    output_path = f"likes_by_day_{period_name.replace(' ', '_').replace('-', '_')}.png"
    plt.savefig(output_path)
    print(f"Graph saved for {period_name} at {output_path}")
    plt.show()
