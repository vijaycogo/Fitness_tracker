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
        return response.json()
    else:
        st.error("Failed to fetch users") 


def create_exercise(exercise_data, token):
    headers = {'accept': 'application/json',
               'Authorization': f'Bearer {token}',
               'Content-Type': 'application/json'}
    response = requests.post("http://127.0.0.1:8000/exercise/", headers=headers, json=exercise_data)
    if response.status_code == 201:
        st.success("Exercise created successfully")
        return response.json()
    else:
        st.error("Failed to create exercise")
 


def get_all_exercises(token):
    headers = {'accept': 'application/json',
               'Authorization': f'Bearer {token}',
               'Content-Type': 'application/json'}
    response = requests.get("http://127.0.0.1:8000/exercise/", headers=headers)
    
    if response.status_code == 200:

        exercises = response.json()
        st.write(exercises)
        return response.json()
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
 



def update_exercise_by_id(token, exercise_data, exercise_id):
    headers = {'accept': 'application/json',
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'}
 
    url = f"http://localhost:8000/exercise/{exercise_id}"
    response = requests.put(url, headers=headers, json = exercise_data )
    return response.json()
 
 
# Function to delete an exercise by ID
def delete_exercise_by_id(token, exercise_id):
    headers = {'accept': 'application/json',
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'}
    url = f" http://localhost:8000/exercise/{exercise_id}"
    response = requests.delete(url, headers=headers)
    return response
 

 
 
# Function to create a workout
def create_workout(workout_data,token):
    headers = {'accept': 'application/json',
               'Authorization': f'Bearer {token}',
               'Content-Type': 'application/json'}
    response = requests.post("http://localhost:8000/workout/", headers=headers, json=workout_data)
    if response.status_code == 201:
        st.success("Workout created successfully")
        return response.json()
    else:
        st.error("Failed to create workout")


def get_all_workouts(token):
    headers = {'accept': 'application/json',
               'Authorization': f'Bearer {token}',
               'Content-Type': 'application/json'}
    response = requests.get("http://localhost:8000/workout/", headers=headers)
    if response.status_code == 200:
        workout = response.json()
        st.write(workout)
    else:
        st.error("Failed to fetch workouts")

def get_workout_by_id(token, workout_id):
    headers = {'accept': 'application/json',
               'Authorization': f'Bearer {token}',
               'Content-Type': 'application/json'}
    url = f" http://localhost:8000/workout/{workout_id}"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()   
    else:
        st.error("Failed to fetch workouts")


def update_workout_by_id(token, workout_data, workout_id):
    headers = {'accept': 'application/json',
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'}
 
    url = f"http://localhost:8000/workout/{workout_id}"
    response = requests.put(url, headers=headers, json = workout_data )
    return response.json()
 
 
# Function to delete an exercise by ID
def delete_workout_by_id(token, workout_id):
    headers = {'accept': 'application/json',
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'}
    url = f" http://localhost:8000/workout/{workout_id}"
    response = requests.delete(url, headers=headers)
    return response
 


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
            # st.write("Token:", login_token)
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
    user_id = st.number_input("User ID", min_value=1, step=1)
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
    per_count_second_unit_calorie = st.number_input("per_count_second_unit_calorie",  min_value=1, step=1)
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
                st.write("Exercise:", exercise_data)
            else:
                st.error("No Exersise found")
        else:
            st.error("Please login first.")

    # Update Exercise by ID
    st.subheader("Update Exercise by ID")
    exercise_id = st.number_input("input exercise_id",  min_value=1, step=1)
    exercise_name = st.text_input("Update Exercise Name")
    added_by_admin = st.selectbox("added_by_admin", ["admin"])
    per_count_second_unit_calorie = st.number_input("Update per_count_second_unit_calorie", min_value=1, step=1)
    exercise_type = st.selectbox("Update Exercise Type", ["outdoors", "indoors"])
    measurement_type = st.selectbox("Update measurement_type", ["count", "time"])
    major_minor_type = st.selectbox("Update mazor/minor Type", ["mazor", "minor", "common"])
   
    exercise_data = {
        "exercise_name": exercise_name,
        "added_by": added_by_admin,
        "per_count_second_unit_calorie": per_count_second_unit_calorie,
        "exercise_type": exercise_type,
        "measurement_type": measurement_type,
        "major_minor_type": major_minor_type,
    }
   
    if st.button("Update Exercise"):
        token = get_session_data('authKey')
        if token:
            exercise_data = update_exercise_by_id(token, exercise_data, exercise_id)
            if exercise_data:
                st.write("User:", exercise_data)
            else:
                st.error("No Exersise found")
        else:
            st.error("Please login first.")      
 
 
    # Delete Exercise by ID
    st.subheader("Delete Exercise by ID")
    exercise_id= st.number_input("Exercise ID to delete", min_value=1, step=1)
    if st.button("Delete Exercise"):
        token = get_session_data('authKey')
        if token:
            response =delete_exercise_by_id(token, exercise_id)
            if response.status_code == 204 :
                st.write("Deleted Exercise Id: ", exercise_id )
            else:
                st.error("No Exersise found")
        else:
            st.error("Please login first.")


    # # Get All Workouts
    st.subheader("Get All Workouts")
    if st.button("Get All Workouts"):
        token = get_session_data('authKey')
        if token:
            get_all_workouts(token)
        else:
            st.error("Please login first.")

    # Get Workout by ID
    st.subheader("Get Workout by ID")
    workout_id = st.number_input("Workout ID", min_value=1, step=1)
    if st.button("Get Workout"):
        token = get_session_data('authKey')
        if token:
            workout_data = get_workout_by_id(token, workout_id)
            if workout_data:
                st.write("Workout:", workout_data)
            else:
                st.error("No Workout found")
        else:
            st.error("Please login first.")
    


       # Delete Workout by ID
    st.subheader("Delete Workout by ID")
    workout_id= st.number_input("Workout ID to delete", min_value=1, step=1)
    if st.button("Delete workout"):
        token = get_session_data('authKey')
        if token:
            response =delete_workout_by_id(token, workout_id)
            if response.status_code == 204 :
                st.write("Deleted Workout Id: ", workout_id )
            else:
                st.error("No workout found")
        else:
            st.error("Please login first.")
 
 
    # # Update Workout by ID
    # st.subheader("Update Workout by ID")
    # exercise_id = st.number_input("enter Exercise ID", min_value=1, step=1)
    # user_id = st.number_input("User ID", min_value=1, step=1)
    # is_set_by_admin:st.selectbox('Choose:', ['True', 'False'])
    # set_count=st.number_input("set_count", min_value=1, step=1)
    # repetition_count=st.number_input("repetition count", min_value=1, step=1)
    # workout_time=st.number_input("workout time", min_value=1, step=1)
 
   
    # workout_data = {
    #     "exercise_id": exercise_id,
    #     "is_set_by_admin": is_set_by_admin,
    #     "set_count": set_count,
    #     "repetition_count": repetition_count,
    #     "workout_time": workout_time
 
    # }
   
    # if st.button("Update workout"):
    #     token = get_session_data('authKey')
    #     if token:
    #         exercise_data = update_workout_by_id(token, workout_data, workout_id)
    #         if workout_data:
    #             st.write("User:", workout_data)
    #         else:
    #             st.error("No workout found")
    #     else:
    #         st.error("Please login first.")    
 
 

    # Create Workout
    st.subheader("Create Workout")
    exercise_id = st.number_input("enter Exercise ID", min_value=1, step=1)
    user_id = st.number_input("Enter User Id ", min_value=1, step=1)
    # is_set_by_admin:st.selectbox('Chooses:', ["true", "false"])
    is_set_by_admin = st.checkbox("Is Set by Admin") 
    # is_set_by_admin:st.text_input(bool)
    set_count=st.number_input("set_count", min_value=1, step=1)
    repetition_count=st.number_input("repetition count", min_value=1, step=1)
    workout_time=st.number_input("workout time", min_value=1, step=1)
 
    workout_data = {
        "exercise_id": exercise_id,
        "is_set_by_admin": is_set_by_admin,
        "set_count": set_count,
        "repetition_count": repetition_count,
        "workout_time": workout_time
 
    }
   
    if st.button("Create Workout"):
        if exercise_id and is_set_by_admin and set_count and repetition_count and workout_time:
            token = get_session_data('authKey')
            if token:
                created_workout = create_workout(workout_data, token)
                st.write(created_workout)
            else:
                st.error("Please login first.")
        else:
            st.warning("Please fill in all the fields.")

      
 
# Define a simple SessionState class
class SessionState:
    def __init__(self):
        self.token = None
 
if __name__ == "__main__":
    main()
 