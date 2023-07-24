import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import random

# Customize the layout
st.set_page_config(page_title="SEO-Potential-Analysis", page_icon="🤖", layout="wide", )     
st.markdown(f"""
            <style>
            .stApp {{background-image: url("https://images.unsplash.com/photo-1509537257950-20f875b03669?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1469&q=80"); 
                     background-attachment: fixed;
                     background-size: cover}}
         </style>
         """, unsafe_allow_html=True)

# The list of improvement scenarios
scenarios = [
    "Improve rankings by X positions", 
    "Improve all rankings by 10%", 
    "Lift all to random page 2 position",
    "Lift all to random page 1 position",
    "Lift all to position 1"
]

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

    data['Potential CTR'] = data.apply(lambda x: max(x['Current CTR per Keyword for the Website'], avg_ctr_by_position.get(min(round(max(1, x['Adjusted Ranking Position'])), 10), 0)), axis=1)
    data['Potential Traffic'] = data['Potential CTR'] * data['Monthly Search Volume per Keyword']
    return data

def main():
    st.title('SEO Potential Analyzer')
    st.write('Please upload your CSV file below. The file should contain the following columns: Keyword, Keyword Cluster, Monthly Search Volume per Keyword, Current Clicks per Month for this Website, Current Ranking Position, Current CTR per Keyword for the Website.')

    uploaded_file = st.file_uploader("Choose a CSV file", type='csv')

    if uploaded_file is not None:
        try:
            data = pd.read_csv(uploaded_file)

            expected_columns = [
                "Keyword", 
                "Keyword Cluster", 
                "Monthly Search Volume per Keyword", 
                "Current Clicks per Month for this Website", 
                "Current Ranking Position", 
                "Current CTR per Keyword for the Website"
            ]
            
            if not all(col in data.columns for col in expected_columns):
                st.error("CSV file must contain the following columns: " + ', '.join(expected_columns))
                return

            scenario = st.selectbox('Select an improvement scenario', scenarios)
            ctr_source = st.selectbox('Select a CTR source', ctr_sources)

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
            months = np.arange(1, 25)  # 2 years
            current_traffic_per_month = [current_traffic] * len(months)

            fig, ax = plt.subplots()
            ax.plot(months, current_traffic_per_month, label='Current Traffic')

            for goal_months in [6, 12, 24]:
                potential_traffic_per_month = [current_traffic + ((potential_traffic - current_traffic) / goal_months) * min(i, goal_months) for i in months]
                ax.plot(months, potential_traffic_per_month, label=f'Goal achieved in {goal_months} months', linestyle='--')
            
            ax.set_xlabel('Month')
            ax.set_ylabel('Traffic')
            ax.set_title('Improvement Trajectory of Traffic')
            ax.legend()
            
            plt.tight_layout()
            st.pyplot(fig)
            
        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
