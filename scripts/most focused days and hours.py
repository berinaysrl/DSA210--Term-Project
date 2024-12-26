import pandas as pd
import matplotlib.pyplot as plt

file_path = '/content/Cleaned_and_Adjusted_Study_Data.csv'
attention_file = '/content/attention_span_analysis.csv'

data = pd.read_csv(file_path)
attention_data = pd.read_csv(attention_file)

data['Start Time'] = pd.to_datetime(data['Start Time'], format='ISO8601', errors='coerce')
data['End Time'] = pd.to_datetime(data['End Time'], format='ISO8601', errors='coerce')

if data['Start Time'].isnull().any() or data['End Time'].isnull().any():
    print("Warning: Some datetime entries could not be parsed and will be dropped.")
    data = data.dropna(subset=['Start Time', 'End Time'])

if 'Duration (hours)' not in data.columns:
    data['Duration (hours)'] = (data['End Time'] - data['Start Time']).dt.total_seconds() / 3600

excluded_tags = ['CDP', 'PROJ201', 'studying italian', 'writing stories']
data = data[~data['Tag'].isin(excluded_tags)]

data['Tag'] = data['Tag'].replace({
    'SPS': 'SPS102',
    'SPS102 1': 'SPS102',
    'CS204 1': 'CS204'
})

unset_data = data[data['Tag'] == 'Unset']
study_data = data[data['Tag'] == 'Study']

total_unset_hours = unset_data['Duration (hours)'].sum()
total_unset_sessions = len(unset_data)

total_study_hours = study_data['Duration (hours)'].sum()
total_study_sessions = len(study_data)

attention_data['Weight'] = attention_data['Total Hours'] / attention_data['Total Hours'].sum()
attention_data['Distributed Unset Hours'] = attention_data['Weight'] * total_unset_hours
attention_data['Distributed Unset Sessions'] = attention_data['Weight'] * total_unset_sessions
attention_data['Distributed Study Hours'] = attention_data['Weight'] * total_study_hours
attention_data['Distributed Study Sessions'] = attention_data['Weight'] * total_study_sessions

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
        new_row_df = pd.DataFrame([new_row])
        data = pd.concat([data, new_row_df], ignore_index=True)


data = data[~data['Tag'].isin(['Unset', 'Study'])]


data['Hour'] = data['Start Time'].dt.hour
data['Day of Week'] = data['Start Time'].dt.day_name()

days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

tags = data['Tag'].unique()
for tag in tags:
    tag_data = data[data['Tag'] == tag]
    
    if tag_data.empty:
        continue

    hourly_counts = tag_data['Hour'].value_counts().reindex(range(24), fill_value=0) 
    daily_counts = tag_data['Day of Week'].value_counts().reindex(days_order, fill_value=0)

    if hourly_counts.sum() == 0 and daily_counts.sum() == 0:
        continue


    plt.figure(figsize=(12, 8))
    plt.subplot(2, 1, 1)
    plt.plot(hourly_counts.index, hourly_counts.values, marker='o', color='plum')
    plt.title(f'Most Focused Hours for {tag}')
    plt.xlabel('Hour of the Day (00:00 to 23:00)')
    plt.ylabel('Number of Study Sessions')
    plt.xticks(range(0, 24))  

    plt.subplot(2, 1, 2)
    plt.plot(daily_counts.index, daily_counts.values, marker='o', color='skyblue')
    plt.title(f'Most Focused Days for {tag}')
    plt.xlabel('Day of the Week')
    plt.ylabel('Number of Study Sessions')
    plt.tight_layout()


    output_path = f'/content/focused_hours_and_days_{tag}.png'
    plt.savefig(output_path)
    plt.show()
    print(f'Graph for {tag} saved to {output_path}')
