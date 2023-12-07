import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
@st.cache
def load_data():
    data = pd.read_csv('day.csv')
    data['dateday'] = pd.to_datetime(data['dateday'])  # Convert 'dateday' to datetime format
    return data

df = load_data()

# Sidebar for user input features
season = st.sidebar.selectbox('Select Season', df['season'].unique())
weather = st.sidebar.selectbox('Select Weather Condition', df['Weather_cond'].unique())

# Filter data based on user input
filtered_data = df[(df['season'] == season) & (df['Weather_cond'] == weather)]

# Display data
st.write("Filtered Data", filtered_data)

# Sidebar untuk fitur input pengguna
st.sidebar.header('Filter by Date Range')
start_date = st.sidebar.date_input('Start Date', df['dateday'].min().date())
end_date = st.sidebar.date_input('End Date', df['dateday'].max().date())

# Konversi start_date dan end_date ke datetime jika belum
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# Pastikan start date tidak setelah end date
if start_date > end_date:
    st.sidebar.error('Error: End date must fall after start date.')

# Filter data berdasarkan input pengguna
filtered_data = df[(df['dateday'] >= start_date) & (df['dateday'] <= end_date)]

# Visualization
st.subheader('Temperature vs Total Count')
fig, ax = plt.subplots()
sns.scatterplot(data=filtered_data, x='temp', y='count', ax=ax)
st.pyplot(fig)

st.subheader('Histogram of Casual vs Registered Users')
fig, ax = plt.subplots()
sns.histplot(filtered_data, x='casual', color='blue', label='Casual', kde=True, ax=ax)
sns.histplot(filtered_data, x='registered', color='red', label='Registered', kde=True, ax=ax)
plt.legend()
st.pyplot(fig)

# Additional Visualizations for Streamlit App

# Bar Chart: Total Bike Rentals by Season
st.subheader('Total Bike Rentals by Season')
fig, ax = plt.subplots()
seasonal_data = df.groupby('season')['count'].sum().reset_index()
sns.barplot(data=seasonal_data, x='season', y='count', ax=ax)
st.pyplot(fig)

# Line Plot: Trend of Bike Rentals Over the Year
st.subheader('Trend of Bike Rentals Over the Year')
fig, ax = plt.subplots()
monthly_data = df.groupby('month')['count'].sum().reset_index()
sns.lineplot(data=monthly_data, x='month', y='count', ax=ax)
st.pyplot(fig)

# Heatmap: Correlation between Features
st.subheader('Correlation Heatmap')
fig, ax = plt.subplots()
correlation_matrix = df[['temp', 'atemp', 'hum', 'windspeed', 'casual', 'registered', 'count']].corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', ax=ax)
st.pyplot(fig)