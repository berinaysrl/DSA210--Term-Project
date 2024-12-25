import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# File paths
study_file_path = "/Users/berinayzumrasariel/Desktop/DSA210 TERM PROJECT/Cleaned_and_Adjusted_Study_Data.csv"
instagram_file_path = "/Users/berinayzumrasariel/Desktop/DSA210 TERM PROJECT/extracted_likes_timestamps.csv"

# Load the cleaned study data
study_data = pd.read_csv(study_file_path)

# Convert Start Time and End Time to datetime with timezone-awareness
study_data["Start Time"] = (
    pd.to_datetime(study_data["Start Time"], errors="coerce")
      .dt.tz_convert("UTC")
      .dt.tz_localize(None)
)
study_data["End Time"] = (
    pd.to_datetime(study_data["End Time"], errors="coerce")
      .dt.tz_convert("UTC")
      .dt.tz_localize(None)
)

# Drop rows with invalid datetimes
study_data = study_data.dropna(subset=["Start Time", "End Time"])

# Extract hour from Start Time for analysis
study_data["Hour"] = study_data["Start Time"].dt.hour

# Load the Instagram data
instagram_data = pd.read_csv(instagram_file_path, header=None, names=["timestamp"])
instagram_data["timestamp"] = (
    pd.to_datetime(instagram_data["timestamp"], errors="coerce")
      .dt.tz_convert("UTC")
      .dt.tz_localize(None)
)

# Drop rows with invalid timestamps
instagram_data = instagram_data.dropna(subset=["timestamp"])

# Define academic periods
academic_periods = {
    "Feb 2023 - June 2023": (pd.Timestamp("2023-02-01"), pd.Timestamp("2023-06-30")),
    "Oct 2023 - Jan 2024": (pd.Timestamp("2023-10-01"), pd.Timestamp("2024-01-31")),
    "Feb 2024 - June 2024": (pd.Timestamp("2024-02-01"), pd.Timestamp("2024-06-30")),
    "Oct 2024 - Now": (pd.Timestamp("2024-10-01"), instagram_data["timestamp"].max()),
}

# Analyze focused study hours and Instagram usage
for period_name, (start_date, end_date) in academic_periods.items():
    # Filter study data and Instagram data for the current academic period
    period_study_data = study_data[
        (study_data["Start Time"] >= start_date) & (study_data["Start Time"] <= end_date)
    ]
    period_instagram_data = instagram_data[
        (instagram_data["timestamp"] >= start_date) & (instagram_data["timestamp"] <= end_date)
    ]

    # Calculate the total focused study hours per hour of day
    focused_hours = period_study_data.groupby("Hour")["Duration (hours)"].sum()

    # Calculate Instagram usage frequency per hour of day
    instagram_hours = period_instagram_data["timestamp"].dt.hour.value_counts().sort_index()

    # Ensure both series have an entry for every hour (0-23)
    hours = np.arange(24)
    focused_hours = focused_hours.reindex(hours, fill_value=0)
    instagram_hours = instagram_hours.reindex(hours, fill_value=0)

    # Plot side by side with two different y-axes
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Primary axis: Study hours (bars)
    color1 = 'tab:blue'
    ax1.set_xlabel("Hour of the Day")
    ax1.set_ylabel("Total Study Hours", color=color1)
    ax1.bar(hours, focused_hours, color=color1, alpha=0.6, label="Focused Study Hours")
    ax1.tick_params(axis='y', labelcolor=color1)

    # Secondary axis: Instagram usage (line or bars)
    ax2 = ax1.twinx()  # shares the same x-axis
    color2 = 'tab:red'
    ax2.set_ylabel("Instagram Usage (count)", color="orange")
    ax2.plot(hours, instagram_hours, color="orange", marker='o', label="Instagram Usage")
    ax2.tick_params(axis='y', labelcolor="orange")

    # Format x-axis with hour labels
    ax1.set_xticks(hours)
    ax1.set_xticklabels([f"{hour:02d}:00" for hour in hours], rotation=45)

    plt.title(f"Focused Study Hours vs Instagram Usage for {period_name}")

    # Make layout nice
    fig.tight_layout()

    # Save the plot
    output_file = f"/Users/berinayzumrasariel/Desktop/DSA210 TERM PROJECT/{period_name.replace(' ', '_')}_comparison.png"
    plt.savefig(output_file)
    plt.show()