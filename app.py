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
 
def get_user_by_id(token, user_id):
    headers = {'accept': 'application/json',
               'Authorization': f'Bearer {token}',
               'Content-Type': 'application/json'}
    
    url = f"http://127.0.0.1:8000/user/{user_id}"
    response = requests.get(url, headers=headers)
    return response.json()
 


def get_all_user(token):
    headers = {'accept': 'application/json',
               'Authorization': f'Bearer {token}',
               'Content-Type': 'application/json'}
    response = requests.get("http://127.0.0.1:8000/user/", headers=headers)
    
    if response.status_code == 200:

        users = response.json()
        st.write(users)
        # return response.json()
    else:
        st.error("Failed to fetch users") 



# def user_details_page(session_state):
#     user_id = st.number_input("http://localhost:8000/User ID/", min_value=1, step=1)
#     if st.button("Get User"):
#         if user_id:
#             st.write()
#             user_data = get_user_by_id(user_id)
#             st.write("User Details:")
#             st.json(user_data)
 


def create_exercise(exercise_data, token):
    headers = {'accept': 'application/json',
               'Authorization': f'Bearer {token}',
               'Content-Type': 'application/json'}
    response = requests.post("http://127.0.0.1:8000/exercise/", headers=headers, json=exercise_data)
    if response.status_code == 201:
        st.success("Exercise created successfully")
    else:
        st.error("Failed to create exercise")
    # return response.json()
 


def get_all_exercises(token):
    headers = {'accept': 'application/json',
               'Authorization': f'Bearer {token}',
               'Content-Type': 'application/json'}
    response = requests.get("http://127.0.0.1:8000/exercise/", headers=headers)
    
    if response.status_code == 200:

        exercises = response.json()
        st.write(exercises)
        # return response.json()
    else:
        st.error("Failed to fetch exercises")

# Function to get an exercise by ID
def get_exercise_by_id(token, exercise_id):
    headers = {'accept': 'application/json',
               'Authorization': f'Bearer {token}',
               'Content-Type': 'application/json'}
    
    url = f"http://127.0.0.1:8000/exercise/{exercise_id}"
    response = requests.get(url, headers=headers)
    return response.json()
 


# def get_exercise_by_id(exercise_id):
#     response = make_request(f'http://localhost:8000/exercise/{exercise_id}', method='get')
#     if response.status_code == 200:
#         exercise = response.json()
#         st.write(exercise)
#     else:
#         st.error("Failed to fetch exercise")
 
# Function to update an exercise by ID
def update_exercise_by_id(exercise_id_to_update, name_update, description_update):
    response = make_request(f'http://localhost:8000/exercise/{exercise_id_to_update}', method='put', data={"name": name_update, "description": description_update})
    if response.status_code == 202:
        st.success("Exercise updated successfully")
    else:
        st.error("Failed to update exercise")
 
# Function to delete an exercise by ID
def delete_exercise_by_id(exercise_id_to_delete):
    response = make_request(f'http://localhost:8000/exercise/{exercise_id_to_delete}', method='delete')
    if response.status_code == 204:
        st.success("Exercise deleted successfully")
    else:
        st.error("Failed to delete exercise")
 
 
# Function to create a workout
def create_workout(exercise_id, user_id):
    response = make_request('http://localhost:8000/workout/', method='post', data={"exercise_id": exercise_id, "user_id": user_id})
    if response.status_code == 201:
        st.success("Workout created successfully")
    else:
        st.error("Failed to create workout")
 
# Function to get all workouts
def get_all_workouts():
    response = make_request('http://localhost:8000/workout/', method='get')
    if response.status_code == 200:
        workouts = response.json()
        st.write(workouts)
    else:
        st.error("Failed to fetch workouts")
 
# Function to get a workout by ID
def get_workout_by_id(workout_id):
    response = make_request(f'http://localhost:8000/workout/{workout_id}', method='get')
    if response.status_code == 200:
        workout = response.json()
        st.write(workout)
    else:
        st.error("Failed to fetch workout")
 
