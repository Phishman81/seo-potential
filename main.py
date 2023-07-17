import streamlit as st
import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt

# The list of improvement scenarios
scenarios = [
    "Improve rankings by 1 position", 
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

# Calculate potential traffic based on scenario
def calculate_potential_traffic_based_on_scenario(data, scenario, avg_ctr_by_position):
    if scenario == scenarios[0]: # Improve rankings by 1 position
        data['Adjusted Ranking Position'] = data['Current Ranking Position'].apply(lambda x: x-1 if x > 1 else x)
    elif scenario == scenarios[1]: # Improve all rankings by 10%
        data['Adjusted Ranking Position'] = data['Current Ranking Position'].apply(lambda x: x*0.9 if x > 1 else x)
    elif scenario == scenarios[2]: # Lift all to random page 2 position
        data['Adjusted Ranking Position'] = data['Current Ranking Position'].apply(lambda x: random.randint(11,20) if x > 20 else x)
    elif scenario == scenarios[3]: # Lift all to random page 1 position
        data['Adjusted Ranking Position'] = data['Current Ranking Position'].apply(lambda x: random.randint(1,10) if x > 10 else x)
    elif scenario == scenarios[4]: # Lift all to position 1
        data['Adjusted Ranking Position'] = data['Current Ranking Position'].apply(lambda x: 1)
    elif scenario == scenarios[5]: # Improve all page 3 rankings to random page 2 rankings
        data['Adjusted Ranking Position'] = data['Current Ranking Position'].apply(lambda x: random.randint(11,20) if x > 20 and x <= 30 else x)
    elif scenario == scenarios[6]: # Lift all (higher than page 2) to random page 2 rankings
        data['Adjusted Ranking Position'] = data['Current Ranking Position'].apply(lambda x: random.randint(11,20) if x > 20 else x)
    elif scenario == scenarios[7]: # Improve all rankings by 20%
        data['Adjusted Ranking Position'] = data['Current Ranking Position'].apply(lambda x: x*0.8 if x > 1 else x)
    elif scenario == scenarios[8]: # Improve all rankings by 50%
        data['Adjusted Ranking Position'] = data['Current Ranking Position'].apply(lambda x: x*0.5 if x > 1 else x)
    elif scenario == scenarios[9]: # Lift all to positions 2 - 5
        data['Adjusted Ranking Position'] = data['Current Ranking Position'].apply(lambda x: random.randint(2,5) if x > 5 else x)
    elif scenario == scenarios[10]: # Lift all to positions 1 - 3
        data['Adjusted Ranking Position'] = data['Current Ranking Position'].apply(lambda x: random.randint(1,3) if x > 3 else x)
    
    data['Potential CTR'] = data['Adjusted Ranking Position'].apply(lambda x: avg_ctr_by_position[min(round(x), 10)])
    data['Potential Traffic'] = data['Potential CTR'] * data['Monthly Search Volume per Keyword']
    return data

def main():
    st.title("SEO Potential Calculator")

    file = st.file_uploader("Upload file", type=['csv'])
    if file is not None:
        data = pd.read_csv(file)
        st.dataframe(data.head())
        
        # Check if required columns exist
        if not all(item in data.columns for item in ['Keyword', 'Current Ranking Position', 'Monthly Search Volume per Keyword']):
            st.error("Required columns not found in the data. Please make sure the following columns exist in your CSV: Keyword, Current Ranking Position, Monthly Search Volume per Keyword")
            return

        scenario = st.selectbox("Select an Improvement Scenario", scenarios)
        
        run_button = st.button('Run analysis')
        if run_button:

            avg_ctr_by_position = {
        1: 0.317, 2: 0.2471, 3: 0.1866, 4: 0.136, 5: 0.0951, 6: 0.0623, 7: 0.04, 8: 0.03, 9: 0.02, 10: 0.02,
        **dict.fromkeys(range(11, 21), 0.015),
        **dict.fromkeys(range(21, 31), 0.01),
        **dict.fromkeys(range(31, 41), 0.008),
        **dict.fromkeys(range(41, 51), 0.007),
        **dict.fromkeys(range(51, 61), 0.006),
        **dict.fromkeys(range(61, 71), 0.005),
        **dict.fromkeys(range(71, 81), 0.004),
        **dict.fromkeys(range(81, 91), 0.003),
        **dict.fromkeys(range(91, 101), 0.002)
    }

            data['Current CTR'] = data['Current Ranking Position'].apply(lambda x: avg_ctr_by_position[min(round(x), 10)])
            data['Current Traffic'] = data['Current CTR'] * data['Monthly Search Volume per Keyword']

            data = calculate_potential_traffic_based_on_scenario(data, scenario, avg_ctr_by_position)
            data['Traffic Difference'] = data['Potential Traffic'] - data['Current Traffic']

            st.dataframe(data)

            fig, ax = plt.subplots()
            ax.hist(data['Traffic Difference'], bins=30, alpha=0.75)
            ax.set_xlabel('Traffic Difference')
            ax.set_ylabel('Number of Keywords')
            ax.set_title('Histogram of Traffic Differences')
            plt.show()
            st.pyplot(fig)

if __name__ == "__main__":
    main()
    
