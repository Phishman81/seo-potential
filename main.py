import pandas as pd
import streamlit as st
import numpy as np
import random

# Customize the layout
st.set_page_config(page_title="SEO-Potential-Analysis", page_icon="🤖", layout="wide", )     
st.markdown(f"""
            <style>
            .stApp {{background-image: url("https://images.unsplash.com/photo-1509537257950-20f875b03669?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fGVufDB8fHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1469&q=80"); 
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

# Function to get CTR by position
def get_ctr_by_position():
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

# Calculate potential traffic based on scenario
def calculate_potential_traffic_based_on_scenario(data, scenario, avg_ctr_by_position, monthly_rates):
    monthly_projections = pd.DataFrame()

    for month, rate in zip(range(1, 25), monthly_rates):  # 24 months
        if scenario == scenarios[0]: # Improve rankings by X positions
            data['Adjusted Ranking Position'] = np.maximum(data['Current Ranking Position'] - (data['Current Ranking Position'] - 1) * rate, 1)
        elif scenario == scenarios[1]: # Improve all rankings by 10%
            data['Adjusted Ranking Position'] = np.maximum(data['Current Ranking Position'] - (data['Current Ranking Position'] * 0.9) * rate, 1)
        elif scenario == scenarios[2]: # Lift all to random page 2 position
            data['Adjusted Ranking Position'] = np.maximum(data['Current Ranking Position'] - (data['Current Ranking Position'] - random.randint(11,20)) * rate, 1)
        elif scenario == scenarios[3]: # Lift all to random page 1 position
            data['Adjusted Ranking Position'] = np.maximum(data['Current Ranking Position'] - (data['Current Ranking Position'] - random.randint(1,10)) * rate, 1)
        elif scenario == scenarios[4]: # Lift all to position 1
            data['Adjusted Ranking Position'] = np.maximum(data['Current Ranking Position'] - (data['Current Ranking Position'] - 1) * rate, 1)

        data['Potential CTR'] = data['Adjusted Ranking Position'].apply(lambda x: avg_ctr_by_position.get(min(round(x), 10), 0))
        data['Potential Traffic'] = data['Potential CTR'] * data['Monthly Search Volume per Keyword']
        
        new_monthly_projection = pd.DataFrame({
            'Month': [month],
            'Total Potential Traffic': [data['Potential Traffic'].sum()]
        })
        
        monthly_projections = monthly_projections.append(new_monthly_projection, ignore_index=True)

    return monthly_projections

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

            avg_ctr_by_position = get_ctr_by_position()
            # Define manual monthly improvement rates over 24 months
            monthly_rates = [
                0.05, 0.07, 0.09, 0.10, 0.12, 0.14,
                0.16, 0.20, 0.24, 0.28, 0.30, 0.35,
                0.40, 0.44, 0.48, 0.52, 0.55, 0.60,
                0.65, 0.70, 0.75, 0.80, 0.85, 1.00
            ]
            monthly_projections = calculate_potential_traffic_based_on_scenario(data, scenario, avg_ctr_by_position, monthly_rates)

            st.dataframe(monthly_projections)

        except Exception as e:
            st.error(f'Error reading file: {e}')
        
if __name__ == "__main__":
    main()
