#find which days of each semester I tend to procrastinate

import pandas as pd
import matplotlib.pyplot as plt

# Load the data
file_path = '/Users/berinayzumrasariel/Desktop/DSA210 TERM PROJECT/extracted_likes_timestamps.csv'  # Replace with your file path
data = pd.read_csv(file_path, header=None, names=["timestamp"])

# Convert timestamps to datetime with timezone-awareness
data["timestamp"] = pd.to_datetime(data["timestamp"], errors="coerce")

# Drop rows with invalid timestamps
data.dropna(subset=["timestamp"], inplace=True)

# Ensure the data timestamps are timezone-aware
data["timestamp"] = data["timestamp"].dt.tz_convert("UTC")  # Adjust the timezone as needed

# Define academic periods with timezone-awareness
academic_periods = {
    "Feb 2023 - June 2023": (pd.Timestamp("2023-02-01", tz="UTC"), pd.Timestamp("2023-06-30", tz="UTC")),
    "Oct 2023 - Jan 2024": (pd.Timestamp("2023-10-01", tz="UTC"), pd.Timestamp("2024-01-31", tz="UTC")),
    "Feb 2024 - June 2024": (pd.Timestamp("2024-02-01", tz="UTC"), pd.Timestamp("2024-06-30", tz="UTC")),
    "Oct 2024 - Now": (pd.Timestamp("2024-10-01", tz="UTC"), data["timestamp"].max())
}

# Categorize data by academic period and analyze days of the week
for period_name, (start_date, end_date) in academic_periods.items():
    # Filter data for the current period
    period_data = data[(data["timestamp"] >= start_date) & (data["timestamp"] <= end_date)]

    if period_data.empty:
        print(f"No data available for {period_name}.")
        continue

    # Extract the day of the week for grouping
    period_data["day_of_week"] = period_data["timestamp"].dt.day_name()

    # Group by day of the week and count the number of likes
    weekly_likes = period_data.groupby("day_of_week").size()

    # Reorder the days of the week
    ordered_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    weekly_likes = weekly_likes.reindex(ordered_days)

    # Plot the data
    plt.figure(figsize=(10, 6))
    plt.bar(weekly_likes.index, weekly_likes.values, color="skyblue", alpha=0.8)
    plt.xlabel("Day of the Week")
    plt.ylabel("Number of Likes")
    plt.title(f"Instagram Likes by Day of the Week for {period_name}")
    plt.tight_layout()

    # Save the plot
    output_path = f"likes_by_day_{period_name.replace(' ', '_').replace('-', '_')}.png"
    plt.savefig(output_path)
    print(f"Graph saved for {period_name} at {output_path}")

    # Show the plot
    plt.show()