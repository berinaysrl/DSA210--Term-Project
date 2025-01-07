import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

study_data_path = "/Users/berinayzumrasariel/Desktop/DSA210 TERM PROJECT/Cleaned_and_Adjusted_Study_Data.csv"
likes_data_path = "/Users/berinayzumrasariel/Desktop/DSA210 TERM PROJECT/processed_likes.csv"

study_data = pd.read_csv(study_data_path)
likes_data = pd.read_csv(likes_data_path)

study_data['Start Time'] = pd.to_datetime(study_data['Start Time'], format='mixed', errors='coerce')
study_data['End Time'] = pd.to_datetime(study_data['End Time'], format='mixed', errors='coerce')
likes_data['timestamp'] = pd.to_datetime(likes_data['timestamp'], format='mixed', errors='coerce')

study_data = study_data.dropna(subset=['Start Time', 'End Time'])
likes_data = likes_data.dropna(subset=['timestamp'])

likes_data['date'] = likes_data['timestamp'].dt.date
instagram_usage_daily = likes_data.groupby('date').size().reset_index(name='Instagram Usage')

study_data['date'] = study_data['Start Time'].dt.date
daily_study_hours = study_data.groupby('date')['Adjusted Hours'].sum().reset_index(name='Study Hours')

merged_data = pd.merge(instagram_usage_daily, daily_study_hours, on='date', how='inner')

features = merged_data[['Instagram Usage']].values  
target = merged_data['Study Hours'].values          

X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

regressor = LinearRegression()
regressor.fit(X_train, y_train)

y_pred = regressor.predict(X_test)

print(f"Mean Squared Error: {mean_squared_error(y_test, y_pred)}")
print(f"R2 Score: {r2_score(y_test, y_pred)}")
