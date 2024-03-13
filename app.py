import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

# Define the base URL for the FastAPI server
BASE_URL = "http://localhost:8004"  
# http://127.0.0.1:8004/docs#/Analytics/progress_chart_analytics_progress_chart__get
# 127.0.0.1:61392 - "GET /docs/Analytics/analytics/progress-chart/?start_date=2024-03-12&end_date=2024-03-15&user_id=1 HTTP/1.1"

# Function to make requests to FastAPI server
def make_request(endpoint, params):
    response = requests.get(BASE_URL + endpoint, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error: {response.status_code}")
        return None

# Streamlit UI
def main():
    st.title("Fitness Analytics Dashboard")

    # Sidebar filters
    st.sidebar.subheader("Filters")
    start_date = st.sidebar.date_input("Start Date")
    end_date = st.sidebar.date_input("End Date")
    user_id = st.sidebar.number_input("User ID", min_value=1)

    # Buttons to trigger actions
    if st.sidebar.button("Show Progress Chart"):
        params = {"start_date": start_date, "end_date": end_date, "user_id": user_id}
        data = make_request("/analytics/progress-chart/", params)
        if data:
            df = pd.DataFrame(data, columns=['created_at', 'total_calories_burnt'])
            st.line_chart(df.set_index('created_at'))

    if st.sidebar.button("Show Workout Summary"):
        params = {"start_date": start_date, "end_date": end_date, "user_id": user_id}
        data = make_request("/analytics/workout-summary/", params)
        if data:
            df = pd.DataFrame(data)
            st.dataframe(df)

if __name__ == "__main__":
    main()
