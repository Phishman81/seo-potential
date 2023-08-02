
import streamlit as st
import pandas as pd
import numpy as np
import random

st.set_option('deprecation.showfileUploaderEncoding', False)

# Define the ranking scenarios and project duration scenarios
ranking_scenarios = {
    'Improve each ranking by 1 position': lambda x: x-1 if x > 1 else x,
    'Lift all positions > 20 to random page 2 positions': lambda x: random.randint(11,20) if x > 20 else x,
    'Lift all rankings to random positions 2-5': lambda x: random.randint(2,5) if x > 5 else x,
    'Lift all rankings to random positions 1-3': lambda x: random.randint(1,3) if x > 3 else x,
    'Lift all to random page 1 positions': lambda x: random.randint(1,10) if x > 10 else x,
    'Lift all to position 1': lambda x: 1 if x > 1 else x,
}

project_duration_scenarios = {
    "6 months scenario": [15,35, 65, 74, 87, 100],
    "12 month scenario": [1, 3, 5, 8, 12, 25, 40, 55, 70, 78, 85, 100],
    "18 month scenario": [2, 5, 8, 12, 18, 35, 42, 54, 67, 72, 77, 81, 87, 90, 93, 95,97,100],
    "24 month scenario": [2, 5, 8, 12, 18, 35, 55, 62, 66, 72, 77, 83, 85, 88,90, 91,92,93,94,95,96,98,99,100],
}

ctr_ranges = {
    range(1, 2): [30, 35],
    range(2, 3): [15, 18],
    range(3, 4): [10, 12],
    range(4, 5): [7, 9],
    range(5, 6): [5, 7],
    range(6, 7): [4, 6],
    range(7, 8): [3, 5],
    range(8, 9): [3, 4],
    range(9, 11): [2, 3],
    range(11, 21): [1, 2],
    range(21, 31): [0.5, 1],
    range(31, 41): [0.4, 0.8],
    range(41, 51): [0.3, 0.7],
    range(51, 61): [0.2, 0.6],
    range(61, 71): [0.2, 0.5],
    range(71, 81): [0.1, 0.4],
    range(81, 91): [0.1, 0.3],
    range(91, 101): [0.1, 0.2]
}

# Streamlit app layout
st.title("SEO Potential Analyzer")
st.markdown("""
Please upload a CSV file containing at least the following columns: 
- Keyword
- Search Volume
- Clicks
- Position
""")
uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    required_columns = {'Keyword', 'Search Volume', 'Clicks', 'Position'}

    if set(data.columns) & required_columns != required_columns:
        st.error('The uploaded file does not have the necessary columns.')
    else:
        data = data[list(required_columns)]

        scenario = st.selectbox("Ranking Scenario", list(ranking_scenarios.keys()))
        duration = st.selectbox("Project Duration", list(project_duration_scenarios.keys()))
        avg_conv_rate = st.number_input("Average Conversion Rate %", 0.0, 100.0, 2.5, 0.1)

        if st.button("Run Analysis"):
            data['Future Position'] = data['Position'].apply(ranking_scenarios[scenario])
            data['Future CTR'] = data['Future Position'].apply(lambda x: np.mean(ctr_ranges[next((r for r in ctr_ranges if x in r), range(91, 101))]) / 100)
            data['Future Clicks'] = (data['Search Volume'] * data['Future CTR']).astype(int)
            data['Current Conversions'] = (data['Clicks'] * (avg_conv_rate / 100)).astype(int)
            data['Future Conversions'] = (data['Future Clicks'] * (avg_conv_rate / 100)).astype(int)

            for month, percentage in enumerate(project_duration_scenarios[duration], start=1):
                data[f'Month {month} Clicks'] = (data['Clicks'] + (data['Future Clicks'] - data['Clicks']) * (percentage / 100)).astype(int)

            st.dataframe(data)

            st.markdown("### Total Current Clicks")
            st.bar_chart(data['Clicks'])

            st.markdown("### Total Future Clicks")
            st.bar_chart(data['Future Clicks'])

            st.markdown("### Total Current Conversions")
            st.bar_chart(data['Current Conversions'])

            st.markdown("### Total Future Conversions")
            st.bar_chart(data['Future Conversions'])

            st.markdown("### Clicks Over Time")
            st.line_chart(data[[f'Month {i} Clicks' for i in range(1, len(project_duration_scenarios[duration])+1)]])
