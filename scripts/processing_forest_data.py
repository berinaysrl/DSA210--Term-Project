import pandas as pd
import os

if not os.path.exists('processed_data_forest'):
    os.makedirs('processed_data_forest')


file_path = '/Users/berinayzumrasariel/Desktop/DSA210 TERM PROJECT/Plants_of_berinayzumrasariel.csv'
df_forest = pd.read_csv(file_path)


df_forest['Start Time'] = pd.to_datetime(df_forest['Start Time'])
df_forest['date'] = df_forest['Start Time'].dt.date  

daily_study = df_forest.groupby('date').size().reset_index(name='total_study_sessions')
daily_study.to_csv('processed_data_forest/daily_study.csv', index=False)
print("Daily study times have been processed and saved.")

daily_tag_summary = df_forest.groupby(['date', 'Tag']).size().reset_index(name='study_sessions')
daily_tag_summary.to_csv('processed_data_forest/daily_tag_summary.csv', index=False)
print("Daily tag-wise study times have been processed and saved.")
