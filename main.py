import streamlit as st
import pandas as pd
import numpy as np
import random

# Set average CTR values by position
avg_ctr_by_position = {1: (30, 35), 2: (15, 18), 3: (10, 12), 4: (7, 9), 5: (5, 7), 6: (4, 6), 7: (3, 5),
                       8: (3, 4), 9: (2, 3), 10: (2, 3)}

for i in range(11, 21):
    avg_ctr_by_position[i] = (1, 2)

for i in range(21, 31):
    avg_ctr_by_position[i] = (0.5, 1)

for i in range(31, 41):
    avg_ctr_by_position[i] = (0.4, 0.8)

for i in range(41, 51):
    avg_ctr_by_position[i] = (0.3, 0.7)

for i in range(51, 61):
    avg_ctr_by_position[i] = (0.2, 0.6)

for i in range(61, 71):
    avg_ctr_by_position[i] = (0.2, 0.5)

for i in range(71, 81):
    avg_ctr_by_position[i] = (0.1, 0.4)

for i in range(81, 91):
    avg_ctr_by_position[i] = (0.1, 0.3)

for i in range(91, 101):
    avg_ctr_by_position[i] = (0.1, 0.2)

# Set ranking scenarios
scenarios = ['improve rankings by 1 position', 'improve all rankings by 10%', 'lift all to random page 2 positions', 
             'lift all to random page 1 positions', 'lift all to position 1']

# Set project success scenarios
project_success_scenarios = {
    "16 month minimum": [1, 2, 3, 5, 7, 15, 25, 35, 45, 50, 55, 60, 63, 66, 68, 70],
    "16 month average": [1, 3, 5, 8, 12, 25, 40, 55, 70, 78, 85, 90, 92, 94, 96, 97],
    "16 month optimum": [2, 5, 8, 12, 18, 35, 55, 73, 82, 85, 94, 96, 97, 98, 99, 100]
}

# Set conversion rate ranges based on search intent
conversion_rate_ranges = {
    "transactional": (1, 5),
    "commercial": (1, 5),
    "informational": (0.01, 0.5),
    "navigational": (6, 9)
}

def validate_csv(file):
    """
    Check if a file has all the necessary columns.
    """
    required_columns = ['Keyword', 'Cluster', 'Search Intent', 'Monthly Search Volume', 
                        'Current Clicks per Month', 'Current Ranking Position', 'Current CTR']
    
    for column in required_columns:
        if column not in file.columns:
            return False, column
    return True, ""

def calculate_potential_traffic(data, scenario, success, conversion_value):
    """
    Calculate the potential traffic for each keyword cluster.
    """
    if scenario == scenarios[0]: # Improve rankings by X positions
        data['Adjusted Ranking Position'] = data['Current Ranking Position'].apply(lambda x: x-1 if x > 1 else x)
    elif scenario == scenarios[1]: # Improve all rankings by 10%
        data['Adjusted Ranking Position'] = data['Current Ranking Position'].apply(lambda x: x*0.9 if x > 1 else x)
    elif scenario == scenarios[2]: # Lift all to random page 2 position
        data['Adjusted Ranking Position'] = data['Current Ranking Position'].apply(lambda x: random.randint(11,20) if x > 20 else x)
    elif scenario == scenarios[3]: # Lift all to random page 1 position
        data['Adjusted Ranking Position'] = data['Current Ranking Position'].apply(lambda x: random.randint(1,10) if x > 10 else x)
    elif scenario == scenarios[4]: # Lift all to position 1
        data['Adjusted Ranking Position'] = data['Current Ranking Position'].apply(lambda x: 1)

    data['Potential CTR'] = data['Adjusted Ranking Position'].apply(lambda x: avg_ctr_by_position.get(min(round(max(1, x)), 10), 0))
    data['Potential Traffic'] = data['Potential CTR'] * data['Monthly Search Volume']
    data['Potential Conversion'] = data['Potential Traffic'] * data['Conversion Rate']
    data['Potential Conversion Value'] = data['Potential Conversion'] * conversion_value
    data['Success Scenario'] = success
    return data

# App title
st.title('SEO Potential Analyzer')
st.write('Please upload a CSV file containing the following columns: Keyword, Cluster, Search Intent, Monthly Search Volume, Current Clicks per Month, Current Ranking Position, and Current CTR.')

# CSV file upload
uploaded_file = st.file_uploader('')

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)

    # Data validation
    is_valid, missing_column = validate_csv(data)
    
    if not is_valid:
        st.error(f'Missing column: {missing_column}')
    else:
        st.write(data)

        # Dropdowns and selectors
        cluster = st.multiselect('Cluster for improvement', data['Cluster'].unique().tolist() + ['all keywords'])
        scenario = st.selectbox('Ranking Scenario', scenarios)
        success = st.selectbox('Project Success', list(project_success_scenarios.keys()))
        conversion_value = st.number_input('Average value of a conversion in €', value=0.0)

        # Data processing button
        if st.button('Run analysis'):
            data['Search Intent'] = data['Search Intent'].apply(lambda x: conversion_rate_ranges.get(x, (0, 0)))
            data['Conversion Rate'] = data.apply(lambda row: np.random.uniform(row['Search Intent'][0], row['Search Intent'][1]) / 100, axis=1)

            # Subset the data if a cluster is selected
            if 'all keywords' not in cluster:
                data = data[data['Cluster'].isin(cluster)]

            success_scenario = project_success_scenarios[success]
    
            # Iterate over each month in the success scenario
            for i, success_rate in enumerate(success_scenario):
                # Calculate potential traffic
                month_data = calculate_potential_traffic(data, scenario, success_rate, conversion_value)
        
                # Store month data
                month_data.to_csv(f'output_month_{i+1}.csv', index=False)

            st.success('Analysis complete. Please check your directory for the output files.')
