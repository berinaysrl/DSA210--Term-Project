import pandas as pd
from scipy.stats import spearmanr, chi2_contingency

study_data_path = "/Users/berinayzumrasariel/Desktop/DSA210 TERM PROJECT/Cleaned_and_Adjusted_Study_Data.csv"
insta_data_path = "/Users/berinayzumrasariel/Desktop/extracted_likes_timestamps.csv"

study_data = pd.read_csv(study_data_path)
insta_data = pd.read_csv(insta_data_path, header=None, names=["timestamp"])

study_data["Start Time"] = pd.to_datetime(study_data["Start Time"], errors="coerce").dt.tz_localize(None)
study_data["End Time"] = pd.to_datetime(study_data["End Time"], errors="coerce").dt.tz_localize(None)
insta_data["timestamp"] = pd.to_datetime(insta_data["timestamp"], errors="coerce").dt.tz_localize(None)

academic_periods = {
    "Oct 2024 - Now": ["CS204", "MATH204", "HUM201", "DSA210", "NS206", "ECON202"],
    "Feb 2024 - June 2024": ["MATH201", "MATH203", "ENS208", "CS201", "PSY201"],
    "Before Feb 2024": ["TLL102", "SPS102", "NS102", "MATH102"],
}
academic_period_dates = {
    "Oct 2024 - Now": ("2024-10-01", insta_data["timestamp"].max()),
    "Feb 2024 - June 2024": ("2024-02-01", "2024-06-30"),
    "Before Feb 2024": ("2022-09-01", "2024-01-31"), }

results = []

pd.set_option('display.max_columns', None)  
pd.set_option('display.width', 1000)       

for period_name, tags in academic_periods.items():
    start_date, end_date = map(pd.Timestamp, academic_period_dates[period_name])

    period_study = study_data.loc[
        (study_data["Start Time"] >= start_date) &
        (study_data["Start Time"] <= end_date) &
        (study_data["Tag"].isin(tags))  ]

    period_insta = insta_data.loc[
        (insta_data["timestamp"] >= start_date) &
        (insta_data["timestamp"] <= end_date)  ]

    daily_study = period_study.groupby(period_study["Start Time"].dt.date)["Duration (hours)"].sum()
    daily_insta = period_insta.groupby(period_insta["timestamp"].dt.date).size()

 
    combined_data = pd.DataFrame({
        "Study Hours": daily_study,
        "Instagram Usage": daily_insta
    }).fillna(0)

    if len(combined_data) > 1:  
        correlation, corr_p_value = spearmanr(combined_data["Study Hours"], combined_data["Instagram Usage"])
    else:
        correlation, corr_p_value = None, None

    # Chi-Square Test
    if not daily_study.empty and not daily_insta.empty:
   
        study_median = daily_study.median()
        insta_median = daily_insta.median()

        daily_study_category = daily_study.apply(lambda x: "High" if x >= study_median else "Low")
        daily_insta_category = daily_insta.apply(lambda x: "High" if x >= insta_median else "Low")

        contingency_table = pd.crosstab(daily_study_category, daily_insta_category)

        if contingency_table.shape == (2, 2):  
            chi2, chi_p_value, _, _ = chi2_contingency(contingency_table)
        else:
            chi2, chi_p_value = None, None
    else:
        chi2, chi_p_value = None, None

    results.append({
        "Period": period_name,
        "Spearman Correlation": correlation,
        "Correlation P-value": corr_p_value,
        "Chi-Square": chi2,
        "Chi-Square P-value": chi_p_value
    })

results_df = pd.DataFrame(results)
print(results_df)
