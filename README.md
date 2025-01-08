# DSA210 Term Project
In this term project, I will be exploring the relationship with my Instagram usage level and my focused hours.

I am Berinay Zümra Sarıel, a DSA210 student who will conduct this term project about the relationship between her social media usage and study focus time. 

You can check my slides [here](https://drive.google.com/file/d/1cncEdrTo5SlBQsEB7A_PjHZbTbTxttrI/view?usp=sharing) to have a general perspective about my project. 


## Table of Contents
**[Motivation](#Motivation)**  

**[Project Idea](#Project-Idea)**

**[Data Source](#Data-Source)** 

**[Project Plan](#Project-Plan)** 

**[Findings](#Findings)** 





## Motivation

As it is a commonly known issue, social media useage has an adverse effect on one's productivity and focus time. By analyzing these two datasets together, I hope to gain valuable insights into how distractions influence my academic performance and identify patterns that can help me improve my time management.




## Project Idea

The goal of this project is to determine whether there is a relationship between my Instagram activity and study focus time throughout my last three academic semesters. Specifically:

1. I analyzed my **Instagram likes activity** to measure how active I am on the platform each day. (The reason why I did not go with the activity time is because of the requested data did not contain such a collection of total hours spent on a daily basis.)
2. I used my **Forest app study sessions** to track the number of hours I spent studying on the same days.
   
3. By comparing these two datasets day by day and hour by hour, I aimed to test my two null hypotheses:  
   a. Hourly Correlation: There is no monotonic relationship between hourly study hours and Instagram usage, especially in last 3 semesters.
   b. Daily Correlation: There is no monotonic relationship between daily study hours and Instagram usage, in last 3 semesters.


## Data Source

1. **Forest App**
   I have exported my focus session data from the app, which spans my whole  university time period of studying. I have tracked the duration of study sessions and timestamps for when they occurred. I have requested to export my personal data from the  [Forest app](https://www.forestapp.cc/) from my phone.
   Data includes:
   - Start and end times of the study sessions.
   - Durations of each study session.
   - Metadata such as the type of tree I planted in the app (for fun context). 
   

 2. **Social Media as Instagram**
    Since Instagram (or TikTok) applies to majority of the society for distraction, I chose the one that I use for this project. I have requested to export my Instagram Activity from the [app](https://apps.apple.com/us/app/instagram/id389801252).
    From that package of data, I chose to go with "Liked Posts" dataset, which contains:
    - Timestamps of likes I've given to posts or reels.
    - The associated metadata for each like (like the URL of the content and its title.)

*note: Raw data files will not be included in this repository to protect privacy and keep the repository lightweight. Only processed and anonymized data will be used for analysis. ".gitignore" will be used to ensure this.*





## Project Plan

I followed these steps to analyze the data. I used Python (PyCharm) for data analysis and visualization with Pandas, numpy, matplotlib, seaborn, and many more to achieve these steps:  

1. **Preprocessing**:
   - Parse and clean both datasets.
   - Standardize timestamps for comparison (convert to daily totals).
   - Get rid of meaningless data and randomize them into useful data.
   - Extract key features:
     - Total likes per day (Instagram dataset).
     - Total study hours per day (Forest dataset).
     - Total study attempts for each tag (course), etc.

2. **Exploratory Data Analysis (EDA)**:
   - I visualized daily Instagram activity and study time, both separately, and together in order to identify any existing patterns. 

3. **Correlation Analysis**:
   - I calculated the daily and hourly correlation between Instagram usage and study focus time to test my hypothesis of an inverse relationship.

4. **Hypothesis Testing**:
     In this part, I conducted some hypothesis testing to find out if I have rejected my null hypotheses or failed to reject. 
     - By calculating Spearman correlation values.
     - P-values.
     - Chi-Square values, etc.
  


## Findings

   You may check out my [slideshow](https://drive.google.com/file/d/1cncEdrTo5SlBQsEB7A_PjHZbTbTxttrI/view?usp=sharing) for this section, I presented and explained it at there. 
   For further details like the coding part and further insights like regression model and decision tree implementations, please check [my term project report](https://colab.research.google.com/drive/11QVhvej8JApum-wUytcw5WGwoQJU7uFy?usp=sharing) as well. My findings are well descripted and shown there. 
   



   

    
