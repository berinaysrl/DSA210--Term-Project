import pandas as pd
import matplotlib.pyplot as plt
import os

# Ensuring again that the 'processed_data' directory exists
if not os.path.exists('processed_data'):
    os.makedirs('processed_data')

# Loading processed datasets here
study_data = pd.read_csv(
    '/Users/berinayzumrasariel/Desktop/DSA210 TERM PROJECT/DSA210-TERM-PROJECT/.venv/processed_data_forest/daily_study.csv')
instagram_data = pd.read_csv(
    '/Users/berinayzumrasariel/Desktop/DSA210 TERM PROJECT/DSA210-TERM-PROJECT/.venv/bin/processed_data_insta/processed_instagram.csv')

# Merging study hours and Instagram likes into one
merged = pd.merge(study_data, instagram_data, on='date', how='left').fillna(0)

# Convert 'date' to datetime
merged['date'] = pd.to_datetime(merged['date'])

# Defining academic periods, omitting the summer/winter breaks
academic_periods = {
    "Feb 2023 - June 2023": (pd.Timestamp("2023-02-01"), pd.Timestamp("2023-06-30")),
    "Oct 2023 - Jan 2024": (pd.Timestamp("2023-10-01"), pd.Timestamp("2024-01-31")),
    "Feb 2024 - June 2024": (pd.Timestamp("2024-02-01"), pd.Timestamp("2024-06-30")),
    "Oct 2024 - Now": (pd.Timestamp("2024-10-01"), merged['date'].max())
}

# Creating a vertical layout with one plot for each period
num_periods = len(academic_periods)
fig, axes = plt.subplots(num_periods, 1, figsize=(12, 6 * num_periods))

# Loop through each academic period and plotting them one by one
for ax, (title, (start, end)) in zip(axes, academic_periods.items()):
    period_data = merged[(merged['date'] >= start) & (merged['date'] <= end)]

    # Skipping if there is no data existing for that period
    if period_data.empty:
        ax.text(0.5, 0.5, f"No data for {title}", ha='center', va='center', fontsize=12)
        continue

    # Study Hours
    ax.set_xlabel('Date')
    ax.set_ylabel('Study Hours', color='tab:blue')
    ax.plot(period_data['date'], period_data['total_study_sessions'], label='Study Hours', color='tab:blue',
            linewidth=2)
    ax.tick_params(axis='y', labelcolor='tab:blue')

    # Instagram Usage over likes given (second axis)
    ax2 = ax.twinx()
    ax2.set_ylabel('Instagram Likes', color='tab:orange')
    ax2.plot(period_data['date'], period_data['likes'], label='Instagram Likes', color='tab:orange', linewidth=2)
    ax2.tick_params(axis='y', labelcolor='tab:orange')

    # Formatting x-axis for precision and readability
    tick_frequency = max(len(period_data['date']) // 8, 1)
    ax.set_xticks(period_data['date'][::tick_frequency])
    ax.set_xticklabels(period_data['date'][::tick_frequency].dt.strftime('%d-%b-%Y'), rotation=45)

    # setting the title for each graph
    ax.set_title(f"Studying Attempts vs Instagram Likes ({title})")


# Adjust layout and save
plt.tight_layout()
plt.savefig('processed_data/vertical_academic_periods.png')
plt.show()




