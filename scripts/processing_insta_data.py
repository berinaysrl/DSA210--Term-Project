import pandas as pd
import json
import os
from datetime import datetime, timezone, timedelta

output_dir = 'processed_data_insta'
os.makedirs(output_dir, exist_ok=True)

file_path = '/Users/berinayzumrasariel/Desktop/DSA210 TERM PROJECT/liked_posts.json'
with open(file_path, 'r') as file:
    data = json.load(file)
    
timestamps = []
for like in data['likes_media_likes']:
    for item in like["string_list_data"]:
        timestamp = int(item['timestamp'])
        timestamps.append(timestamp)

df_instagram = pd.DataFrame({'timestamp': timestamps})
df_instagram['timestamp'] = pd.to_datetime(df_instagram['timestamp'], unit='s')  
df_instagram['date'] = df_instagram['timestamp'].dt.date 
df_instagram['time'] = df_instagram['timestamp'].dt.strftime('%H:%M')  

processed_data = df_instagram[['date', 'time']]

processed_data['date'] = processed_data['date'].astype(str)

csv_output_path = os.path.join(output_dir, 'processed_instagram.csv')
processed_data.to_csv(csv_output_path, index=False)

json_output_path = os.path.join(output_dir, 'processed_instagram.json')
processed_data_json = processed_data.to_dict(orient='records')  # Convert DataFrame to list of dictionaries
with open(json_output_path, 'w') as json_file:
    json.dump(processed_data_json, json_file, indent=4)

print(f"Instagram data has been processed and saved to:\nCSV: {csv_output_path}\nJSON: {json_output_path}")
