import streamlit as st
import pandas as pd
import random
import numpy as np
import matplotlib.pyplot as plt

def load_data(file):
    data = pd.read_csv(file)
    required_columns = ['Keyword', 'Cluster', 'Search Intent', 'Monthly Search Volume', 'Current Clicks per Month', 'Current Ranking Position', 'Current CTR']
    if all(col in data.columns for col in required_columns):
        return data[required_columns]
    else:
        return None

def calculate_potential_data(data, ranking_scenario, avg_conversion_value):
    scenarios = ["improve rankings by 1 position", "improve all rankings by 10%", "improve all rankings to position 1"]
    if ranking_scenario == scenarios[0]:
        data['Adjusted Ranking Position'] = data['Current Ranking Position'].apply(lambda x: x-1 if x > 1 else x)
    elif ranking_scenario == scenarios[1]:
        data['Adjusted Ranking Position'] = data['Current Ranking Position'].apply(lambda x: x*0.9 if x > 1 else x)
    elif ranking_scenario == scenarios[2]:
        data['Adjusted Ranking Position'] = data['Current Ranking Position'].apply(lambda x: 1)

    data['Potential CTR'] = data['Adjusted Ranking Position'].apply(lambda x: 0.3 if x == 1 else 0.1)
    data['Potential Traffic'] = data['Potential CTR'] * data['Monthly Search Volume']

    return data

st.title('SEO Potential Analyzer')
st.write('Upload a CSV file for analysis.')

file = st.file_uploader("Upload CSV", type='csv')

if file is not None:
    data = load_data(file)
    if data is not None:
        st.write(data)
        
        ranking_scenario = st.selectbox('Select Ranking Scenario', ["improve rankings by 1 position", "improve all rankings by 10%", "improve all rankings to position 1"])
        avg_conversion_value = st.number_input('Average value of a conversion in €', value=1.0)

        if st.button('Run Analysis'):
            potential_data = calculate_potential_data(data, ranking_scenario, avg_conversion_value)
            st.write(potential_data)

            fig, ax = plt.subplots()
            ax.plot(potential_data['Adjusted Ranking Position'], potential_data['Potential Traffic'])
            ax.set_xlabel('Adjusted Ranking Position')
            ax.set_ylabel('Potential Traffic')
            st.pyplot(fig)

    else:
        st.error('File does not contain the required columns.')
