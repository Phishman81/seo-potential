import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import random

# Die Liste der Verbesserungsszenarien
scenarios = [
    "Verbessere alle Rankings um 1 Position",
    "Verbessere alle Rankings um 2 Positionen",
    "Verbessere alle Rankings um 5 Positionen",
    "Verbessere alle Rankings um 10 Positionen",
    "Verbessere alle Rankings um 20%",
    "Verbessere alle Rankings um 50%",
    "Verbessere alle Rankings um 100%",
    "Hebe alle Rankings unter Seite 2 auf eine zufällige Position auf Seite 2 an",
    "Hebe alle Rankings unter Seite 1 auf eine zufällige Position auf Seite 1 an",
    "Hebe alle Rankings auf Position 1 an"
]

# Die Liste der CTR-Quellen
ctr_sources = ["Quelle 1", "Quelle 2", "Quelle 3"]

# Funktion um die CTR nach Position basierend auf der Quelle zu bekommen
def get_ctr_by_position(ctr_source):
    if ctr_source == "Quelle 1":
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
    elif ctr_source == "Quelle 2":
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
    elif ctr_source == "Quelle 3":
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

# Berechne den potenziellen Traffic basierend auf dem Szenario
def calculate_potential_traffic_based_on_scenario(data, scenario, avg_ctr_by_position):
    if "Verbessere alle Rankings um" in scenario:
        if "Position" in scenario:
            improvement = int(scenario.split()[4])  # extrahiere die Anzahl der zu verbessernden Positionen
            data['Adjusted Ranking Position'] = data['Current Ranking Position'].apply(lambda x: max(x - improvement, 1))
        elif "%" in scenario:
            improvement = int(scenario.split()[4].strip('%')) / 100  # extrahiere den Prozentsatz der Verbesserung
            data['Adjusted Ranking Position'] = data['Current Ranking Position'].apply(lambda x: max(x * (1 - improvement), 1))
    elif "Hebe alle Rankings unter" in scenario:
        target_page = int(scenario.split()[4])  # extrahiere die Ziel-Seite
        lower_bound = 10 * (target_page - 1) + 1  # berechne die untere Grenze der Ziel-Seite
        upper_bound = 10 * target_page  # berechne die obere Grenze der Ziel-Seite
        data['Adjusted Ranking Position'] = data['Current Ranking Position'].apply(lambda x: random.randint(lower_bound, upper_bound) if x > upper_bound else x)
    elif scenario == "Hebe alle Rankings auf Position 1 an":
        data['Adjusted Ranking Position'] = 1
    data['Potential CTR'] = data['Adjusted Ranking Position'].apply(lambda x: avg_ctr_by_position[min(round(x), 10)])
    data['Potential Traffic'] = data['Potential CTR'] * data['Monthly Search Volume per Keyword']
    return data

def main():
    st.title('SEO Potential Analyzer')
    st.write('Bitte laden Sie Ihre CSV-Datei hoch. Die Datei sollte die folgenden Spalten enthalten: Keyword, Keyword Cluster, monatliches Suchvolumen pro Keyword, aktuelle Klicks pro Monat für diese Website, aktuelle Ranking-Position, aktuelle CTR pro Keyword für die Website.')

    uploaded_file = st.file_uploader("Wählen Sie eine CSV-Datei aus", type='csv')

    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)

        scenario = st.selectbox(
            'Wählen Sie ein Verbesserungsszenario aus',
            scenarios
        )

        ctr_source = st.selectbox(
            'Wählen Sie eine CTR-Quelle aus',
            ctr_sources
        )

        avg_ctr_by_position = get_ctr_by_position(ctr_source)

        data = calculate_potential_traffic_based_on_scenario(data, scenario, avg_ctr_by_position)

        st.dataframe(data)

        st.subheader('Gesamtaktuelle Traffic')
        current_traffic = data['Current Clicks per Month for this Website'].sum()
        st.write(current_traffic)

        st.subheader('Gesamtpotenzial Traffic')
        potential_traffic = data['Potential Traffic'].sum()
        st.write(potential_traffic)

        fig, ax = plt.subplots()

        bar_width = 0.35

        rects1 = plt.bar(1, current_traffic, bar_width,
        color='b',
        label='Gesamtaktuelle Traffic')

        rects2 = plt.bar(1 + bar_width, potential_traffic, bar_width,
        color='g',
        label='Gesamtpotenzial Traffic')

        plt.xlabel('Traffic-Typ')
        plt.ylabel('Traffic')
        plt.title('Gesamtaktuelle Traffic vs. Gesamtpotenzial Traffic')
        plt.xticks([1, 1 + bar_width], ['Gesamtaktuelle Traffic', 'Gesamtpotenzial Traffic'])
        plt.legend()

        plt.tight_layout()
        st.pyplot(fig)

        # Erstelle ein Balkendiagramm für die Keyword Cluster
        fig, ax = plt.subplots()

        keyword_clusters = data['Keyword Cluster'].unique()
        index = np.arange(len(keyword_clusters))
        
        current_traffic_per_cluster = [data[data['Keyword Cluster'] == cluster]['Current Clicks per Month for this Website'].sum() for cluster in keyword_clusters]
        potential_traffic_per_cluster = [data[data['Keyword Cluster'] == cluster]['Potential Traffic'].sum() for cluster in keyword_clusters]

        rects1 = plt.bar(index, current_traffic_per_cluster, bar_width,
        color='b',
        label='Gesamtaktuelle Traffic')

        rects2 = plt.bar(index + bar_width, potential_traffic_per_cluster, bar_width,
        color='g',
        label='Gesamtpotenzial Traffic')

        plt.xlabel('Keyword Cluster')
        plt.ylabel('Traffic')
        plt.title('Gesamtaktuelle Traffic vs. Gesamtpotenzial Traffic pro Keyword Cluster')
        plt.xticks(index + bar_width, keyword_clusters, rotation=90)
        plt.legend()

        plt.tight_layout()
        st.pyplot(fig)

if __name__ == "__main__":
    main()
