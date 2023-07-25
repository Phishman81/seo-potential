import streamlit as st
import pandas as pd
import random
import numpy as np
import matplotlib.pyplot as plt

# Functions to calculate metrics
def calculate_impressions(position, search_volume):
    if position <= 10:
        return int(search_volume * random.uniform(0.6, 0.9))
    elif position <= 20:
        return int(search_volume * random.uniform(0.2, 0.6))
    elif position <= 30:
        return int(search_volume * random.uniform(0.1, 0.2))
    elif position <= 40:
        return int(search_volume * random.uniform(0.05, 0.1))
    else:
        return int(search_volume * random.uniform(0.01, 0.05))

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
        return random.uniform(0.01, 0.02)
    elif 21 <= position <= 30:
        return random.uniform(0.005, 0.01)
    elif 31 <= position <= 40:
        return random.uniform(0.004, 0.008)
    elif 41 <= position <= 50:
        return random.uniform(0.003, 0.007)
    elif 51 <= position <= 60:
        return random.uniform(0.002, 0.006)
    elif 61 <= position <= 70:
        return random.uniform(0.002, 0.005)
    elif 71 <= position <= 80:
        return random.uniform(0.001, 0.004)
    elif 81 <= position <= 90:
        return random.uniform(0.001, 0.003)
    elif 91 <= position <= 100:
        return random.uniform(0.001, 0.002)
    else:
        return 0.0

def calculate_clicks(impressions, ctr):
    return int(impressions * ctr)

# Streamlit interface
def main():
    st.title("SEO Metrics Forecast")
    
    search_volume = st.number_input("Enter Search Volume", min_value=0, max_value=int(1e9), value=10000)
    current_position = st.number_input("Enter Current Position", min_value=0.0, max_value=100.0, value=15.0)
    expected_position = st.number_input("Enter Expected Position", min_value=0.0, max_value=100.0, value=5.0)
    
    if st.button("Forecast Metrics"):
        forecast = forecast_seo_metrics(search_volume, current_position, expected_position)
        st.write(forecast)
        
# Running the main function
if __name__ == '__main__':
    main()
