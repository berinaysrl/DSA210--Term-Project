import pandas as pd
import numpy as np
import os

file_path = '/Users/berinayzumrasariel/Desktop/DSA210 TERM PROJECT/Plants_of_berinayzumrasariel.csv'

if not os.path.exists(file_path):
    raise FileNotFoundError(f"The specified file does not exist: {file_path}")

data = pd.read_csv(file_path)

columns_to_drop = ['Note', 'Tree Type', 'Is Success']
data = data.drop(columns=columns_to_drop, errors='ignore')

data['Start Time'] = pd.to_datetime(data['Start Time'], errors='coerce')
data['End Time'] = pd.to_datetime(data['End Time'], errors='coerce')

data = data.dropna(subset=['Start Time', 'End Time'])

data['Duration (hours)'] = (data['End Time'] - data['Start Time']).dt.total_seconds() / 3600

data['Tag'] = data['Tag'].replace({
    'CS204 1': 'CS204',
    'SPS': 'SPS102',
    'SPS102 1': 'SPS102'
})

data = data[~data['Tag'].isin(['CDP', 'PROJ201'])]

unset_data = data[data['Tag'] == 'Unset']
study_data = data[data['Tag'] == 'Study']
filtered_data = data[~data['Tag'].isin(['Unset', 'Study'])].copy()  


if not filtered_data.empty:
    total_hours = filtered_data['Duration (hours)'].sum()
    filtered_data['Weight'] = filtered_data['Duration (hours)'] / total_hours
else:
    filtered_data['Weight'] = 0

total_unset_hours = unset_data['Duration (hours)'].sum()
total_study_hours = study_data['Duration (hours)'].sum()
total_unset_sessions = len(unset_data)
total_study_sessions = len(study_data)

filtered_data['Distributed Unset Hours'] = filtered_data['Weight'] * total_unset_hours
filtered_data['Distributed Study Hours'] = filtered_data['Weight'] * total_study_hours
filtered_data['Distributed Unset Sessions'] = filtered_data['Weight'] * total_unset_sessions
filtered_data['Distributed Study Sessions'] = filtered_data['Weight'] * total_study_sessions


filtered_data['Adjusted Hours'] = (
    filtered_data['Duration (hours)'] +
    filtered_data['Distributed Unset Hours'] +
    filtered_data['Distributed Study Hours']
)
filtered_data['Adjusted Sessions'] = (
    filtered_data['Distributed Unset Sessions'] +
    filtered_data['Distributed Study Sessions']
)

filtered_data.fillna(0, inplace=True)

output_path = '/Users/berinayzumrasariel/Desktop/DSA210 TERM PROJECT/Cleaned_and_Adjusted_Study_Data.csv'
filtered_data.to_csv(output_path, index=False)

print("Cleaned and Adjusted Study Data:")
print(filtered_data)
print(f"Data cleaned and saved to {output_path}")
