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
output_dir = "./updated_graphs"
os.makedirs(output_dir, exist_ok=True)

def create_density_heatmap(data_x, data_y, xlabel, ylabel, title, output_path):
    """
    Create density-style heatmap using sns.kdeplot
    """
    # Convert categorical x to numeric codes if necessary
    if data_x.dtype == 'object' or isinstance(data_x.dtype, pd.CategoricalDtype):
        x_labels = data_x.unique()
        x_numeric = data_x.astype('category').cat.codes
    else:
        x_numeric = data_x
        x_labels = None

    # Convert categorical y to numeric codes if necessary
    if data_y.dtype == 'object' or isinstance(data_y.dtype, pd.CategoricalDtype):
        y_labels = data_y.unique()
        y_numeric = data_y.astype('category').cat.codes
    else:
        y_numeric = data_y
        y_labels = None

    plt.figure(figsize=(12, 10))
    sns.kdeplot(x=x_numeric, y=y_numeric, cmap="Reds", fill=True, alpha=0.8, levels=100)

    # Add x-axis labels if converted to numeric
    if x_labels is not None:
        plt.xticks(ticks=range(len(x_labels)), labels=x_labels, rotation=45)

    # Add y-axis labels if converted to numeric
    if y_labels is not None:
        plt.yticks(ticks=range(len(y_labels)), labels=y_labels)

    plt.title(title, fontsize=16)
    plt.xlabel(xlabel, fontsize=14)
    plt.ylabel(ylabel, fontsize=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)

    # Save to file
    plt.savefig(output_path)
    print(f"Saved plot to {output_path}")

    # Show plot
    plt.show()
    plt.close()

# Analyze and plot data
def analyze_and_plot(period_name, tags, study_data, insta_data, start_date, end_date):
    # Filter data
    period_study = study_data.loc[
        (study_data["Start Time"] >= start_date) &
        (study_data["Start Time"] <= end_date) &
        (study_data["Tag"].isin(tags))
    ].copy()

    if period_study.empty:
        print(f"No study data for {period_name}. Skipping.")
        return

    # Create hour and day columns
    period_study["hour"] = period_study["Start Time"].dt.hour
    period_study["day_of_week"] = period_study["Start Time"].dt.day_name()
    period_study["day_of_week"] = pd.Categorical(period_study["day_of_week"], categories=day_order, ordered=True)

    # Hourly correlation heatmap (density-style)
    output_hourly_path = f"{output_dir}/density_hourly_correlation_{period_name}.png"
    create_density_heatmap(
        data_x=period_study["hour"],
        data_y=period_study["Tag"],
        xlabel="Hour",
        ylabel="Tags",
        title=f"Density Heatmap of Hourly Correlation ({period_name})",
        output_path=output_hourly_path
    )

    # Daily correlation heatmap (density-style)
    output_daily_path = f"{output_dir}/density_daily_correlation_{period_name}.png"
    create_density_heatmap(
        data_x=period_study["day_of_week"],
        data_y=period_study["Tag"],
        xlabel="Day of Week",
        ylabel="Tags",
        title=f"Density Heatmap of Daily Correlation ({period_name})",
        output_path=output_daily_path
    )

# Iterate through academic periods
academic_period_dates = {
    "Oct 2024 - Now": ("2024-10-01", insta_data["timestamp"].max()),
    "Feb 2024 - June 2024": ("2024-02-01", "2024-06-30"),
    "Before Feb 2024": ("2023-09-01", "2024-01-31")
}

for period_name, tags in academic_periods.items():
    start_date, end_date = map(pd.Timestamp, academic_period_dates[period_name])
    analyze_and_plot(period_name, tags, study_data, insta_data, start_date, end_date)
