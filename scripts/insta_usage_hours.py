import json
from datetime import datetime, timezone, timedelta
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# Load the JSON file
file_path = '/Users/berinayzumrasariel/Desktop/DSA210 TERM PROJECT/liked_posts.json'
with open(file_path, 'r') as file:
    data = json.load(file)

# Extract and convert timestamps
likes = data.get("likes_media_likes", [])
timestamps = []
for like in likes:
    for item in like["string_list_data"]:
        timestamp = item["timestamp"]
        # Convert timestamp to a datetime object with timezone
        dt = datetime.fromtimestamp(timestamp, tz=timezone(timedelta(hours=3)))  # Assuming +03:00 timezone
        timestamps.append(dt)

# Convert timestamps to a DataFrame for easier handling
likes_df = pd.DataFrame({'timestamp': timestamps})
likes_df['date'] = likes_df['timestamp'].dt.date
likes_df['hour'] = likes_df['timestamp'].dt.hour

# Define academic periods with timezone awareness
tz = timezone(timedelta(hours=3))  # Assuming +03:00 timezone
academic_periods = {
    "Feb 2023 - June 2023": (pd.Timestamp("2023-02-01", tz=tz), pd.Timestamp("2023-06-30", tz=tz)),
    "Oct 2023 - Jan 2024": (pd.Timestamp("2023-10-01", tz=tz), pd.Timestamp("2024-01-31", tz=tz)),
    "Feb 2024 - June 2024": (pd.Timestamp("2024-02-01", tz=tz), pd.Timestamp("2024-06-30", tz=tz)),
    "Oct 2024 - Now": (pd.Timestamp("2024-10-01", tz=tz), likes_df['timestamp'].max())
}

# Analyze hourly likes for each academic period
for period, (start, end) in academic_periods.items():
    period_likes = likes_df[(likes_df['timestamp'] >= start) & (likes_df['timestamp'] <= end)]
    likes_count = Counter(period_likes['hour'])

    # Prepare data for plotting
    hours_sorted = sorted(likes_count.keys())
    likes_sorted = [likes_count[hour] for hour in hours_sorted]

    # Print the counts for each hour
    print(f"\nHourly Likes for {period}:")
    for hour, count in zip(hours_sorted, likes_sorted):
        print(f"{hour:02d}:00–{hour:02d}:59: {count} likes")

    # Plot the counts
    plt.figure(figsize=(12, 6))
    plt.bar(hours_sorted, likes_sorted, color='pink', alpha=0.8)
    plt.xticks(hours_sorted, [f"{hour:02d}:00" for hour in hours_sorted], rotation=45)
    plt.xlabel("Hour of the Day")
    plt.ylabel("Number of Likes")
    plt.title(f"Hourly Likes for {period}")
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Save the chart
    output_chart_path = f'/Users/berinayzumrasariel/Desktop/DSA210 TERM PROJECT/hourly_likes_{period.replace(" ", "_").replace("-", "_")}.png'
    plt.savefig(output_chart_path)
    plt.show()

    print(f"Chart saved to {output_chart_path}")