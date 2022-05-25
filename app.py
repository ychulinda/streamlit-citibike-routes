import pandas as pd
import folium
import streamlit as st
from streamlit_folium import folium_static
import base64

st.set_page_config(
     page_title="Top Routes App",
     page_icon="\N{globe with meridians}",
     layout="wide",
     initial_sidebar_state="expanded")

st.get_option('theme.backgroundColor')

st.write('''
# Map of the most popular bike rental routes in New York
Data obtained from the Google BigQuery public datasets 
''')


trip_year = st.sidebar.selectbox('Trip year', (2013, 2014, 2015, 2016, 2017, 2018))
top_routes = st.sidebar.slider('Number of top trips', 1, 100, 15)


@st.cache
def load_trip_data():
    df = pd.read_csv('trips.csv')
    return df


def file_download(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="trip_data.csv">Download CSV File</a>'
    return href


df = load_trip_data()

df = df[df['trip_year'] == trip_year]


m = folium.Map([40.73, -73.95] ,zoom_start=12.4)

for _, row in df.iloc[:top_routes].iterrows():
    folium.CircleMarker([row['start_station_latitude'], row['start_station_longitude']],
                        radius=10,
                        fill_color="#3db7e4", 
                       ).add_to(m)

    folium.CircleMarker([row['end_station_latitude'], row['end_station_longitude']],
                        radius=10,
                        fill_color="red", 
                       ).add_to(m)

    folium.PolyLine([[row['start_station_latitude'], row['start_station_longitude']], 
                     [row['end_station_latitude'], row['end_station_longitude']]]).add_to(m)

st.write("Total trips: ", df.iloc[:top_routes]['Trips_on_route'].sum())

folium_static(m)

st.dataframe(df)


st.sidebar.markdown(file_download(df), unsafe_allow_html=True)