import json
import pandas as pd
from datetime import datetime, timezone

raw_file_path = '/Users/berinayzumrasariel/Desktop/DSA210 TERM PROJECT/liked_posts.json'
with open(raw_file_path, 'r') as file:
    data = json.load(file)

timestamps = []
for like in data['likes_media_likes']:
    for item in like['string_list_data']:

        utc_timestamp = int(item['timestamp'])
        dt_utc = datetime.fromtimestamp(utc_timestamp, tz=timezone.utc)
        timestamps.append(dt_utc)

likes_df = pd.DataFrame({'timestamp': timestamps})
likes_df['timestamp'] = likes_df['timestamp'].dt.tz_convert('Europe/Istanbul')
likes_df['hour'] = likes_df['timestamp'].dt.hour

processed_file_path = '/Users/berinayzumrasariel/Desktop/DSA210 TERM PROJECT/processed_likes.csv'
likes_df.to_csv(processed_file_path, index=False)
print(f"Preprocessed data saved to {processed_file_path}")
