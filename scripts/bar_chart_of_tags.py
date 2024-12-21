import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load daily_tag_summary data
tag_data = pd.read_csv("/Users/berinayzumrasariel/Desktop/DSA210 TERM PROJECT/DSA210-TERM-PROJECT/.venv/processed_data_forest/daily_tag_summary.csv")

# Step 1: Merge duplicate tags
tag_data['Tag'] = tag_data['Tag'].replace({'SPS102 1': 'SPS102', 'CS204 1': 'CS204', 'SPS': 'SPS102'})

# Step 2: Separate "Unset" and "Study" tags
unset_data = tag_data[tag_data['Tag'] == 'Unset']
study_data = tag_data[tag_data['Tag'] == 'Study']
non_unset_data = tag_data[~tag_data['Tag'].isin(['Unset', 'Study', 'English', 'writing stories', 'studying italian'])]

# Step 2.1: Exclude specific tags (CDP and PROJ201)
excluded_tags = ['CDP', 'PROJ201']
non_unset_data = non_unset_data[~non_unset_data['Tag'].isin(excluded_tags)]

# Calculate total unset and study sessions
total_unset_sessions = unset_data['study_sessions'].sum()
total_study_sessions = study_data['study_sessions'].sum()

# Step 3: Group non-unset data to calculate weights
tag_summary = non_unset_data.groupby('Tag')['study_sessions'].sum().reset_index()
tag_summary.columns = ['Tag', 'Total Attempts']

# Calculate the total study sessions excluding "Unset" and "Study"
total_attempts_excluding_unset_and_study = tag_summary['Total Attempts'].sum()

# Calculate weights for each tag
tag_summary['Weight'] = tag_summary['Total Attempts'] / total_attempts_excluding_unset_and_study

# Distribute "Unset" and "Study" sessions proportionally
tag_summary['Distributed Unset Attempts'] = tag_summary['Weight'] * total_unset_sessions
tag_summary['Distributed Study Attempts'] = tag_summary['Weight'] * total_study_sessions

# Add the redistributed sessions to the original total
tag_summary['Adjusted Total Attempts'] = (
    tag_summary['Total Attempts'] +
    tag_summary['Distributed Unset Attempts'] +
    tag_summary['Distributed Study Attempts']
)

# Sort the data for visualization
tag_summary = tag_summary.sort_values(by='Adjusted Total Attempts', ascending=False)

# Step 4: Plot the horizontal bar chart
plt.figure(figsize=(6, 12))
bars = plt.barh(tag_summary['Tag'], tag_summary['Adjusted Total Attempts'], color='#B2D8B2')
plt.xlabel('Total Adjusted Attempts of Studying')
plt.title('Randomized Total Attempts of Studying by Course Tag')

# Add values at the end of the bars
for bar in bars:
    plt.text(bar.get_width() + 1, bar.get_y() + bar.get_height() / 2,
             f'{int(bar.get_width())}', va='center', ha='left', fontsize=10)

plt.gca().invert_yaxis()  # Highest value at the top
plt.tight_layout()

# Save and show the plot
plt.savefig('processed_data/tag_ranking_study_realistic_adjusted.png')
plt.show()