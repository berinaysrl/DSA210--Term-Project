import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load datasets
study_data_path = "/Users/berinayzumrasariel/Desktop/DSA210 TERM PROJECT/Cleaned_and_Adjusted_Study_Data.csv"
insta_data_path = "/Users/berinayzumrasariel/Desktop/DSA210 TERM PROJECT/extracted_likes_timestamps.csv"

study_data = pd.read_csv(study_data_path)
insta_data = pd.read_csv(insta_data_path, header=None, names=["timestamp"])

# Convert to datetime
study_data["Start Time"] = pd.to_datetime(study_data["Start Time"], errors="coerce").dt.tz_localize(None)
study_data["End Time"] = pd.to_datetime(study_data["End Time"], errors="coerce").dt.tz_localize(None)
insta_data["timestamp"] = pd.to_datetime(insta_data["timestamp"], errors="coerce").dt.tz_localize(None)

# Define academic periods and tags
academic_periods = {
    "Oct 2024 - Now": ["CS204", "MATH204", "HUM201", "DSA210", "NS206", "ECON202"],
    "Feb 2024 - June 2024": ["MATH201", "MATH203", "ENS208", "CS201", "PSY201"],
    "Before Feb 2024": ["TLL102", "SPS102", "NS102", "MATH102"]
}

# Day-of-week order
day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# Output directory to save graphs
output_dir = "./graphs"
os.makedirs(output_dir, exist_ok=True)

# Define colors
heatmap_cmap = sns.diverging_palette(220, 20, as_cmap=True)  # Pastel blue and coral
bar_colors = {
    "aggregate": ["skyblue", "lightcoral"],  # Two pastel colors
    "hourly_tag": "mediumpurple",
    "daily_tag": "lightseagreen"
}


# Helper function to calculate and plot correlations
def analyze_and_plot(period_name, tags, study_data, insta_data, start_date, end_date):
    # Filter data (create copies to avoid SettingWithCopyWarning)
    period_study = study_data.loc[
        (study_data["Start Time"] >= start_date) &
        (study_data["Start Time"] <= end_date) &
        (study_data["Tag"].isin(tags))
        ].copy()

    period_insta = insta_data.loc[
        (insta_data["timestamp"] >= start_date) &
        (insta_data["timestamp"] <= end_date)
        ].copy()

    # If no data, skip
    if period_study.empty or period_insta.empty:
        print(f"No data for {period_name}. Skipping.")
        return

    # Create hour and ordered weekday columns
    period_study["hour"] = period_study["Start Time"].dt.hour
    period_study["day"] = period_study["Start Time"].dt.day_name()
    period_study["day"] = pd.Categorical(period_study["day"], categories=day_order, ordered=True)

    period_insta["hour"] = period_insta["timestamp"].dt.hour
    period_insta["day"] = period_insta["timestamp"].dt.day_name()
    period_insta["day"] = pd.Categorical(period_insta["day"], categories=day_order, ordered=True)

    # Aggregate study data by hour and day
    hourly_focus = (
        period_study
        .groupby(["Tag", "hour"], observed=False)["Duration (hours)"]
        .sum()
        .unstack(fill_value=0)
    )
    daily_focus = (
        period_study
        .groupby(["Tag", "day"], observed=False)["Duration (hours)"]
        .sum()
        .unstack(fill_value=0)
    )
    
    # Reindex daily columns to ensure Monday→Sunday
    existing_days = [c for c in day_order if c in daily_focus.columns]
    daily_focus = daily_focus.reindex(columns=existing_days)

    
    hourly_insta = period_insta.groupby("hour").size()
    daily_insta = period_insta.groupby("day", observed=False).size().reindex(day_order, fill_value=0)

    hourly_sum = hourly_focus.sum(axis=0)
    hour_corr = hourly_sum.corr(hourly_insta)

    daily_sum = daily_focus.sum(axis=0)
    day_corr = daily_sum.corr(daily_insta)

    tag_hourly_corr = {}
    for tag in hourly_focus.index:
        tag_series = hourly_focus.loc[tag]
        corr_val = tag_series.corr(hourly_insta)
        tag_hourly_corr[tag] = corr_val
    df_tag_hourly_corr = pd.DataFrame.from_dict(tag_hourly_corr, orient="index", columns=["Hourly Correlation"])

    tag_daily_corr = {}
    for tag in daily_focus.index:
        tag_series = daily_focus.loc[tag]
        corr_val = tag_series.corr(daily_insta)
        tag_daily_corr[tag] = corr_val
    df_tag_daily_corr = pd.DataFrame.from_dict(tag_daily_corr, orient="index", columns=["Daily Correlation"])

    plt.figure(figsize=(8, 6))
    plt.bar(["Hourly", "Daily"], [hour_corr, day_corr], color=bar_colors["aggregate"])
    plt.title(f"Aggregate Correlation of Study Time vs. Instagram Usage ({period_name})", fontsize=14)
    plt.ylabel("Correlation Coefficient", fontsize=12)
    plt.ylim(-1, 1)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.savefig(f"{output_dir}/aggregate_correlation_{period_name}.png")
    plt.show()
    plt.close()
    plt.show()

    df_tag_hourly_corr.sort_values("Hourly Correlation", inplace=True)
    plt.figure(figsize=(8, 6))
    sns.barplot(x="Hourly Correlation", y=df_tag_hourly_corr.index, data=df_tag_hourly_corr,
                color=bar_colors["hourly_tag"])
    plt.title(f"Per-Tag Hourly Correlation with Instagram Usage ({period_name})", fontsize=14)
    plt.xlim(-1, 1)
    plt.xlabel("Correlation Coefficient", fontsize=12)
    plt.ylabel("Tags", fontsize=12)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.savefig(f"{output_dir}/per_tag_hourly_correlation_{period_name}.png")
    plt.show()
    plt.close()

    df_tag_daily_corr.sort_values("Daily Correlation", inplace=True)
    plt.figure(figsize=(8, 6))
    sns.barplot(x="Daily Correlation", y=df_tag_daily_corr.index, data=df_tag_daily_corr, color=bar_colors["daily_tag"])
    plt.title(f"Per-Tag Daily Correlation with Instagram Usage ({period_name})", fontsize=14)
    plt.xlim(-1, 1)
    plt.xlabel("Correlation Coefficient", fontsize=12)
    plt.ylabel("Tags", fontsize=12)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.savefig(f"{output_dir}/per_tag_daily_correlation_{period_name}.png")
    plt.show()
    plt.close()


# Iterate through academic periods
academic_period_dates = {
    "Oct 2024 - Now": ("2024-10-01", insta_data["timestamp"].max()),
    "Feb 2024 - June 2024": ("2024-02-01", "2024-06-30"),
    "Before Feb 2024": ("2023-09-01", "2024-01-31")
}

for period_name, tags in academic_periods.items():
    start_date, end_date = map(pd.Timestamp, academic_period_dates[period_name])
    analyze_and_plot(period_name, tags, study_data, insta_data, start_date, end_date)

