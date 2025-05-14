# covid_tracker_app.py

import streamlit as st
import pandas as pd
import plotly.express as px

st.title("COVID-19 Global Data Tracker")

# Load data
@st.cache_data
def load_data():
    url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
    df = pd.read_csv(url)
    df['date'] = pd.to_datetime(df['date'])
    df = df[['location', 'date', 'total_cases', 'new_cases', 'total_deaths', 'new_deaths', 'total_vaccinations', 'people_vaccinated']]
    return df.dropna(subset=["location"])

df = load_data()

# Filter by country
country = st.selectbox("Select a country", sorted(df['location'].unique()))
country_df = df[df['location'] == country]

# Line chart
fig = px.line(
    country_df, x='date', y=['total_cases', 'total_deaths', 'total_vaccinations'],
    labels={'value': 'Count', 'date': 'Date'}, 
    title=f"COVID-19 Trends in {country}"
)
st.plotly_chart(fig, use_container_width=True)

# Show data table
if st.checkbox("Show raw data"):
    st.write(country_df.tail())