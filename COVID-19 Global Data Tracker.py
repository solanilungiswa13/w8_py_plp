# 📌 COVID-19 Global Data Tracker
# Step 2 & Step 3: Data Acquisition and Cleaning

# 📦 Import required libraries
import pandas as pd
import numpy as np

# 🌐 Step 2: Load the Data
# Source: Our World in Data (OWID) - CSV URL
data_url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"

# Read CSV directly from the URL
df = pd.read_csv(data_url)

# Quick preview
print("Dataset Shape:", df.shape)
df.head()

# Step 3: Data Cleaning
# Check for missing values
df.isnull().sum().sort_values(ascending=False).head(10)

# Convert 'date' column to datetime
df['date'] = pd.to_datetime(df['date'])

# Select important columns for analysis
cols_of_interest = [
    'iso_code', 'continent', 'location', 'date',
    'total_cases', 'new_cases', 'total_deaths', 'new_deaths',
    'total_vaccinations', 'people_vaccinated', 'people_fully_vaccinated',
    'population'
]

df = df[cols_of_interest]

# Drop rows where location is missing (optional for cleaning)
df = df[df['location'].notnull()]

# Filter out aggregate rows like "World", "Africa", "Europe" etc.
continents = ['Africa', 'Asia', 'Europe', 'European Union', 'North America', 'Oceania', 'South America', 'World']
df = df[~df['location'].isin(continents)]

# Fill NaNs with 0 for numerical analysis (or keep them, depending on your approach)
df.fillna(0, inplace=True)

# Check cleaned data
df.info()
df.describe()

#Step 4
# Group data by date for global totals
global_daily = df.groupby('date')[['new_cases', 'new_deaths', 'total_vaccinations']].sum()

# Plot global trends
import matplotlib.pyplot as plt

plt.figure(figsize=(14, 6))
plt.plot(global_daily.index, global_daily['new_cases'], label='New Cases', color='blue')
plt.plot(global_daily.index, global_daily['new_deaths'], label='New Deaths', color='red')
plt.title('Global COVID-19 Daily New Cases and Deaths')
plt.xlabel('Date')
plt.ylabel('Count')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Get the latest data for each country
latest_date = df['date'].max()
latest_df = df[df['date'] == latest_date]

top_countries = latest_df.sort_values(by='total_cases', ascending=False).head(10)

# Plot
plt.figure(figsize=(10, 6))
plt.barh(top_countries['location'], top_countries['total_cases'], color='orange')
plt.xlabel('Total Cases')
plt.title('Top 10 Countries by Total COVID-19 Cases (as of {})'.format(latest_date.date()))
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()

# Check vaccination progress
# Choose a few countries
countries = ['United States', 'India', 'Brazil', 'Germany', 'South Africa']

# Filter and pivot
vax_df = df[df['location'].isin(countries)]
vax_pivot = vax_df.pivot(index='date', columns='location', values='people_vaccinated')

# Plot
vax_pivot.plot(figsize=(14, 6), title='People Vaccinated Over Time')
plt.ylabel('People Vaccinated')
plt.grid(True)
plt.tight_layout()
plt.show()