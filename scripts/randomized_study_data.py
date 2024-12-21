import pandas as pd
import numpy as np
import os

# Specify the file path
file_path = '/Users/berinayzumrasariel/Desktop/DSA210 TERM PROJECT/Plants_of_berinayzumrasariel.csv'

# Check if the file exists
if not os.path.exists(file_path):
    raise FileNotFoundError(f"The specified file does not exist: {file_path}")

# Load the data
data = pd.read_csv(file_path)

# Drop specific columns: "Note" and "Tree Type"
columns_to_drop = ['Note', 'Tree Type', 'Is Success']
data = data.drop(columns=columns_to_drop, errors='ignore')

# Convert Start Time and End Time to datetime
data['Start Time'] = pd.to_datetime(data['Start Time'], errors='coerce')
data['End Time'] = pd.to_datetime(data['End Time'], errors='coerce')

# Drop rows with invalid dates
data = data.dropna(subset=['Start Time', 'End Time'])

# Calculate Duration in hours
data['Duration (hours)'] = (data['End Time'] - data['Start Time']).dt.total_seconds() / 3600

# Merge duplicate tags
data['Tag'] = data['Tag'].replace({
    'CS204 1': 'CS204',
    'SPS': 'SPS102',
    'SPS102 1': 'SPS102'
})

# Exclude unwanted tags
data = data[~data['Tag'].isin(['CDP', 'PROJ201'])]

# Separate "Unset" and "Study" data
unset_data = data[data['Tag'] == 'Unset']
study_data = data[data['Tag'] == 'Study']
filtered_data = data[~data['Tag'].isin(['Unset', 'Study'])].copy()  # Explicit copy to avoid warnings

# Calculate weights for redistribution
if not filtered_data.empty:
    total_hours = filtered_data['Duration (hours)'].sum()
    filtered_data['Weight'] = filtered_data['Duration (hours)'] / total_hours
else:
    filtered_data['Weight'] = 0

# Redistribute Unset and Study data
total_unset_hours = unset_data['Duration (hours)'].sum()
total_study_hours = study_data['Duration (hours)'].sum()
total_unset_sessions = len(unset_data)
total_study_sessions = len(study_data)

filtered_data['Distributed Unset Hours'] = filtered_data['Weight'] * total_unset_hours
filtered_data['Distributed Study Hours'] = filtered_data['Weight'] * total_study_hours
filtered_data['Distributed Unset Sessions'] = filtered_data['Weight'] * total_unset_sessions
filtered_data['Distributed Study Sessions'] = filtered_data['Weight'] * total_study_sessions

# Add redistributed values to the original data
filtered_data['Adjusted Hours'] = (
    filtered_data['Duration (hours)'] +
    filtered_data['Distributed Unset Hours'] +
    filtered_data['Distributed Study Hours']
)
filtered_data['Adjusted Sessions'] = (
    filtered_data['Distributed Unset Sessions'] +
    filtered_data['Distributed Study Sessions']
)

# Fill any NaN values with 0 (in case of missing data)
filtered_data.fillna(0, inplace=True)

# Save the cleaned and adjusted dataset
output_path = '/Users/berinayzumrasariel/Desktop/DSA210 TERM PROJECT/Cleaned_and_Adjusted_Study_Data.csv'
filtered_data.to_csv(output_path, index=False)

# Print the resulting dataset
print("Cleaned and Adjusted Study Data:")
print(filtered_data)

# Print confirmation
print(f"Data cleaned and saved to {output_path}")