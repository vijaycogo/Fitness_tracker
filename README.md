# Fitness Tracker

Build a FastAPI-based API for tracking and managing fitness activities, workouts, and progress

## Components

- **FastAPI**: Utilizes the FastAPI framework for building high-performance APIs with Python 3.10.
- **SQLite3**: Stores operators in a MongoDB database for efficient and scalable data storage.

- **pipenv**: Handles Python dependencies and virtual environment management.

## Prerequisites

Before running the Project, make sure you have the following installed:

- Python 3.10 or later
- SQLite3 (with connection details available)

## Getting Started

* Clone the repository:

```bash
git clone git@github.com:vijaycogo/Fitness_tracker.git

```

* Create a virtual environment and install the required dependencies:

```bash
python -m venv myenv
```

* Activate the virtual environment:

```bash
myenv\Scripts\activate
```


* Run the FastAPI server:

```bash
uvicorn main:app --port 8000 --reload
```

The server will start running at `http://localhost:8000`. You can access the interactive API documentation at `http://localhost:8000/docs`.

* Run the Unit test Cases:

```bash
python3 -m unittest app.routers.file_name like(python3 -m unittest app.routers.test_exercise, python3 -m unittest app.routers.test_user)
```


## API Endpoints

The Fitness Project provides the following API endpoints:

### User Endpoints
- `GET /users/`             : Get all user.
- `POST /create_user/`      : Create a new user.
- `PUT /users/{user_id}/`   : Update user information.
- `DELETE /users/{user_id}/`: Delete User Information.


### Workout Endpoints

- `POST /workouts/`                 : Create a new workout session.
- `GET /workouts/{workout_id}/`     : Retrieve information about a specific workout.
- `GET /workouts/user/{user_id}/`   : Retrieve all workouts for a specific user.
- `PUT /workouts/{workout_id}/`     : Update information about a specific workout.
- `DELETE /workouts/{workout_id}/`  : Delete a specific workout session.

### Exercise Endpoints

- `POST /exercises/`                     : Add a new exercise to a workout.
- `GET /exercises/{exercise_id}/`        : Retrieve information about a specific exercise.
- `GET /exercises/workout/{workout_id}/` : Retrieve all exercises for a specific workout.
- `PUT /exercises/{exercise_id}/`        : Update information about a specific exercise.
- `DELETE /exercises/{exercise_id}/`     : Delete a specific exercise

 
## How to run the Project
- Install SQllite, SQLalchemy
- Install Python
- Git clone the project
- Create your virtualenv with `conda create` and activate it.
- Install the requirements with ``` pip install -r requirements.txt ```
- Set Up your SQLlite database and set its URI in your ```database.py```
 
- Create your database by running ``` python init_db.py ```
- Finally run the API
``` uvicorn main:app ``