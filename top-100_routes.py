import pandas as pd
import folium
import streamlit as st
from streamlit_folium import folium_static



st.write('''
# Map of the most popular bike rental routes in New York
Data obtained from the Google BigQuery public datasets 
''')

st.markdown('<style>body{background-color: #0B2339;}</style>',unsafe_allow_html=True) 

trip_year = st.sidebar.selectbox('Trip year', (2013, 2014, 2015, 2016, 2017, 2018))
top_routes = st.sidebar.slider('Number of top trips', 1, 100, 5)


@st.cache
def load_trip_data():
    df = pd.read_csv('trips.csv')
    return df


df = load_trip_data()

df = df[df['trip_year'] == trip_year]


m = folium.Map([40.73, -73.95] ,zoom_start=12.4)

for _, row in df.iloc[:top_routes].iterrows():
    folium.CircleMarker([row['start_station_latitude'], row['start_station_longitude']],
                        radius=10,
                        fill_color="#3db7e4", # divvy color
                       ).add_to(m)

    folium.CircleMarker([row['end_station_latitude'], row['end_station_longitude']],
                        radius=10,
                        fill_color="red", # divvy color
                       ).add_to(m)

    folium.PolyLine([[row['start_station_latitude'], row['start_station_longitude']], 
                     [row['end_station_latitude'], row['end_station_longitude']]]).add_to(m)

folium_static(m)

st.write("Total trips: ", df.iloc[:top_routes]['Trips_on_route'].sum())
