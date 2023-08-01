import streamlit as st
import pandas as pd
import random
import numpy as np
import matplotlib.pyplot as plt

# Define CTR ranges for each position
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

# Function to get CTR for a given position
def get_ctr(position):
    for r in ctr_ranges:
        if position in r:
            return random.uniform(ctr_ranges[r][0], ctr_ranges[r][1])
    return 0

# Project duration scenarios
project_duration_scenarios = {
    "6 months": {f'Month {i+1}': val for i, val in enumerate([15, 35, 65, 74, 87, 100])},
    "12 months": {f'Month {i+1}': val for i, val in enumerate([1, 3, 5, 8, 12, 25, 40, 55, 70, 78, 85, 100])},
    "18 months": {f'Month {i+1}': val for i, val in enumerate([2, 5, 8, 12, 18, 35, 42, 54, 67, 72, 77, 81, 87, 90, 93, 95, 97, 100])},
    "24 months": {f'Month {i+1}': val for i, val in enumerate([2, 5, 8, 12, 18, 35, 55, 62, 66, 72, 77, 83, 85, 88, 90, 91, 92, 93, 94, 95, 96, 98, 99, 100])},
}

st.title('SEO Potential Analyzer')
st.write('Upload a CSV file containing at least the following columns: Keyword, Search Volume, Clicks, Position')

uploaded_file = st.file_uploader("Upload CSV", type=['csv'])

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    columns = data.columns.tolist()

    # Check if required columns are present
    required_columns = ['Keyword', 'Search Volume', 'Clicks', 'Position']
    if all(item in columns for item in required_columns):
        data = data[required_columns]
        st.write(data)
    else:
        st.error('The uploaded CSV file does not contain the required columns.')
        st.stop()

    scenario = st.selectbox('Ranking Scenario', options = ['Improve rankings by 1 position', 'Lift all to random page 2 position', 
    'Lift all rankings to random positions 2-5', 'Lift all rankings to random positions 1-3', 
    'Lift all to random page 1 positions', 'Lift all to position 1'])

    if scenario == 'Improve rankings by 1 position':
        data['Future Position'] = data['Position'].apply(lambda x: x-1 if x > 1 else x)
    
    elif scenario == 'Lift all to random page 2 position':
        data['Future Position'] = data['Position'].apply(lambda x: random.randint(11,20) if x > 20 else x)
        
    # Add your own scenarios here...

    duration = st.selectbox('Project Duration', options = list(project_duration_scenarios.keys()))

    conversion_rate = st.number_input('Average Conversion Rate %', min_value=0.0, max_value=100.0, step=0.01)
    data['Current Conversions'] = data['Clicks'] * conversion_rate / 100

    run_button = st.button('Run Analysis')
    
    if run_button:
        scenario_data = project_duration_scenarios[duration]
        for month, improvement in scenario_data.items():
            data[month] = data['Future Position'] * (1 + improvement / 100)

        # Calculate future data
        data['Future CTR'] = data['Future Position'].apply(get_ctr)
        data['Future Clicks'] = data['Search Volume'] * data['Future CTR'] / 100
        data['Future Conversions'] = data['Future Clicks'] * conversion_rate / 100

        # Display the data
        st.write(data)

        # Plot the graphs
        st.bar_chart(data[['Clicks', 'Future Clicks']])
        st.bar_chart(data[['Current Conversions', 'Future Conversions']])
        st.line_chart(data['Future Clicks'].cumsum())
