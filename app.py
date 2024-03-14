import streamlit as st
import requests
from datetime import date
import pandas as pd
 
# Base URL for the FastAPI server
BASE_URL = "http://localhost:8000"
 
# Function to make requests to FastAPI server
def make_request(endpoint, method='get', data=None):
    url = f"{BASE_URL}{endpoint}"
    headers = {'Content-Type': 'application/json'}
    if method == 'get':
        response = requests.get(url, headers=headers)
    elif method == 'post':
        response = requests.post(url, json=data, headers=headers)
    elif method == 'put':
        response = requests.put(url, json=data, headers=headers)
    elif method == 'delete':
        response = requests.delete(url, headers=headers)
    else:
        raise ValueError(f"Unsupported HTTP method: {method}")
    return response
 
 
def make_request1(endpoint, params):
    response = requests.get(BASE_URL + endpoint, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error: {response.status_code}")
        return None
   

def make_request2(endpoint, params):
    # 8000/analytics/workout-summary/?start_date=2024-03-12&end_date=2024-03-15
    response = requests.get(BASE_URL + endpoint, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error: {response.status_code}")
        return None
   
 
def login(email, password):
    response = requests.post("http://localhost:8000/login", data={"username": email, "password": password})
    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        st.error("Invalid credentials")
        return None
 
 
# Function to make API request
def create_user(user_data):
    response = requests.post("http://localhost:8000/user/", json=user_data)
    return response.json()
 
 
 
 
# # Function to make API request with JWT token
def get_user_by_id(user_id):
    # headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"http://localhost:8000/user/{user_id}")
    if response.status_code == 200:
        return response.json()
    else:
        return None
 
 
def user_details_page(session_state):
    user_id = st.number_input("User ID", min_value=1, step=1)
    if st.button("Get User"):
        if user_id:
            st.write()
            user_data = get_user_by_id(user_id)
            st.write("User Details:")
            st.json(user_data)
 
 
 
# Main function to interact with FastAPI server routes
def main():
            st.title("Fitness Analytics Dashboard")
 
           
            st.subheader("Login")
            email = st.text_input("Email", key="email_input")
            password = st.text_input("Password", type="password", key="password_input")
            if st.button("Login", key="login_button"):
                token = login(email, password)
                if token:
                    st.success("Login successful")
                    # st.write("Token:", token)
                    st.write("")
 
 
 
            st.subheader("Sign Up User")
           
            name = st.text_input("Name")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            role = st.selectbox("Role", ["admin", "customer"])
            admin_id = st.number_input("Admin ID", min_value=1, step=1)
           
            user_data = {
                "name": name,
                "email": email,
                "password": password,
                "role": role,
                "admin_id": admin_id
            }
           
            if st.button("Create User"):
                if name and email and password and role:
                    created_user = create_user(user_data)
                    st.write("User Created Successfully:")
                    # st.json(created_user)
                else:
                    st.warning("Please fill in all the fields.")
 
 
 
            # Fetch a user by ID
            st.subheader("Get User by ID")
            user_id = st.number_input("User ID", key="user_id_input")
            if st.button("Get User", key="get_user_button"):
                user_data = get_user_by_id(user_id)
                if user_data:
                    st.write("User:", user_data)
                st.write("")
 
 
            st.sidebar.subheader("Filters")
            start_date = st.sidebar.date_input("Start Date")
            end_date = st.sidebar.date_input("End Date")
            user_id = st.sidebar.number_input("User ID", min_value=1)
 

                # Buttons to trigger actions
            if st.sidebar.button("Show Progress Chart"):
                params = {"start_date": start_date, "end_date": end_date, "user_id": user_id}
                data = make_request1("/analytics/progress-chart/", params)
                if data:
                    df = pd.DataFrame(data, columns=['created_at', 'total_calories_burnt'])
                    st.line_chart(df.set_index('created_at'))
           
            st.subheader("workout summary")
            if st.sidebar.button("Show Workout Summary"):
                params = {"start_date": start_date, "end_date": end_date, "user_id": user_id}
                data = make_request1("/analytics/workout-summary/", params)
                if data:
                    df = pd.DataFrame(data)
                    st.dataframe(df)
           
       
 
# Define a simple SessionState class
class SessionState:
    def __init__(self):
        self.token = None
 
if __name__ == "__main__":
    main()
 
 
 