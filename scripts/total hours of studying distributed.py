import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

# Load the dataset
file_path = '/Users/berinayzumrasariel/Desktop/DSA210 TERM PROJECT/Plants_of_berinayzumrasariel.csv'
data = pd.read_csv(file_path)

# Convert Start Time and End Time to datetime objects
data['Start Time'] = pd.to_datetime(data['Start Time'])
data['End Time'] = pd.to_datetime(data['End Time'])

#excluding almost non-recorded tags from the main dataset for simplicity
excluded_tags = ['CDP', 'PROJ201']
data = data[~data['Tag'].isin(excluded_tags)]

# Calculate session durations in hours
data['Duration (hours)'] = (data['End Time'] - data['Start Time']).dt.total_seconds() / 3600

# Merge duplicate tags
data['Tag'] = data['Tag'].replace({'SPS': 'SPS102', 'SPS102 1': 'SPS102', 'CS204 1': 'CS204'})

# Group by tag to consolidate hours
merged_data = data.groupby('Tag')['Duration (hours)'].sum().reset_index()
merged_data.columns = ['Tag', 'Total Hours']

# Handle "Unset" and "Study" by randomly distributing them
# Extract total hours for "Unset" and "Study"
unset_hours = merged_data.loc[merged_data['Tag'] == 'Unset', 'Total Hours'].values[0]
study_hours = merged_data.loc[merged_data['Tag'] == 'Study', 'Total Hours'].values[0]

# Filter out "Unset" and "Study" from the main dataset
filtered_data = merged_data[~merged_data['Tag'].isin(['Unset', 'Study'])].copy()

# Calculate the total hours excluding "Unset" and "Study"
total_hours_excluding_unset_and_study = filtered_data['Total Hours'].sum()

# Calculate weights for each tag
filtered_data['Weight'] = filtered_data['Total Hours'] / total_hours_excluding_unset_and_study

# Distribute "Unset" and "Study" hours proportionally
filtered_data['Distributed Unset Hours'] = filtered_data['Weight'] * unset_hours
filtered_data['Distributed Study Hours'] = filtered_data['Weight'] * study_hours

# Add the redistributed hours to the original hours
filtered_data['Adjusted Total Hours'] = (
    filtered_data['Total Hours'] +
    filtered_data['Distributed Unset Hours'] +
    filtered_data['Distributed Study Hours']
)

# Sort the final dataset in descending order by Adjusted Total Hours
filtered_data = filtered_data.sort_values(by='Adjusted Total Hours', ascending=True)

# Final dataset
final_data = filtered_data[['Tag', 'Total Hours', 'Distributed Unset Hours', 'Distributed Study Hours', 'Adjusted Total Hours']]

# Save a bar chart for the final dataset
plt.figure(figsize=(12, 8))
plt.barh(final_data['Tag'], final_data['Adjusted Total Hours'], color='pink')
plt.xlabel('Adjusted Total Hours')
plt.title('Adjusted Total Hours by Course Tag (Descending Order)')

# Add values at the end of the bars
for index, value in enumerate(final_data['Adjusted Total Hours']):
    plt.text(value + 0.5, index, f'{value:.2f}', va='center')

plt.tight_layout()

# Save the chart
output_chart_path = '/Users/berinayzumrasariel/Desktop/DSA210 TERM PROJECT/Adjusted_Total_Hours_by_Tag_Sorted.png'  # Replace with desired save path
plt.savefig(output_chart_path)
plt.show()
print(final_data)
