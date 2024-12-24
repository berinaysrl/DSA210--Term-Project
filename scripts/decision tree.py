import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report, precision_score, roc_auc_score, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

# Load datasets
study_data_path = '/Users/berinayzumrasariel/Desktop/DSA210 TERM PROJECT/Cleaned_and_Adjusted_Study_Data.csv'
insta_data_path = '/Users/berinayzumrasariel/Desktop/DSA210 TERM PROJECT/extracted_likes_timestamps.csv'

study_data = pd.read_csv(study_data_path)
insta_data = pd.read_csv(insta_data_path, header=None, names=["timestamp"])

# Preprocess timestamps
study_data["Start Time"] = pd.to_datetime(study_data["Start Time"], errors="coerce").dt.tz_localize(None)
study_data["End Time"] = pd.to_datetime(study_data["End Time"], errors="coerce").dt.tz_localize(None)
insta_data["timestamp"] = pd.to_datetime(insta_data["timestamp"], errors="coerce").dt.tz_localize(None)

# Add a binary target variable: Did Instagram usage occur during the study session?
study_data["Instagram Used"] = study_data.apply(
    lambda row: int(
        insta_data["timestamp"].between(row["Start Time"], row["End Time"]).any()
    ),
    axis=1
)

# Select features and target variable
y = study_data["Instagram Used"]
x = study_data[["Duration (hours)", "Weight", "Adjusted Hours", "Adjusted Sessions"]]

# Split data into train and test sets
train_x, test_x, train_y, test_y = train_test_split(x, y, test_size=0.2, random_state=42)

# Hyperparameter tuning
param_grid = {
    'max_depth': [None, 10, 20],
    'min_samples_leaf': [1, 2, 4]
}

grid_search = GridSearchCV(DecisionTreeClassifier(random_state=42),
                           param_grid=param_grid, cv=5, scoring="accuracy")
grid_search.fit(train_x, train_y)

# Get the best hyperparameters and train the model
best_params = grid_search.best_params_
print(f'Best Hyperparameters: {best_params}')
best_model = grid_search.best_estimator_

# Predict on the test set
y_pred = best_model.predict(test_x)

# Evaluate the model
accuracy = accuracy_score(test_y, y_pred)
classification_report_result = classification_report(test_y, y_pred)
precision = precision_score(test_y, y_pred)
roc_auc = roc_auc_score(test_y, y_pred)

print(f'Accuracy: {accuracy}')
print('Classification Report:')
print(classification_report_result)
print(f'Precision: {precision}')
print(f'AUC-ROC: {roc_auc}')

# Confusion matrix
conf_matrix = confusion_matrix(test_y, y_pred)
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Purples', cbar=False)
plt.xlabel('Predicted Labels')
plt.ylabel('True Labels')
plt.title('Confusion Matrix')
plt.show()