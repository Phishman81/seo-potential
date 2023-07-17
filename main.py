import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import random

# The list of improvement scenarios
scenarios = [
    "Improve rankings by X positions", 
    "Improve all rankings by 10%", 
    "Lift all to random page 2 position",
    "Lift all to random page 1 position",
    "Lift all to position 1",
    "Improve all page 3 rankings to random page 2 rankings",
    "Lift all (higher than page 2) to random page 2 rankings",
    "Improve all rankings by 20%",
    "Improve all rankings by 50%",
    "Lift all to positions 2 - 5",
    "Lift all to positions 1 - 3"
]

# The list of CTR sources
ctr_sources = ["Source 1", "Source 2", "Source 3"]

# SEO Growth scenarios
seo_growth_scenarios = {
    "Minimum": [2, 5, 10, 18, 28, 40, 55, 62, 69, 75, 79, 82, 85, 86, 87, 88],
    "Average": [1, 3, 6, 12, 20, 33, 50, 62, 70, 76, 80, 83, 85, 87, 89, 90],
    "Optimum": [0, 2, 5, 11, 20, 33, 50, 67, 80, 90, 95, 97, 99, 100, 100, 100]
}

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
    # Scenario calculations
    # Implement your scenarios here
    # ...
    
    data['Potential CTR'] = data['Adjusted Ranking Position'].apply(lambda x: avg_ctr_by_position[min(round(x), 10)])
    data['Potential Traffic'] = data['Potential CTR'] * data['Monthly Search Volume per Keyword']
    return data

def main():
    st.title('SEO Potential Analyzer')
    st.write('Please upload your CSV file below. The file should contain the following columns: Keyword, Keyword Cluster, Monthly Search Volume per Keyword, Current Clicks per Month for this Website, Current Ranking Position, Current CTR per Keyword for the Website.')

    uploaded_file = st.file_uploader("Choose a CSV file", type='csv')

    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)

        scenario = st.selectbox('Select an improvement scenario', scenarios)
        ctr_source = st.selectbox('Select a CTR source', ctr_sources)
        seo_growth_scenario = st.selectbox('Select an SEO growth scenario', list(seo_growth_scenarios.keys()))

        if st.button('Run analysis'):
            avg_ctr_by_position = get_ctr_by_position(ctr_source)
            data = calculate_potential_traffic_based_on_scenario(data, scenario, avg_ctr_by_position)

            st.dataframe(data)
            
            current_traffic = data['Current Clicks per Month for this Website'].sum()
            potential_traffic = data['Potential Traffic'].sum()

            st.subheader('Total Current Traffic vs. Total Potential Traffic')
            st.bar_chart(pd.DataFrame({'Traffic': [current_traffic, potential_traffic]}, index=['Current', 'Potential']))
            
            st.subheader('Traffic by Keyword Cluster')
            cluster_data = data.groupby('Keyword Cluster').sum()[['Current Clicks per Month for this Website', 'Potential Traffic']]
            st.bar_chart(cluster_data)

            st.subheader('Improvement Trajectory')
            months = np.arange(1, 17)  # 16 months
            current_traffic_per_month = [current_traffic] * len(months)

            fig, ax = plt.subplots()
            ax.plot(months, current_traffic_per_month, label='Current Traffic')

            potential_traffic_per_month = [current_traffic + ((potential_traffic - current_traffic) * (seo_growth_scenarios[seo_growth_scenario][i] / 100)) for i in range(len(months))]

            ax.plot(months, potential_traffic_per_month, label=f'Potential Traffic ({seo_growth_scenario})', linestyle='--')
            ax.set_xlabel('Month')
            ax.set_ylabel('Traffic')
            ax.set_title('Improvement Trajectory of Traffic')
            ax.legend()

            plt.tight_layout()
            st.pyplot(fig)

if __name__ == "__main__":
    main()
