# DSA210 Term Project
In this term project, I will be exploring the relationship with my Instagram usage level and my focused hours.

I am Berinay Zümra Sarıel, a DSA210 student who will conduct this term project about the relationship between her social media usage and study focus time. 


## Table of Contents
**[Motivation](#Motivatiom)**  

**[Project Idea](#Project-Idea)**

**[Data Source](#Data-Source)** 

**[Project Plan](#Project-Plan)** 

**[Findings](#Findings)** 

**[Limitations and Future Work](#Limitations-and-Future-Work)** 




## Motivation

As it is a commonly known issue, social media useage has an adverse effect on one's productivity and focus time. By analyzing these two datasets together, I hope to gain valuable insights into how distractions influence my academic performance and identify patterns that can help me improve my time management.




## Project Idea

The goal of this project is to determine whether there is an **inverse relationship** between my Instagram activity and study focus time throughout this semester. Specifically:
1. I will analyze my **Instagram likes activity** to measure how active I am on the platform each day. (The reason why I did not go with the activity time is because of the requested data did not contain such a collection of total hours spent on a daily basis.)
2. I will use my **Forest app study sessions** to track the number of hours I spent studying on the same days.
3. By comparing these two datasets day by day, I aim to test my hypothesis:  
   - Higher Instagram usage corresponds to lower study time (and vice versa).  
   - This may reveal patterns about how distractions like Instagram impact productivity.




## Data Source

1. **Forest App**
   I have exported my focus session data from the app, which spans my whole  university time period of studying. I have tracked the duration of study sessions and timestamps for when they occurred. I have requested to export my personal data from the  [Forest app](https://www.forestapp.cc/) from my phone.
   Data includes:
   - Start and end times of the study sessions.
   - Durations of each study session.
   - Metadata such as the type of tree I planted in the app (for fun context). 
   

 2. **Social Media as Instagram**
    Since Instagram (or TikTok) applies to majority of the society for distraction, I chose the one  that I use for this project. I have requested to export my Instagram Activity from the [app](https://apps.apple.com/us/app/instagram/id389801252).
    From that package of data, I chose to go with "Liked Posts" dataset, which contains:
    - Timestamps of likes I've given to posts or reels.
    - The associated metadata for each like (like the URL of the content and its title.)

*note: Raw data files will not be included in this repository to protect privacy and keep the repository lightweight. Only processed and anonymized data will be used for analysis. ".gitignore" will be used to ensure this.*





## Project Plan

I will follow these steps to analyze the data. I will use Python for data analysis and visualization with Pandas, numpy, matplotlib, and seaborn to achieve these steps:  

1. **Preprocessing**:
   - Parse and clean both datasets.
   - Standardize timestamps for comparison (convert to daily totals).
   - Extract key features:
     - Total likes per day (Instagram dataset).
     - Total study hours per day (Forest dataset).

2. **Exploratory Data Analysis (EDA)**:
   - Visualize daily Instagram activity and study time.
   - Identify patterns and outliers.

3. **Correlation Analysis**:
   - Calculate the correlation between Instagram usage and study focus time to test my hypothesis of an inverse relationship.

4. **Visualization**:
     Create comparative charts:
     - Line charts will show the trend of Instagram likes and study focus time over days
     - Scatter plots to show any correlation between the two variables (if exists).




## Findings

   This section will be completed after the proposal is approved and the analysis is conducted.


 
## Limitations and Future Work

   This section will be completed after the proposal is approved and the analysis is conducted. In the future, I may extend this analysis to other social media platforms like YouTube (my second mostly-used app for distraction) or explore strategies to reduce distractions.

    
