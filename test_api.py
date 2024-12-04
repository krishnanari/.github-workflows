# test_api.py
import pytest
from fastapi.testclient import TestClient
from main import app  # Import the FastAPI app from main.py

# Create an instance of TestClient to test the FastAPI app
client = TestClient(app)

def test_predict_rating_valid_input():
    # Test with valid data
    response = client.post("/predict/", json={
        "user_id": 1,
        "movie_id": 50,
        "gender": 1,
        "occupation": 2,
        "age": 25,
        "release_year": 2000,
        "release_month": 5
    })
    
    # Check that the status code is 200 OK
    assert response.status_code == 200
    
    # Check that the response contains 'predicted_rating'
    response_json = response.json()
    assert "predicted_rating" in response_json
    
    # Ensure that the predicted rating is an integer
    assert isinstance(response_json["predicted_rating"], int)

def test_predict_rating_missing_user_id():
    # Test for missing 'user_id' field in the request
    response = client.post("/predict/", json={
        "movie_id": 50,
        "gender": 1,
        "occupation": 2,
        "age": 25,
        "release_year": 2000,
        "release_month": 5
    })
    
    # Check that the status code is 422 Unprocessable Entity (field is missing)
    assert response.status_code == 422
    
    # Check if the error message is related to the missing user_id
    response_json = response.json()
    assert "detail" in response_json
    assert "user_id" in str(response_json["detail"])

def test_predict_rating_invalid_age():
    # Test with an invalid 'age' field (negative value)
    response = client.post("/predict/", json={
        "user_id": 1,
        "movie_id": 50,
        "gender": 1,
        "occupation": 2,
        "age": -5,  # Invalid age
        "release_year": 2000,
        "release_month": 5
    })
    
    # Check if the response status is 422 (Unprocessable Entity) due to validation failure
    assert response.status_code == 422

def test_predict_rating_edge_case():
    # Test with edge case values (high user_id and movie_id)
    response = client.post("/predict/", json={
        "user_id": 99999,  # High user_id value
        "movie_id": 99999,  # High movie_id value
        "gender": 1,
        "occupation": 5,
        "age": 30,
        "release_year": 2010,
        "release_month": 12
    })
    
    # Check that the response contains 'predicted_rating'
    assert response.status_code == 200
    response_json = response.json()
    assert "predicted_rating" in response_json
    assert isinstance(response_json["predicted_rating"], int)

def test_predict_rating_invalid_json_format():
    # Test with incorrect JSON format (invalid keys)
    response = client.post("/predict/", data="user_id=1&movie_id=50")
    
    # Check for a bad request response (400 status code)
    assert response.status_code == 400