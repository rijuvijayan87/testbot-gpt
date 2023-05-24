import pytest
import requests

# Set up the base URL for the API
BASE_URL = "http://petstore.swagger.io/v1"


# Test case for listing all pets
def test_list_pets():
    # Send GET request to /pets endpoint
    response = requests.get(BASE_URL + "/pets")

    # Assert that the response status code is 200 OK
    assert response.status_code == 200

    # Assert that the response headers contain the x-next header
    assert "x-next" in response.headers


# Test case for creating a new pet
def test_create_pet():
    # Define the payload for the POST request
    payload = {"id": 123, "name": "Fido", "tag": "dog"}

    # Send POST request to /pets endpoint with the payload
    response = requests.post(BASE_URL + "/pets", json=payload)

    # Assert that the response status code is 201 Created
    assert response.status_code == 201


# Test case for retrieving info for a specific pet
def test_show_pet_by_id():
    # Send GET request to /pets/{petId} endpoint with petId = 123
    response = requests.get(BASE_URL + "/pets/123")

    # Assert that the response status code is 200 OK
    assert response.status_code == 200

    # Assert that the response body contains the expected pet properties
    response_json = response.json()
    assert response_json["id"] == 123
    assert response_json["name"] == "Fido"
    assert response_json["tag"] == "dog"


# Run the tests with Pytest
pytest.main()
