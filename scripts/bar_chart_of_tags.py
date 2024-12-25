import pandas as pd
import matplotlib.pyplot as plt
import os

tag_data = pd.read_csv("/Users/berinayzumrasariel/Desktop/DSA210 TERM PROJECT/Cleaned_and_Adjusted_Study_Data.csv")

tag_data['Tag'] = tag_data['Tag'].replace({'SPS102 1': 'SPS102', 'CS204 1': 'CS204', 'SPS': 'SPS102'})

unset_data = tag_data[tag_data['Tag'] == 'Unset']
study_data = tag_data[tag_data['Tag'] == 'Study']
non_unset_data = tag_data[~tag_data['Tag'].isin(['Unset', 'Study', 'English', 'writing stories', 'studying italian'])]

excluded_tags = ['CDP', 'PROJ201']
non_unset_data = non_unset_data[~non_unset_data['Tag'].isin(excluded_tags)]

total_unset_sessions = unset_data['Adjusted Sessions'].sum() if not unset_data.empty else 0
total_study_sessions = study_data['Adjusted Sessions'].sum() if not study_data.empty else 0

tag_summary = non_unset_data.groupby('Tag')['Adjusted Sessions'].sum().reset_index()
tag_summary.columns = ['Tag', 'Total Attempts']

total_attempts_excluding_unset_and_study = tag_summary['Total Attempts'].sum()

tag_summary['Weight'] = tag_summary['Total Attempts'] / total_attempts_excluding_unset_and_study
tag_summary['Distributed Unset Attempts'] = tag_summary['Weight'] * total_unset_sessions
tag_summary['Distributed Study Attempts'] = tag_summary['Weight'] * total_study_sessions

tag_summary['Adjusted Total Attempts'] = (
    tag_summary['Total Attempts'] +
    tag_summary['Distributed Unset Attempts'] +
    tag_summary['Distributed Study Attempts']
)

tag_summary = tag_summary.sort_values(by='Adjusted Total Attempts', ascending=False)

plt.figure(figsize=(6, 12))
bars = plt.barh(tag_summary['Tag'], tag_summary['Adjusted Total Attempts'], color='#B2D8B2')
plt.xlabel('Total Adjusted Attempts of Studying')
plt.title('Randomized Total Attempts of Studying by Course Tag')

for bar, value in zip(bars, tag_summary['Adjusted Total Attempts']):
    plt.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height() / 2,
             f'{int(value)}', va='center', ha='left', fontsize=10, color='black')

plt.gca().invert_yaxis()
plt.tight_layout()

output_dir = "/Users/berinayzumrasariel/Desktop/DSA210 TERM PROJECT"
os.makedirs(output_dir, exist_ok=True)

output_path = os.path.join(output_dir, "tag_ranking_study_realistic_adjusted.png")
plt.savefig(output_path)
plt.show()

print(f"Plot saved to {output_path}")
