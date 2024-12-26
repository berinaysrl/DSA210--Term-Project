import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

file_path = '/Users/berinayzumrasariel/Desktop/DSA210 TERM PROJECT/Cleaned_and_Adjusted_Study_Data.csv'
data = pd.read_csv(file_path)

data['Start Time'] = pd.to_datetime(data['Start Time'], errors='coerce')
data['End Time'] = pd.to_datetime(data['End Time'], errors='coerce')
data['Duration (hours)'] = (data['End Time'] - data['Start Time']).dt.total_seconds() / 3600

excluded_tags = ['CDP', 'PROJ201', 'studying italian', 'writing stories']
data = data[~data['Tag'].isin(excluded_tags)]
data['Tag'] = data['Tag'].replace({'SPS': 'SPS102', 'SPS102 1': 'SPS102', 'CS204 1': 'CS204'})

merged_data = data.groupby('Tag')[['Duration (hours)']].sum().reset_index()
merged_data['study_sessions'] = data.groupby('Tag').size().values
merged_data.columns = ['Tag', 'Total Hours', 'Study Sessions']

unset_data = merged_data[merged_data['Tag'] == 'Unset']
study_data = merged_data[merged_data['Tag'] == 'Study']

unset_hours = unset_data['Total Hours'].sum() if not unset_data.empty else 0
unset_sessions = unset_data['Study Sessions'].sum() if not unset_data.empty else 0
study_hours = study_data['Total Hours'].sum() if not study_data.empty else 0
study_sessions = study_data['Study Sessions'].sum() if not study_data.empty else 0

filtered_data = merged_data[~merged_data['Tag'].isin(['Unset', 'Study'])].copy()
filtered_data['Weight'] = filtered_data['Total Hours'] / filtered_data['Total Hours'].sum()
filtered_data['Distributed Unset Hours'] = filtered_data['Weight'] * unset_hours
filtered_data['Distributed Study Hours'] = filtered_data['Weight'] * study_hours
filtered_data['Distributed Unset Sessions'] = filtered_data['Weight'] * unset_sessions
filtered_data['Distributed Study Sessions'] = filtered_data['Weight'] * study_sessions

filtered_data['Adjusted Total Hours'] = (
    filtered_data['Total Hours'] +
    filtered_data['Distributed Unset Hours'] +
    filtered_data['Distributed Study Hours']  )

filtered_data['Adjusted Study Sessions'] = (
    filtered_data['Study Sessions'] +
    filtered_data['Distributed Unset Sessions'] +
    filtered_data['Distributed Study Sessions'] )

filtered_data['Attention Span (minutes/attempt)'] = (
    (filtered_data['Adjusted Total Hours'] / filtered_data['Adjusted Study Sessions']) * 60 )

filtered_data = filtered_data.sort_values(by='Attention Span (minutes/attempt)', ascending=False)

output_path = '/Users/berinayzumrasariel/Desktop/DSA210 TERM PROJECT/attention_span_analysis.csv'
filtered_data.to_csv(output_path, index=False)

plt.figure(figsize=(10, 8))
bars = plt.barh(filtered_data['Tag'], filtered_data['Attention Span (minutes/attempt)'], color='plum')
plt.xlabel('Attention Span (minutes/attempt)')
plt.ylabel('Course Tag')
plt.title('Attention Span by Course (in Minutes)')

for bar, value in zip(bars, filtered_data['Attention Span (minutes/attempt)']):
    plt.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height() / 2,
             f'{int(round(value))}', va='center', ha='left', fontsize=10)

plt.tight_layout()
plot_output_path = '/Users/berinayzumrasariel/Desktop/DSA210 TERM PROJECT/attention_span_plot_minutes.png'
plt.savefig(plot_output_path)
plt.show()

print(f"Analysis saved to {output_path}")
print(f"Plot saved to {plot_output_path}")
