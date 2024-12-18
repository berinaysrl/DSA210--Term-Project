import pandas as pd
import json
import os

# Ensuring that the 'processed_data' directory exists
if not os.path.exists('processed_data_insta'):
    os.makedirs('processed_data_insta')

# Loading Instagram JSON file here
with open('/Users/berinayzumrasariel/Desktop/DSA210 TERM PROJECT/liked_posts.json', 'r') as file:
    data = json.load(file)

# Here we are extracting the timestamps from the file 
timestamps = [int(item['string_list_data'][0]['timestamp']) for item in data['likes_media_likes']]

# Converting timestamps to DataFrame
df_instagram = pd.DataFrame(timestamps, columns=['timestamp'])
df_instagram['timestamp'] = pd.to_datetime(df_instagram['timestamp'], unit='s')  # Convert to datetime

# Converting to dates and count likes per day
df_instagram['date'] = df_instagram['timestamp'].dt.date
daily_likes = df_instagram['date'].value_counts().reset_index()
daily_likes.columns = ['date', 'likes']

# Sorting the data chronologically by date, this way we can track the flow of ups and downs
daily_likes = daily_likes.sort_values(by='date', ascending=True)

# Saving anonymized and processed data
daily_likes.to_csv('processed_data_insta/processed_instagram.csv', index=False)
print("Instagram data has been processed and saved.")

