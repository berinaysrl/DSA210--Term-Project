#total hours / attempt count

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the dataset
file_path = '/Users/berinayzumrasariel/Desktop/DSA210 TERM PROJECT/Plants_of_berinayzumrasariel.csv'
data = pd.read_csv(file_path)

# Convert Start Time and End Time to datetime objects
data['Start Time'] = pd.to_datetime(data['Start Time'])
data['End Time'] = pd.to_datetime(data['End Time'])

# Calculate session durations in hours
data['Duration (hours)'] = (data['End Time'] - data['Start Time']).dt.total_seconds() / 3600

# Step 1: Exclude CDP and PROJ201
excluded_tags = ['CDP', 'PROJ201']
data = data[~data['Tag'].isin(excluded_tags)]

# Step 2: Handle duplicate tags (including merging SPS into SPS102)
data['Tag'] = data['Tag'].replace({'SPS': 'SPS102', 'SPS102 1': 'SPS102', 'CS204 1': 'CS204'})

# Step 3: Group by tag to calculate total hours and study sessions
merged_data = data.groupby('Tag')[['Duration (hours)']].sum().reset_index()
merged_data['study_sessions'] = data.groupby('Tag').size().values
merged_data.columns = ['Tag', 'Total Hours', 'Study Sessions']

# Step 4: Separate "Unset" and "Study" data
unset_data = merged_data[merged_data['Tag'] == 'Unset']
study_data = merged_data[merged_data['Tag'] == 'Study']

# Step 5: Calculate the total number of unset and study sessions and hours
unset_hours = unset_data['Total Hours'].sum()
unset_sessions = unset_data['Study Sessions'].sum()
study_hours = study_data['Total Hours'].sum()
study_sessions = study_data['Study Sessions'].sum()

# Filter out "Unset" and "Study" from the main dataset
filtered_data = merged_data[~merged_data['Tag'].isin(['Unset', 'Study'])].copy()

# Step 6: Calculate weights for redistribution
filtered_data['Weight'] = filtered_data['Total Hours'] / filtered_data['Total Hours'].sum()

# Distribute "Unset" and "Study" hours and sessions proportionally
filtered_data['Distributed Unset Hours'] = filtered_data['Weight'] * unset_hours
filtered_data['Distributed Study Hours'] = filtered_data['Weight'] * study_hours
filtered_data['Distributed Unset Sessions'] = filtered_data['Weight'] * unset_sessions
filtered_data['Distributed Study Sessions'] = filtered_data['Weight'] * study_sessions

# Add redistributed data to original values
filtered_data['Adjusted Total Hours'] = (
    filtered_data['Total Hours'] +
    filtered_data['Distributed Unset Hours'] +
    filtered_data['Distributed Study Hours']
)
filtered_data['Adjusted Study Sessions'] = (
    filtered_data['Study Sessions'] +
    filtered_data['Distributed Unset Sessions'] +
    filtered_data['Distributed Study Sessions']
)

# Step 7: Calculate Attention Span (in minutes)
filtered_data['Attention Span (minutes/attempt)'] = (
    (filtered_data['Adjusted Total Hours'] / filtered_data['Adjusted Study Sessions']) * 60
)

# Sort by attention span for analysis
filtered_data = filtered_data.sort_values(by='Attention Span (minutes/attempt)', ascending=False)

# Save the results to a CSV for further inspection
output_path = '/Users/berinayzumrasariel/Desktop/DSA210 TERM PROJECT/attention_span_analysis.csv'
filtered_data.to_csv(output_path, index=False)

# Plot the results
plt.figure(figsize=(10, 8))
bars = plt.barh(filtered_data['Tag'], filtered_data['Attention Span (minutes/attempt)'], color='plum')
plt.xlabel('Attention Span (minutes/attempt)')
plt.ylabel('Course Tag')
plt.title('Attention Span by Course (in Minutes)')

# Add attention span values (rounded to whole minutes) next to each bar
for bar, value in zip(bars, filtered_data['Attention Span (minutes/attempt)']):
    plt.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height() / 2,
             f'{int(round(value))}', va='center', ha='left', fontsize=10)

plt.tight_layout()

# Save the plot
plot_output_path = '/Users/berinayzumrasariel/Desktop/DSA210 TERM PROJECT/attention_span_plot_minutes.png'
plt.savefig(plot_output_path)
plt.show()

print(f"Analysis saved to {output_path}")
print(f"Plot saved to {plot_output_path}")