# Function to update a workout by ID
def update_workout_by_id(workout_id_to_update, exercise_id_update, user_id_update):
    response = make_request(f'http://localhost:8000/workout/{workout_id_to_update}', method='put', data={"exercise_id": exercise_id_update, "user_id": user_id_update})
    if response.status_code == 202:
        st.success("Workout updated successfully")
    else:
        st.error("Failed to update workout")
 
# Function to delete a workout by ID
def delete_workout_by_id(workout_id_to_delete):
    response = make_request(f'http://localhost:8000/workout/{workout_id_to_delete}', method='delete')
    if response.status_code == 204:
        st.success("Workout deleted successfully")
    else:
        st.error("Failed to delete workout")
 
 

def set_session_data(key, value):
    session_state = st.session_state.get('session_state', {})
    session_state[key] = value
    st.session_state['session_state'] = session_state

# Function to get session data
def get_session_data(key):
    session_state = st.session_state.get('session_state', {})
    return session_state.get(key)

# Function to remove session data
def remove_session_data(key):
    session_state = st.session_state.get('session_state', {})
    if key in session_state:
        del session_state[key]
        st.session_state['session_state'] = session_state


# Main function to interact with FastAPI server routes
def main():
    # Adding CSS for styling
    st.markdown("""
        <style>
        body {
            font-family: Arial, sans-serif;
        }
        .stTextInput>div>div>input {
            background-color: #f4f4f4 !important;
            color: #333333 !important;
        }
        .stButton>button {
            background-color: #007bff !important;
            color: white !important;
        }
        .stSelectbox>div>div>div {
            background-color: #f4f4f4 !important;
            color: #333333 !important;
        }
        .stDateInput>div>div>div>input {
            background-color: #f4f4f4 !important;
            color: #333333 !important;
        }
        .sidebar-content {
            background-color: #f4f4f4 !important;
        }
        .sidebar .sidebar-content .block-container {
            padding: 1rem;
        }
        .sidebar .sidebar-content .block-container .stButton button {
            background-color: #007bff !important;
            color: white !important;
        }
        .sidebar .sidebar-content .block-container .stButton button:hover {
            background-color: #0056b3 !important;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("Fitness Analytics Dashboard")
    st.subheader("Login")
    email = st.text_input("Email", key="email_input")
    password = st.text_input("Password", type="password", key="password_input")
    if st.button("Login", key="login_button"):
        token = login(email, password)
        login_token = token
        if token:
            set_session_data('authKey',token)
            st.success("Login successful")
            st.write("Token:", login_token)
            st.write("")
            st.write("")
            



    st.subheader("Create User")
    
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
            st.write("")
            st.write("")
            # st.json(created_user)
        else:
            st.warning("Please fill in all the fields.")



    # Fetch a user by ID
    st.subheader("Get User by ID")
    user_id = st.number_input("User ID", key="user_id_input")
    if st.button("Get User", key="get_user_button"):
        token = get_session_data('authKey')
        if token:
            user_data = get_user_by_id(token, user_id)
            if user_data:
                st.write("User:", user_data)
        else:
            st.error("Please login first.")

    # Get All Users
    st.subheader("Get All Users")
    if st.button("Get All Users"):
        token = get_session_data('authKey')
        if token:
            get_all_user(token)
            st.write("")
            st.write("")
        else:
            st.error("Please login first.")
    
    

    # Get Users by ID
    st.write("")
    st.write("")
    

    st.subheader("Get Users by ID")
    user_id = st.number_input("Users ID", min_value=1, step=1)
    if st.button("Get Users"):
        token = get_session_data('authKey')
        if token:
            # get_all_user(token)
            get_user_by_id(token, user_id)
        else:
            st.error("Please login first.")


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
    
    if st.sidebar.button("Show Workout Summary"):
        params = {"start_date": start_date, "end_date": end_date, "user_id": user_id}
        data = make_request1("/analytics/workout-summary/", params)
        if data:
            df = pd.DataFrame(data)
            st.dataframe(df)
    
    st.subheader("Create Exercise")
    exercise_name = st.text_input("Exercise Name")
    added_by = st.selectbox("added_by", ["admin"])
    per_count_second_unit_calorie = st.number_input("per_count_second_unit_calorie")
    exercise_type = st.selectbox("Exercise Type", ["outdoors", "indoors"])
    measurement_type = st.selectbox("measurement_type", ["count", "time"])
    major_minor_type = st.selectbox("mazor/minor Type", ["mazor", "minor", "common"])
    
    exercise_data = {
        "exercise_name": exercise_name,
        "added_by": added_by,
        "per_count_second_unit_calorie": per_count_second_unit_calorie,
        "exercise_type": exercise_type,
        "measurement_type": measurement_type,
        "major_minor_type": major_minor_type,
    }
    
    if st.button("Create Exercise"):
        if exercise_name and exercise_type and per_count_second_unit_calorie and measurement_type and major_minor_type:
            token = get_session_data('authKey')
            if token:
                created_exercise = create_exercise(exercise_data, token)
                # st.write(created_exercise)
                st.write("Exercise Created Successfully:")
            else:
                st.error("Please login first.")
        else:
            st.warning("Please fill in all the fields.")


    # Get All Exercises
    st.subheader("Get All Exercises")
    if st.button("Get All Exercises"):
        token = get_session_data('authKey')
        if token:
            get_all_exercises(token)
        else:
            st.error("Please login first.")
    
    

    # Get Exercise by ID
    st.subheader("Get Exercise by ID")
    exercise_id = st.number_input("Exercise ID", min_value=1, step=1)
    if st.button("Get Exercise"):
        token = get_session_data('authKey')
        if token:
            exercise_data = get_exercise_by_id(token, exercise_id)
            if exercise_data:
                st.write("User:", exercise_data)
            else:
                st.error("No Exersise found")
        else:
            st.error("Please login first.")

    # Update Exercise by ID
    st.subheader("Update Exercise by ID")
    exercise_id_to_update = st.number_input("Exercise ID to update", min_value=1, step=1)
    name_update = st.text_input("Update exercise Name")
    description_update = st.text_input("Exercise Description")
    if st.button("Update Exercise"):
        update_exercise_by_id(exercise_id_to_update, name_update, description_update)

    # Delete Exercise by ID
    st.subheader("Delete Exercise by ID")
    exercise_id_to_delete = st.number_input("Exercise ID to delete", min_value=1, step=1)
    if st.button("Delete Exercise"):
        delete_exercise_by_id(exercise_id_to_delete)

    # Create Workout
    st.subheader("Create Workout")
    exercise_id = st.number_input("enter Exercise ID", min_value=1, step=1)
    user_id = st.number_input("User ID", min_value=1, step=1)
    if st.button("Create Workout"):
        create_workout(exercise_id, user_id)

    # Get All Workouts
    st.subheader("Get All Workouts")
    if st.button("Get All Workouts"):
        get_all_workouts()

    # Get Workout by ID
    st.subheader("Get Workout by ID")
    workout_id = st.number_input("Workout ID", min_value=1, step=1)
    if st.button("Get Workout"):
        get_workout_by_id(workout_id)

    # Update Workout by ID
    st.subheader("Update Workout by ID")
    workout_id_to_update = st.number_input("Workout ID to update", min_value=1, step=1)
    exercise_id_update = st.number_input("Update Exercise ID", min_value=1, step=1)
    user_id_update = st.number_input("Update User ID", min_value=1, step=1)
    if st.button("Update Workout"):
        update_workout_by_id(workout_id_to_update, exercise_id_update, user_id_update)

    # Delete Workout by ID
    st.subheader("Delete Workout by ID")
    workout_id_to_delete = st.number_input("Workout ID to delete", min_value=1, step=1)
    if st.button("Delete Workout"):
        delete_workout_by_id(workout_id_to_delete)
 
 
       
 
# Define a simple SessionState class
class SessionState:
    def __init__(self):
        self.token = None
 
if __name__ == "__main__":
    main()
 