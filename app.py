import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("🚕 NYC Taxi Trips - January 2021")

@st.cache_data
def load_data(nrows):
    df = pd.read_csv("yellow_tripdata_2021-01.csv", nrows=nrows)
    df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
    df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])
    df['trip_duration_min'] = (df['tpep_dropoff_datetime'] - df['tpep_pickup_datetime']).dt.total_seconds() / 60
    df = df[(df['trip_duration_min'] > 0) & (df['trip_duration_min'] < 180)]
    df['pickup_hour'] = df['tpep_pickup_datetime'].dt.hour
    return df

nrows = st.sidebar.slider("Number of rows to load", 10000, 100000, 30000)
df = load_data(nrows)

st.write(f"Loaded {len(df)} rows.")

if st.checkbox("Show raw data"):
    st.dataframe(df.head())

st.subheader("Distribution of Trip Duration (minutes)")
fig1, ax1 = plt.subplots(figsize=(10, 4))
sns.histplot(df['trip_duration_min'], bins=100, kde=True, ax=ax1)
ax1.set_xlim(0, 60)
st.pyplot(fig1)

st.subheader("Number of Trips by Pickup Hour")
fig2, ax2 = plt.subplots(figsize=(10, 4))
sns.countplot(x='pickup_hour', data=df, palette='viridis', ax=ax2)
st.pyplot(fig2)

st.subheader("Average Trip Distance by Hour of Day")
avg_distance = df.groupby('pickup_hour')['trip_distance'].mean().reset_index()
fig3, ax3 = plt.subplots(figsize=(10, 4))
sns.lineplot(x='pickup_hour', y='trip_distance', data=avg_distance, marker='o', ax=ax3)
st.pyplot(fig3)

# Download filtered data button
csv = df.to_csv(index=False)
st.download_button("Download loaded data as CSV", data=csv, file_name='nyc_taxi_sample.csv')
