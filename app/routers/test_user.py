import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app
from app.repository import user
from app.enum.user_enum import UserRole
from fastapi import Depends, status
from sqlalchemy.orm import Session
from app import oauth2

class TestUserEndpoints(unittest.TestCase):

    def setUp(self):        # Set up the test client and mock dependencies.
        self.client = TestClient(app)

    @patch('app.oauth2.token.verify_token')
    @patch('app.repository.user.show')

    # Test retrieving user information.
    def test_get_user(self, mock_show_user, mock_verify_token):
        # Mock the get_current_user function
        mock_user = MagicMock(id=1, name="shree", email="shree@gmail.com", role=UserRole.admin)
        mock_verify_token.return_value = mock_user

        # Mock the show_user function
        mock_user_data = MagicMock(id=1, name="shree", email="shree@gmail.com", role=UserRole.admin)
        mock_user_data.name = "shree"
        mock_show_user.return_value = mock_user_data

        # Make a request to the /user/{id} endpoint with a valid token
        response = self.client.get("/user/1", headers={"Authorization": "Bearer valid_token"})

        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Assert that the response JSON matches the expected data
        expected_data = {
            "id": 1,
            "name": "shree",
            "email": "shree@gmail.com",
            "role": "admin" 
        }
        self.assertDictEqual({k: v for k, v in response.json().items() if k in expected_data}, expected_data)

    @patch('app.oauth2.token.verify_token')
    @patch('app.repository.user.destroy')

    # Test deleting a user.
    def test_delete_user(self, mock_destroy_user, mock_verify_token):
        # Mock the get_current_user function
        mock_user = MagicMock(id=1, name="shree", email="shree@gmail.com", role=UserRole.admin)
        mock_verify_token.return_value = mock_user

        # Mock the destroy_user function
        mock_destroy_user.return_value = None

        response = self.client.delete("/user/1", headers={"Authorization": "Bearer valid_token"})
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.text, "")


    @patch('app.oauth2.token.verify_token')
    @patch('app.repository.user.update')

    # test updating a User
    def test_update_user(self, mock_update_user, mock_verify_token):
        # Mock the get_current_user function
        mock_user = MagicMock(id=1, name="shree", email="shree@gmail.com", role=UserRole.admin)
        mock_verify_token.return_value = mock_user

        # Mock the update_user function
        mock_update_user.return_value = None

        update_data = {
        "name": "ShreeKanti",
        "email": "shreekanti@gmail.com",
        "role": "admin",  
        "password": "shree1"  
    }

        
        response = self.client.put("/user/1", json=update_data, headers={"Authorization": "Bearer valid_token"})
    
        self.assertEqual(response.status_code, 202)
        self.assertEqual(response.text.strip(), '"User updated successfully"')


    @patch('app.oauth2.token.verify_token')
    @patch('app.repository.user.create')


    # Test creating a User
    def test_create_user(self, mock_create_user, mock_verify_token):
        # Mock the get_current_user function
        mock_user = MagicMock(id=1, name="shree", email="shree@gmail.com", role=UserRole.admin)
        mock_verify_token.return_value = mock_user
        # Mock the create_user function
        mock_user_data = MagicMock(id=1, name="shree", email="shree@gmail.com", role=UserRole.admin)
        mock_user_data.name = "shree"
        mock_create_user.return_value = mock_user_data

        user_data = {
        "name": "shree",
        "email": "shree@gmail.com",
        "role": "admin",
        "password": "shree" 
    }

        response = self.client.post("/user/", json=user_data, headers={"Authorization": "Bearer valid_token"})
        if response.status_code != 200:
            print(response.json())
        self.assertEqual(response.status_code, 200)
        created_user = response.json()
        self.assertEqual(created_user["name"], "shree")

    @patch('app.oauth2.token.verify_token')
    @patch('app.repository.user.get_all_user')

    # test getting all Users
    def test_get_all_users(self, mock_get_all_user, mock_verify_token):
        # Mock the get_current_user function
        mock_user = MagicMock(id=1, name="shree", email="shree@gmail.com", role=UserRole.admin)
        mock_verify_token.return_value = mock_user

        # Mock the get_all_user function
        mock_user_data = [
            MagicMock(id=1, name="shree", email="shree@gmail.com", role=UserRole.admin)
        ]
        mock_user_data[0].name = "shree"
        mock_get_all_user.return_value = mock_user_data

        response = self.client.get("/user/", headers={"Authorization": "Bearer valid_token"})
        self.assertEqual(response.status_code, 200)
        users = response.json()
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0]["name"], "shree")


if __name__ == '__main__':
    unittest.main()