import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
file_path = '/Users/berinayzumrasariel/Desktop/DSA210 TERM PROJECT/Plants_of_berinayzumrasariel.csv'
attention_file = '/Users/berinayzumrasariel/Desktop/DSA210 TERM PROJECT/attention_span_analysis.csv'

data = pd.read_csv(file_path)
attention_data = pd.read_csv(attention_file)

# Convert Start Time and End Time to datetime objects
data['Start Time'] = pd.to_datetime(data['Start Time'])
data['End Time'] = pd.to_datetime(data['End Time'])

# Calculate 'Duration (hours)' if not already calculated
if 'Duration (hours)' not in data.columns:
    data['Duration (hours)'] = (data['End Time'] - data['Start Time']).dt.total_seconds() / 3600

# Exclude CDP and PROJ201
excluded_tags = ['CDP', 'PROJ201']
data = data[~data['Tag'].isin(excluded_tags)]

# Handle duplicate tags (merging SPS into SPS102 and others)
data['Tag'] = data['Tag'].replace({'SPS': 'SPS102', 'SPS102 1': 'SPS102', 'CS204 1': 'CS204'})

# Redistribute "Unset" and "Study"
unset_data = data[data['Tag'] == 'Unset']
study_data = data[data['Tag'] == 'Study']

total_unset_hours = unset_data['Duration (hours)'].sum()
total_unset_sessions = len(unset_data)

total_study_hours = study_data['Duration (hours)'].sum()
total_study_sessions = len(study_data)

# Calculate weights based on attention span analysis
attention_data['Weight'] = attention_data['Total Hours'] / attention_data['Total Hours'].sum()
attention_data['Distributed Unset Hours'] = attention_data['Weight'] * total_unset_hours
attention_data['Distributed Unset Sessions'] = attention_data['Weight'] * total_unset_sessions
attention_data['Distributed Study Hours'] = attention_data['Weight'] * total_study_hours
attention_data['Distributed Study Sessions'] = attention_data['Weight'] * total_study_sessions

# Adjust the main dataset with redistributed "Unset" and "Study" data
for idx, row in attention_data.iterrows():
    tag = row['Tag']
    hours_to_add = row['Distributed Unset Hours'] + row['Distributed Study Hours']
    sessions_to_add = row['Distributed Unset Sessions'] + row['Distributed Study Sessions']
    if tag in data['Tag'].values:
        data.loc[data['Tag'] == tag, 'Duration (hours)'] += hours_to_add
    else:
        new_row = {
            'Tag': tag,
            'Duration (hours)': hours_to_add,
            'study_sessions': sessions_to_add
        }
        data = data.append(new_row, ignore_index=True)

data = data[~data['Tag'].isin(['Unset', 'Study'])]  # Drop unset and study after redistribution

# Extract hourly data and day of the week
data['Hour'] = data['Start Time'].dt.hour
data['Day of Week'] = data['Start Time'].dt.day_name()

# Sort day of the week for proper order
days_order = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

# Create the graphs for each tag
tags = data['Tag'].unique()
for tag in tags:
    tag_data = data[data['Tag'] == tag]

    # Aggregate data by hour and day of the week
    hourly_counts = tag_data['Hour'].value_counts().reindex(range(24), fill_value=0)  # Ensure all hours are included
    daily_counts = tag_data['Day of Week'].value_counts().reindex(days_order, fill_value=0)

    # Create the figure with subplots
    plt.figure(figsize=(12, 8))

    # Most Focused Hours (00:00 to 23:00)
    plt.subplot(2, 1, 1)
    plt.plot(hourly_counts.index, hourly_counts.values, marker='o', color='plum')
    plt.title(f'Most Focused Hours for {tag}')
    plt.xlabel('Hour of the Day (00:00 to 23:00)')
    plt.ylabel('Number of Study Sessions')
    plt.xticks(range(0, 24))  # Ensure all hours are shown

    # Most Focused Days of the Week
    plt.subplot(2, 1, 2)
    plt.plot(daily_counts.index, daily_counts.values, marker='o', color='skyblue')
    plt.title(f'Most Focused Days for {tag}')
    plt.xlabel('Day of the Week')
    plt.ylabel('Number of Study Sessions')

    plt.tight_layout()

    # Save the graph
    output_path = f'/Users/berinayzumrasariel/Desktop/DSA210 TERM PROJECT/focused_hours_and_days_{tag}.png'
    plt.savefig(output_path)
    plt.show()

    print(f'Graph for {tag} saved to {output_path}')