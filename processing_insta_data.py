import pandas as pd
import json
import os

# Ensure 'processed_data' directory exists
if not os.path.exists('processed_data_insta'):
    os.makedirs('processed_data_insta')

# Load Instagram JSON file
with open('/Users/berinayzumrasariel/Desktop/DSA210 TERM PROJECT/liked_posts.json', 'r') as file:
    data = json.load(file)

# Extract timestamps (like activity)
timestamps = [int(item['string_list_data'][0]['timestamp']) for item in data['likes_media_likes']]

# Convert timestamps to DataFrame
df_instagram = pd.DataFrame(timestamps, columns=['timestamp'])
df_instagram['timestamp'] = pd.to_datetime(df_instagram['timestamp'], unit='s')  # Convert to datetime

# Convert to dates and count likes per day
df_instagram['date'] = df_instagram['timestamp'].dt.date
daily_likes = df_instagram['date'].value_counts().reset_index()
daily_likes.columns = ['date', 'likes']

# Sort the data chronologically by date
daily_likes = daily_likes.sort_values(by='date', ascending=True)

# Save anonymized and processed data
daily_likes.to_csv('processed_data_insta/processed_instagram.csv', index=False)
print("Instagram data has been processed and saved.")

