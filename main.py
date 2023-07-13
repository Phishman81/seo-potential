# main.py

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# The list of improvement scenarios
scenarios = ["Improve rankings by X positions", "Improve all rankings by X%"]

# The list of CTR sources
ctr_sources = ["Source 1", "Source 2", "Source 3"]

# Function to get CTR by position based on source
def get_ctr_by_position(ctr_source):
    if ctr_source == "Source 1":
        return {
            1: 0.35,
            2: 0.25,
            3: 0.20,
            4: 0.15,
            5: 0.10,
            6: 0.08,
            7: 0.06,
            8: 0.04,
            9: 0.03,
            10: 0.02
        }
    elif ctr_source == "Source 2":
        return {
            1: 0.30,
            2: 0.24,
            3: 0.18,
            4: 0.14,
            5: 0.11,
            6: 0.07,
            7: 0.06,
            8: 0.05,
            9: 0.03,
            10: 0.02
        }
    elif ctr_source == "Source 3":
        return {
            1: 0.32,
            2: 0.26,
            3: 0.21,
            4: 0.15,
            5: 0.10,
            6: 0.06,
            7: 0.04,
            8: 0.03,
            9: 0.02,
            10: 0.01
        }

# Calculate potential traffic based on scenario
def calculate_potential_traffic_based_on_scenario(data, scenario, avg_ctr_by_position):
    data['Adjusted Ranking Position'] = data['Current Ranking Position'].apply(lambda x: x-1 if scenario == scenarios[0] else x*0.9 if scenario == scenarios[1] else x)
    data['Potential CTR'] = data['Adjusted Ranking Position'].apply(lambda x: avg_ctr_by_position[min(round(x), 10)])
    data['Potential Traffic'] = data['Potential CTR'] * data['Monthly Search Volume per Keyword']
    return data

def main():
    st.title('SEO Potential Analyzer')
    st.write('Please upload your CSV file below. The file should contain the following columns: Keyword, Keyword Cluster, Monthly Search Volume per Keyword, Current Clicks per Month for this Website, Current Ranking Position, Current CTR per Keyword for the Website.')

    uploaded_file = st.file_uploader("Choose a CSV file", type='csv')

    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)

        scenario = st.selectbox(
            'Select an improvement scenario',
            scenarios
        )

        ctr_source = st.selectbox(
            'Select a CTR source',
            ctr_sources
        )

        avg_ctr_by_position = get_ctr_by_position(ctr_source)
        
        data = calculate_potential_traffic_based_on_scenario(data, scenario, avg_ctr_by_position)

        st.dataframe(data)
        
        st.subheader('Total Current Traffic')
        st.write(data['Current Clicks per Month for this Website'].sum())
        
        st.subheader('Total Potential Traffic')
        st.write(data['Potential Traffic'].sum())

        fig, ax = plt.subplots()

        index = np.arange(len(data))
        bar_width = 0.35

        opacity = 0.8
        rects1 = plt.bar(index, data['Current Clicks per Month for this Website'], bar_width,
        alpha=opacity,
        color='b',
        label='Current Traffic')

        rects2 = plt.bar(index + bar_width, data['Potential Traffic'], bar_width,
        alpha=opacity,
        color='g',
        label='Potential Traffic')

        plt.xlabel('Keywords')
        plt.ylabel('Traffic')
        plt.title('Current vs Potential Traffic')
        plt.xticks(index + bar_width, data['Keyword'], rotation=90)
        plt.legend()

        plt.tight_layout()
        st.pyplot(fig)

if __name__ == "__main__":
    main()
