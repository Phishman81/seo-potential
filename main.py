import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def calculate_impressions(position, search_volume):
    if position <= 10:
        return int(search_volume * np.random.uniform(0.6, 0.9))
    elif position <= 20:
        return int(search_volume * np.random.uniform(0.2, 0.6))
    elif position <= 30:
        return int(search_volume * np.random.uniform(0.1, 0.2))
    elif position <= 40:
        return int(search_volume * np.random.uniform(0.05, 0.1))
    else:
        return int(search_volume * np.random.uniform(0.01, 0.05))

def calculate_ctr(position):
    if position < 1:
        position = 1
    elif position > 100:
        position = 100

    ctr_by_position = {
        1: 0.35, 
        2: 0.18,
        3: 0.12,
        4: 0.08,
        5: 0.06,
        6: 0.05,
        7: 0.04,
        8: 0.03,
        9: 0.02,
        10: 0.02,
    }

    if position in ctr_by_position:
        return ctr_by_position[position]

    elif 11 <= position <= 20:
        return np.random.uniform(0.01, 0.02)
    elif 21 <= position <= 30:
        return np.random.uniform(0.005, 0.01)
    elif 31 <= position <= 40:
        return np.random.uniform(0.004, 0.008)
    elif 41 <= position <= 50:
        return np.random.uniform(0.003, 0.007)
    elif 51 <= position <= 60:
        return np.random.uniform(0.002, 0.006)
    elif 61 <= position <= 70:
        return np.random.uniform(0.002, 0.005)
    elif 71 <= position <= 80:
        return np.random.uniform(0.001, 0.004)
    elif 81 <= position <= 90:
        return np.random.uniform(0.001, 0.003)
    elif 91 <= position <= 100:
        return np.random.uniform(0.001, 0.002)
    else:
        return 0.0

def calculate_clicks(impressions, ctr):
    return int(impressions * ctr)

def forecast_seo_metrics(search_volume, current_position, expected_position):
    # calculate metrics for current position
    current_impressions = calculate_impressions(current_position, search_volume)
    current_ctr = calculate_ctr(current_position)
    current_clicks = calculate_clicks(current_impressions, current_ctr)

    # calculate metrics for expected position
    expected_impressions = calculate_impressions(expected_position, search_volume)
    expected_ctr = calculate_ctr(expected_position)
    expected_clicks = calculate_clicks(expected_impressions, expected_ctr)

    return {
        'current_position': current_position,
        'current_impressions': current_impressions,
        'current_ctr': current_ctr,
        'current_clicks': current_clicks,
        'expected_position': expected_position,
        'expected_impressions': expected_impressions,
        'expected_ctr': expected_ctr,
        'expected_clicks': expected_clicks,
    }

def main():
    st.title('SEO Metrics Forecast')
    uploaded_file = st.file_uploader('Choose a CSV file', type='csv')
    
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        st.write(data)

        # Select columns
        search_volume_column = st.selectbox("Select search volume column", data.columns)
        current_position_column = st.selectbox("Select current position column", data.columns)
        expected_position_column = st.selectbox("Select expected position column", data.columns)
        
        if st.button("Forecast Metrics"):
            forecasts = []
            for index, row in data.iterrows():
                forecast = forecast_seo_metrics(row[search_volume_column], row[current_position_column], row[expected_position_column])
                forecasts.append(forecast)

            forecasts_df = pd.DataFrame(forecasts)
            st.write(forecasts_df)

if __name__ == "__main__":
    main()
