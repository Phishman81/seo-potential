import streamlit as st
import pandas as pd
import numpy as np
import random

# Define the ranking scenarios
ranking_scenarios = {
    'improve each ranking by 1 position': lambda x: x-1 if x > 1 else x,
    'lift all positions > 20 to random page 2 positions': lambda x: random.randint(11,20) if x > 20 else x,
    'lift all rankings to random positions 2-5': lambda x: random.randint(2,5) if x > 5 else x,
    'lift all rankings to random positions 1-3': lambda x: random.randint(1,3) if x > 3 else x,
    'lift all to random page 1 positions': lambda x: random.randint(1,10) if x > 10 else x,
    'lift all to position 1': lambda x: 1 if x != 1 else x
}

# Define the project duration scenarios
project_duration_scenarios = {
    "6 months scenario": [15,35, 65, 74, 87, 100],
    "12 month scenario": [1, 3, 5, 8, 12, 25, 40, 55, 70, 78, 85, 100],
    "18 month scenario": [2, 5, 8, 12, 18, 35, 42, 54, 67, 72, 77, 81, 87, 90, 93, 95,97,100],
    "24 month scenario": [2, 5, 8, 12, 18, 35, 55, 62, 66, 72, 77, 83, 85, 88,90, 91,92,93,94,95,96,98,99,100]
}

# Define the CTR ranges for each position
ctr_ranges = {
    range(1, 2): (30, 35),
    range(2, 3): (15, 18),
    range(3, 4): (10, 12),
    range(4, 5): (7, 9),
    range(5, 6): (5, 7),
    range(6, 7): (4, 6),
    range(7, 8): (3, 5),
    range(8, 9): (3, 4),
    range(9, 11): (2, 3),
    range(11, 21): (1, 2),
    range(21, 31): (0.5, 1),
    range(31, 41): (0.4, 0.8),
    range(41, 51): (0.3, 0.7),
    range(51, 61): (0.2, 0.6),
    range(61, 71): (0.2, 0.5),
    range(71, 81): (0.1, 0.4),
    range(81, 91): (0.1, 0.3),
    range(91, 101): (0.1, 0.2)
}

# Create the app title and instructions
st.title("SEO Potential Analyzer")
st.write("Please upload a CSV file with at least the following columns: Keyword, Search Volume, Clicks, Position")

# Create the file uploader and read the uploaded file
uploaded_file = st.file_uploader("Upload CSV", type=['csv'])
if uploaded_file is not None:
    try:
        data = pd.read_csv(uploaded_file, on_bad_lines='warn')
    except Exception as e:
        st.error(f"Error reading file: {e}")

if 'data' in locals():
    # Check that the required columns are present
    required_columns = {'Keyword', 'Search Volume', 'Clicks', 'Position'}
    if set(data.columns) & required_columns == required_columns:
        data = data[list(required_columns)]

        # Get user input for ranking scenario, project duration and average conversion rate
        scenario = st.selectbox("Ranking Scenario", list(ranking_scenarios.keys()))
        duration = st.selectbox("Project Duration", list(project_duration_scenarios.keys()))
        avg_conv_rate = st.number_input("Average Conversion Rate %", min_value=0.0, max_value=100.0)

        # Define a button to start the analysis
        if st.button('Start Analysis'):
            # Apply the selected ranking scenario to calculate the future position
            data['Future Position'] = data['Position'].apply(ranking_scenarios[scenario])
            # Calculate the CTR for the future position
            data['Future CTR'] = data['Future Position'].apply(lambda x: np.mean(ctr_ranges[next((r for r in ctr_ranges if x in r), range(91, 101))]) / 100)
            # Calculate the future clicks based on the future CTR and search volume
            data['Future Clicks'] = (data['Search Volume'] * data['Future CTR']).astype(int)
            # Calculate the current and future conversions based on the clicks and average conversion rate
            data['Current Conversions'] = (data['Clicks'] * (avg_conv_rate / 100)).astype(int)
            data['Future Conversions'] = (data['Future Clicks'] * (avg_conv_rate / 100)).astype(int)
            # Calculate the additional conversions and additional revenue
            data['Additional Conversions'] = data['Future Conversions'] - data['Current Conversions']

            # Calculate the clicks for each month
            for month, percentage in enumerate(project_duration_scenarios[duration], start=1):
                data[f'Month {month}'] = (data['Clicks'] + (data['Future Clicks'] - data['Clicks']) * (percentage / 100)).astype(int)

            # Display the resulting DataFrame
            st.dataframe(data)

    else:
        st.error("The uploaded file doesn't contain the required columns.")
