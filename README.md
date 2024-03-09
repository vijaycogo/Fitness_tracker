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
git clone 

```

* Run the FastAPI server:

```bash
uvicorn main:app --port 8000 --reload
```

The server will start running at `http://localhost:8000`. You can access the interactive API documentation at `http://localhost:8000/docs`.

## API Endpoints

The Fitness Project provides the following API endpoints:

- `GET /create_user/`: Healthcheck endpoint for Operator Service.


<!-- ## Remove table schema and create -->
<!-- rm ./app/fitness.db -->

<!-- python3 database.py -->
