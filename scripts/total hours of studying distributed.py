import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

file_path = '/Users/berinayzumrasariel/Desktop/DSA210 TERM PROJECT/Cleaned_and_Adjusted_Study_Data.csv'
data = pd.read_csv(file_path)

data['Start Time'] = pd.to_datetime(data['Start Time'], errors='coerce')
data['End Time'] = pd.to_datetime(data['End Time'], errors='coerce')

excluded_tags = ['CDP', 'PROJ201']
data = data[~data['Tag'].isin(excluded_tags)]

data['Duration (hours)'] = (data['End Time'] - data['Start Time']).dt.total_seconds() / 3600

data['Tag'] = data['Tag'].replace({'SPS': 'SPS102', 'SPS102 1': 'SPS102', 'CS204 1': 'CS204'})


merged_data = data.groupby('Tag')['Duration (hours)'].sum().reset_index()
merged_data.columns = ['Tag', 'Total Hours']
unset_hours = merged_data.loc[merged_data['Tag'] == 'Unset', 'Total Hours'].values[0] if 'Unset' in merged_data['Tag'].values else 0
study_hours = merged_data.loc[merged_data['Tag'] == 'Study', 'Total Hours'].values[0] if 'Study' in merged_data['Tag'].values else 0

filtered_data = merged_data[~merged_data['Tag'].isin(['Unset', 'Study'])].copy()
total_hours_excluding_unset_and_study = filtered_data['Total Hours'].sum()

filtered_data['Weight'] = filtered_data['Total Hours'] / total_hours_excluding_unset_and_study
filtered_data['Distributed Unset Hours'] = filtered_data['Weight'] * unset_hours
filtered_data['Distributed Study Hours'] = filtered_data['Weight'] * study_hours

filtered_data['Adjusted Total Hours'] = (
    filtered_data['Total Hours'] +
    filtered_data['Distributed Unset Hours'] +
    filtered_data['Distributed Study Hours'] )

filtered_data = filtered_data.sort_values(by='Adjusted Total Hours', ascending=True)

final_data = filtered_data[['Tag', 'Total Hours', 'Distributed Unset Hours', 'Distributed Study Hours', 'Adjusted Total Hours']]


plt.figure(figsize=(12, 8))
plt.barh(final_data['Tag'], final_data['Adjusted Total Hours'], color='pink')
plt.xlabel('Adjusted Total Hours')
plt.title('Adjusted Total Hours by Course Tag (Descending Order)')

for index, value in enumerate(final_data['Adjusted Total Hours']):
    plt.text(value + 0.5, index, f'{value:.2f}', va='center')

plt.tight_layout()
output_chart_path = '/Users/berinayzumrasariel/Desktop/DSA210 TERM PROJECT/Adjusted_Total_Hours_by_Tag_Sorted.png'
plt.savefig(output_chart_path)
plt.show()
print(final_data)
