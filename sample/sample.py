import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px

# Generate some example data (replace this with your actual data loading logic)
def generate_example_data():
    today = datetime.now()
    dates = [today - timedelta(days=i) for i in range(1, 100)]
    actual_values = [i + 10 * (i % 5) for i in range(1, 100)]
    forecasted_values = [i + 10 * (i % 5) + 5 for i in range(1, 100)]
    df = pd.DataFrame({'Date': dates, 'Actual': actual_values, 'Forecasted': forecasted_values})
    return df

# Function to plot the graph based on user input
def plot_time_series(selected_option, num_records):
    df = generate_example_data()

    if selected_option == 'monthly':
        df = df.resample('M', on='Date').mean()
    elif selected_option == 'halferly':
        df = df.resample('2M', on='Date').mean()
    elif selected_option == 'yearly':
        df = df.resample('Y', on='Date').mean()

    # Select the specified number of records
    df = df.tail(num_records)

    # Reset index to make 'Date' a regular column
    df = df.reset_index()

    # Plotting with Plotly
    fig = px.line(df, x='Date', y=['Actual', 'Forecasted'], labels={'value': 'Values'}, title='Actual vs Forecasted Values')
    st.plotly_chart(fig)

# Streamlit app
st.title('Time Series Visualization')

# Select box for time period
selected_option = st.selectbox('Select Time Period', ['monthly', 'halferly', 'yearly'])

# Number input for the number of records
num_records = st.number_input('Enter Number of Records', min_value=1, value=40)

# Plot the time series graph
plot_time_series(selected_option, num_records)
