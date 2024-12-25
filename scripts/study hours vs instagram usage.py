import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

study_file_path = "/Users/berinayzumrasariel/Desktop/DSA210 TERM PROJECT/Cleaned_and_Adjusted_Study_Data.csv"
instagram_file_path = "/Users/berinayzumrasariel/Desktop/DSA210 TERM PROJECTcontent/processed_likes.csv"

output_directory = "/Users/berinayzumrasariel/Desktop/DSA210 TERM PROJECT/insta_usage_vs_study_graphs"
os.makedirs(output_directory, exist_ok=True)

study_data = pd.read_csv(study_file_path)
instagram_data = pd.read_csv(instagram_file_path)

study_data["Start Time"] = pd.to_datetime(study_data["Start Time"], errors="coerce").dt.tz_localize(None)
study_data["End Time"] = pd.to_datetime(study_data["End Time"], errors="coerce").dt.tz_localize(None)
study_data = study_data.dropna(subset=["Start Time", "End Time"])
study_data["Hour"] = study_data["Start Time"].dt.hour

instagram_data["timestamp"] = pd.to_datetime(instagram_data["timestamp"], errors="coerce").dt.tz_localize(None)
instagram_data = instagram_data.dropna(subset=["timestamp"])


academic_periods = {
    "Feb 2023 - June 2023": (pd.Timestamp("2023-02-01"), pd.Timestamp("2023-06-30")),
    "Oct 2023 - Jan 2024": (pd.Timestamp("2023-10-01"), pd.Timestamp("2024-01-31")),
    "Feb 2024 - June 2024": (pd.Timestamp("2024-02-01"), pd.Timestamp("2024-06-30")),
    "Oct 2024 - Now": (pd.Timestamp("2024-10-01"), instagram_data["timestamp"].max()),
}

for period_name, (start_date, end_date) in academic_periods.items():
    period_study_data = study_data[
        (study_data["Start Time"] >= start_date) & (study_data["Start Time"] <= end_date)
    ]
    period_instagram_data = instagram_data[
        (instagram_data["timestamp"] >= start_date) & (instagram_data["timestamp"] <= end_date)
    ]

    focused_hours = period_study_data.groupby("Hour")["Duration (hours)"].sum()
    instagram_hours = period_instagram_data["timestamp"].dt.hour.value_counts().sort_index()

    hours = np.arange(24)
    focused_hours = focused_hours.reindex(hours, fill_value=0)
    instagram_hours = instagram_hours.reindex(hours, fill_value=0)

    fig, ax1 = plt.subplots(figsize=(12, 6))
    color1 = 'tab:blue'
    ax1.set_xlabel("Hour of the Day")
    ax1.set_ylabel("Total Study Hours", color=color1)
    ax1.bar(hours, focused_hours, color=color1, alpha=0.6, label="Focused Study Hours")
    ax1.tick_params(axis='y', labelcolor=color1)

    ax2 = ax1.twinx()
    color2 = 'tab:red'
    ax2.set_ylabel("Instagram Usage (count)", color="orange")
    ax2.plot(hours, instagram_hours, color="orange", marker='o', label="Instagram Usage")
    ax2.tick_params(axis='y', labelcolor="orange")

    ax1.set_xticks(hours)
    ax1.set_xticklabels([f"{hour:02d}:00" for hour in hours], rotation=45)
    plt.title(f"Focused Study Hours vs Instagram Usage for {period_name}")

    fig.tight_layout()
    output_file = f"{output_directory}/{period_name.replace(' ', '_')}_comparison.png"
    plt.savefig(output_file)
    plt.show()
