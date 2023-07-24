import pandas as pd
import streamlit as st
import numpy as np
import random

def main():
    # Set up the page
    st.set_page_config(page_title="SEO-Potential-Analysis", page_icon="🤖", layout="wide", )     
    st.title('SEO Potential Analyzer')
    st.write('Please upload your CSV file below. The file should contain the following columns: Keyword, Keyword Cluster, Monthly Search Volume per Keyword, Current Clicks per Month for this Website, Current Ranking Position, Current CTR per Keyword for the Website.')

    # Upload the CSV file
    uploaded_file = st.file_uploader("Choose a CSV file", type='csv')
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)

        # Check that the CSV file has the required columns
        required_columns = ["Keyword", "Keyword Cluster", "Monthly Search Volume per Keyword", "Current Clicks per Month for this Website", "Current Ranking Position", "Current CTR per Keyword for the Website"]
        if not all(column in data.columns for column in required_columns):
            st.error("CSV file must contain the following columns: " + ', '.join(required_columns))
        else:
            # Define the improvement scenarios and get the user's choice
            scenarios = ["Improve rankings by X positions", "Improve all rankings by 10%", "Lift all to random page 2 position", "Lift all to random page 1 position", "Lift all to position 1"]
            scenario = st.selectbox('Select an improvement scenario', scenarios)

            # Define the average CTR by position
            avg_ctr_by_position = {1: 0.35, 2: 0.25, 3: 0.20, 4: 0.15, 5: 0.10, 6: 0.08, 7: 0.06, 8: 0.04, 9: 0.03, 10: 0.02}

            # Define the monthly improvement rates
            monthly_rates = [0.05, 0.07, 0.09, 0.10, 0.12, 0.14, 0.16, 0.20, 0.24, 0.28, 0.30, 0.35, 0.40, 0.44, 0.48, 0.52, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 1.00]

            # Initialize the monthly_projections DataFrame
            monthly_projections = pd.DataFrame(columns=['Month', 'Total Potential Traffic'])

            # Calculate the potential traffic for each scenario
            for month, rate in zip(range(1, 25), monthly_rates):
                if scenario == scenarios[0]: # Improve rankings by X positions
                    data['Adjusted Ranking Position'] = np.where(data['Current Ranking Position'] > 1, data['Current Ranking Position'] - rate, data['Current Ranking Position'])
                elif scenario == scenarios[1]: # Improve all rankings by 10%
                    data['Adjusted Ranking Position'] = np.where(data['Current Ranking Position'] > 1, data['Current Ranking Position'] - 0.1 * rate, data['Current Ranking Position'])
                elif scenario == scenarios[2]: # Lift all to random page 2 position
                    data['Adjusted Ranking Position'] = np.where(data['Current Ranking Position'] > 20, random.randint(11, 20), data['Current Ranking Position'])
                elif scenario == scenarios[3]: # Lift all to random page 1 position
                    data['Adjusted Ranking Position'] = np.where(data['Current Ranking Position'] > 10, random.randint(1, 10), data['Current Ranking Position'])
                elif scenario == scenarios[4]: # Lift all to position 1
                    data['Adjusted Ranking Position'] = 1

                data['Potential CTR'] = data['Adjusted Ranking Position'].apply(lambda x: avg_ctr_by_position.get(min(round(x), 10), 0))
                data['Potential Traffic'] = data['Potential CTR'] * data['Monthly Search Volume per Keyword']
                
                monthly_projection = pd.DataFrame({'Month': [month], 'Total Potential Traffic': [data['Potential Traffic'].sum()]})

                monthly_projections = monthly_projections.append(monthly_projection, ignore_index=True)

            # Display the monthly projections
            st.dataframe(monthly_projections)

if __name__ == "__main__":
    main() 
