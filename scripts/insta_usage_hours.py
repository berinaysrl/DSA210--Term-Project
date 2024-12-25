import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

processed_file_path = '/Users/berinayzumrasariel/Desktop/DSA210 TERM PROJECT/processed_likes.csv'

likes_df = pd.read_csv(processed_file_path, parse_dates=['timestamp'])
likes_df['hour'] = likes_df['timestamp'].dt.hour

academic_periods = {
    "Feb 2023 - June 2023": (pd.Timestamp("2023-02-01", tz='Europe/Istanbul'),
                             pd.Timestamp("2023-06-30", tz='Europe/Istanbul')),
    "Oct 2023 - Jan 2024": (pd.Timestamp("2023-10-01", tz='Europe/Istanbul'),
                            pd.Timestamp("2024-01-31", tz='Europe/Istanbul')),
    "Feb 2024 - June 2024": (pd.Timestamp("2024-02-01", tz='Europe/Istanbul'),
                             pd.Timestamp("2024-06-30", tz='Europe/Istanbul')),
    "Oct 2024 - Now": (pd.Timestamp("2024-10-01", tz='Europe/Istanbul'),
                       likes_df['timestamp'].max())}

for period, (start, end) in academic_periods.items():

    period_likes = likes_df[(likes_df['timestamp'] >= start) & (likes_df['timestamp'] <= end)]
    likes_count = Counter(period_likes['hour'])

    full_hours = list(range(24))
    likes_sorted = [likes_count.get(hour, 0) for hour in full_hours]

    print(f"\nHourly Likes for {period}:")
    for hour, count in zip(full_hours, likes_sorted):
        print(f"{hour:02d}:00–{hour:02d}:59 => {count} likes")

    plt.figure(figsize=(12, 6))
    plt.bar(full_hours, likes_sorted, color='pink', alpha=0.8)
    plt.xticks(full_hours, [f"{hour:02d}:00" for hour in full_hours], rotation=45)
    plt.xlabel("Hour of the Day")
    plt.ylabel("Number of Likes")
    plt.title(f"Hourly Likes for {period}")
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    output_chart_path = f'/Users/berinayzumrasariel/Desktop/DSA210 TERM PROJECT/hourly_likes_{period.replace(" ", "_").replace("-", "_")}.png'
    plt.savefig(output_chart_path)
    plt.show()
    print(f"Chart saved to {output_chart_path}")
