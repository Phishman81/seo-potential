import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def calculate_clicks(df):
    monthly_improvements = [0.01, 0.04, 0.06, 0.09, 0.15, 0.27, 0.45, 0.57, 0.67, 0.70, 0.81, 1.00]
    current_clicks = df['Clicks'].sum()
    all_clicks = [current_clicks]

    for improvement in monthly_improvements:
        current_clicks += current_clicks * improvement
        all_clicks.append(current_clicks)

    return all_clicks

def plot_graph(all_clicks):
    months = list(range(13))
    plt.figure(figsize=(10, 5))
    plt.plot(months, all_clicks, label='Mit Verbesserungen', marker='o')
    plt.axhline(y=all_clicks[0], color='r', linestyle='-', label='Ohne Verbesserung')
    for i, txt in enumerate(monthly_improvements):
        plt.annotate(txt, (months[i+1], all_clicks[i+1]), fontsize=9)
    plt.title('Prognose der Klickentwicklung')
    plt.xlabel('Monate')
    plt.ylabel('Gesamtklicks')
    plt.legend()
    st.pyplot()

monthly_improvements = [0.01, 0.04, 0.06, 0.09, 0.15, 0.27, 0.45, 0.57, 0.67, 0.70, 0.81, 1.00]
result_df = None

st.title('SEO Potential Prognose')

uploaded_file = st.file_uploader("Wählen Sie eine CSV-Datei aus", type="csv")
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.write(data)

    st.write("### Prognose")
    result_df = calculate_clicks(data)
    plot_graph(result_df)

if result_df is not None:
    st.write(result_df)
