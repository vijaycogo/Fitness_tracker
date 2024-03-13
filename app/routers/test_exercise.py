import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app
from app.enum.exercise_enum import IndoorOutdoorExerciseType, MeasurementType, MajorMinorExerciseType
from app.enum.user_enum import UserRole

class TestExerciseEndpoints(unittest.TestCase):

    def setUp(self):        # Setup the test client 
        self.client = TestClient(app)

    @patch('app.oauth2.token.verify_token')
    @patch('app.repository.exercise.create')
    def test_create_exercise(self, mock_create_exercise, mock_verify_token):        # Test creating an exercise.
        # Mock the get_current_user function
        mock_user = MagicMock(id=1, name="shree", email="shree@gmail.com", role="admin")
        mock_verify_token.return_value = mock_user

        # Mock the create_exercise function
        mock_user_data = MagicMock(id=1, name="shree", email="shree@gmail.com", role="admin")
        mock_user_data.name = "shree"
        mock_exercise_data = MagicMock(id=1, exercise_name="Running", exercise_type=IndoorOutdoorExerciseType.outdoors, measurement_type=MeasurementType.time, 
                                       major_minor_type=MajorMinorExerciseType.mazor, added_by="admin", user=mock_user_data)
        mock_create_exercise.return_value = mock_exercise_data
        exercise_data = {
            "exercise_name": "Running",
            "exercise_type": "outdoors",
            "measurement_type": "time",
            "major_minor_type": "mazor",
            "per_count_second_unit_calorie": 10,  
            "added_by": "admin" 
        }

        # Make a request to the /exercise/ endpoint with a valid token
        response = self.client.post("/exercise/", json=exercise_data, headers={"Authorization": "Bearer valid_token"})

        # Assert that the response status code is 201
        self.assertEqual(response.status_code, 201)

        created_exercise = response.json()
        self.assertEqual(created_exercise["exercise_name"], "Running")

    @patch('app.oauth2.token.verify_token')
    @patch('app.repository.exercise.get_all')

    # Test getting all exercises
    def test_get_all_exercises(self, mock_get_all_exercises, mock_verify_token):
        # Mock the get_current_user function
        mock_user = MagicMock(id=1, name="shree", email="shree@gmail.com", role="admin")
        mock_verify_token.return_value = mock_user

        # Mock the exercise items returned by the database
        mock_user_data = MagicMock(id=1, name="shree", email="shree@gmail.com", role="admin")
        mock_user_data.name = "shree"
        mock_exercise_items = [
            MagicMock(id=1, exercise_name="Running", exercise_type=IndoorOutdoorExerciseType.outdoors, measurement_type=MeasurementType.time,
                       major_minor_type=MajorMinorExerciseType.mazor, added_by="admin", user=mock_user_data),
            MagicMock(id=2, exercise_name="Walking", exercise_type=IndoorOutdoorExerciseType.indoors, measurement_type=MeasurementType.time,
                       major_minor_type=MajorMinorExerciseType.minor, added_by="admin", user=mock_user_data)
        ]
        mock_get_all_exercises.return_value = mock_exercise_items

        # Make a request to the /exercise/ endpoint with a valid token
        response = self.client.get("/exercise/", headers={"Authorization": "Bearer valid_token"})

        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200)

        
        returned_exercises = response.json()

    
        self.assertEqual(len(returned_exercises), 2)
        self.assertEqual(returned_exercises[0]["exercise_name"], "Running")
        self.assertEqual(returned_exercises[1]["exercise_name"], "Walking")
        self.assertEqual(returned_exercises[0]["measurement_type"], "time")
        

    @patch('app.oauth2.token.verify_token')
    @patch('app.repository.exercise.show')

    # Test getting a specific exercise.
    def test_get_exercise(self, mock_get_exercise, mock_verify_token):
        # Mock the get_current_user function
        mock_user = MagicMock(id=1, name="shree", email="shree@gmail.com", role="admin")
        mock_verify_token.return_value = mock_user

        # Mock the exercise items returned by the database
        mock_user_data = MagicMock(id=1, name="shree", email="shree@gmail.com", role="admin")
        mock_user_data.name = "shree"
        mock_exercise_items = MagicMock(id=1, exercise_name="Running", exercise_type=IndoorOutdoorExerciseType.outdoors, measurement_type=MeasurementType.time,
                       major_minor_type=MajorMinorExerciseType.mazor, added_by="admin", user=mock_user_data)
        
        mock_get_exercise.return_value = mock_exercise_items

        # Make a request to the /exercise/ endpoint with a valid token
        response = self.client.get("/exercise/1", headers={"Authorization": "Bearer valid_token"})

        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200)

         # Assert that the response JSON contains the expected exercise data
        returned_exercise = response.json()
        self.assertEqual(returned_exercise["id"], 1)
        self.assertEqual(returned_exercise["exercise_name"], "Running")
        self.assertEqual(returned_exercise["exercise_type"], "outdoors")
        self.assertEqual(returned_exercise["measurement_type"], "time")
        self.assertEqual(returned_exercise["per_count_second_unit_calorie"], 1)

        
    @patch('app.oauth2.token.verify_token')
    @patch('app.repository.exercise.update')

    # Test uodating exercise
    def test_update_exercise(self, mock_update_exercise, mock_verify_token):
        # Mock the get_current_user function
        mock_user = MagicMock(id=1, name="shree", email="shree@gmail.com", role="admin")
        mock_verify_token.return_value = mock_user


        mock_update_exercise.return_value = None

        update_data = {
            "exercise_name": "Running1",
            "exercise_type": "indoors",
            "measurement_type": "time",
            "per_count_second_unit_calorie": 10,
            "added_by": "admin",
            "major_minor_type": "minor"
        }

        
        response = self.client.put("/exercise/1", json=update_data, headers={"Authorization": "Bearer valid_token"})
    
        self.assertEqual(response.status_code, 202)
        self.assertEqual(response.text.strip(), '"Exercise updated successfully"')
        

    @patch('app.oauth2.token.verify_token')
    @patch('app.repository.exercise.destroy')

    # Test deleting exercise
    def test_delete_user(self, mock_destroy_exercise, mock_verify_token):
        # Mock the get_current_user function
        mock_user = MagicMock(id=1, name="shree", email="shree@gmail.com", role=UserRole.admin)
        mock_verify_token.return_value = mock_user

        # Mock the destroy_user function
        mock_destroy_exercise.return_value = None

        response = self.client.delete("/exercise/1", headers={"Authorization": "Bearer valid_token"})
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.text, "")


    

if __name__ == '__main__':
    unittest.main()
