import base64
import streamlit as st
import pandas as pd

# CTR-Bereiche
ctr_ranges_adjusted = {
    (0, 1.5): (0.30, 0.35),
    (1.5, 2.5): (0.15, 0.18),
    (2.5, 3.5): (0.10, 0.12),
    (3.5, 4.5): (0.07, 0.09),
    (4.5, 5.5): (0.05, 0.07),
    (5.5, 6.5): (0.04, 0.06),
    (6.5, 7.5): (0.03, 0.05),
    (7.5, 8.5): (0.03, 0.04),
    (8.5, 10.5): (0.02, 0.03),
    (10.5, 20.5): (0.01, 0.02),
    (20.5, 30.5): (0.005, 0.01),
    (30.5, 40.5): (0.004, 0.008),
    (40.5, 50.5): (0.003, 0.007),
    (50.5, 60.5): (0.002, 0.006),
    (60.5, 70.5): (0.002, 0.005),
    (70.5, 80.5): (0.001, 0.004),
    (80.5, 90.5): (0.001, 0.003),
    (90.5, 100.5): (0.001, 0.002)
}

# Monatliche Verbesserungen
monthly_improvements = [0.01, 0.04, 0.06, 0.09, 0.15, 0.27, 0.45, 0.57, 0.67, 0.70, 0.81, 1.00]

# Funktion, um den durchschnittlichen CTR basierend auf der Position zu erhalten
def get_avg_ctr_corrected(position):
    for key, value in ctr_ranges_adjusted.items():
        if key[0] <= position <= key[1]:
            return (value[0] + value[1]) / 2
    return 0

# Hauptfunktion der Streamlit-App
def main():
    st.title("Berechnung der monatlichen geschätzten Klicks")

    uploaded_file = st.file_uploader("Laden Sie Ihre CSV-Datei hoch", type=["csv"])
    
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        
        for month in range(1, 13):
            data[f"Improvement Month {month} (in percent)"] = monthly_improvements[month - 1] * 100
            data[f"Estimated Position Month {month}"] = data["Position"] - (data["Position"] - 1) * monthly_improvements[month - 1]
            data[f"Estimated Clicks Month {month}"] = data['Avg. monthly searches'] * data[f"Estimated Position Month {month}"].apply(get_avg_ctr_corrected)
        
        st.write(data)

        csv = data.to_csv(index=False)
        b64 = b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="estimated_clicks_monthly_details.csv">Download CSV File</a>'
        st.markdown(href, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

import matplotlib.pyplot as plt

# Erstellung des Liniendiagramms
def create_visualization(df):
    months = ["Current"] + [f"Month {i}" for i in range(1, 13)]
    total_clicks = [df["Clicks"].sum()]
    for month in range(1, 13):
        total_clicks.append(df[f"Estimated Clicks Month {month}"].sum())
    
    plt.figure(figsize=(12, 6))
    plt.plot(months, total_clicks, marker='o', color='b')
    
    for i, (month, value) in enumerate(zip(months[1:], total_clicks[1:])):
        plt.text(month, value, f"{monthly_improvements[i]*100:.0f}%", ha='center', va='bottom')

    plt.title('Gesamtklicks pro Monat (Aktuell und Prognostiziert)')
    plt.xlabel('Monat')
    plt.ylabel('Gesamtklicks')
    plt.grid(True)
    plt.ylim(df["Clicks"].sum(), max(total_clicks) + 0.05 * max(total_clicks))
    plt.tight_layout()
    
    st.pyplot(plt)

result_df = None
# Anzeigen der Visualisierung
if result_df is not None:
    create_visualization(result_df)
