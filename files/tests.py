import json

import requests

# Define the base URL of the API
base_url = "http://petstore.swagger.io/v1"


# Test the listPets endpoint
def test_list_pets():
    # Define the URL of the endpoint
    url = base_url + "/pets"

    # Define the query parameter
    params = {"limit": 10}

    # Send a GET request to the endpoint
    response = requests.get(url, params=params)

    # Check if the response status code is 200 OK
    assert response.status_code == 200

    # Check if the response contains a paged array of pets
    assert "pets" in json.loads(response.text)


# Test the createPets endpoint
def test_create_pet():
    # Define the URL of the endpoint
    url = base_url + "/pets"

    # Define the payload
    payload = {"name": "Fluffy", "tag": "cat"}

    # Send a POST request to the endpoint
    response = requests.post(url, json=payload)

    # Check if the response status code is 201 Created
    assert response.status_code == 201

    # Check if the response body is null
    assert response.text == ""


# Test the showPetById endpoint
def test_show_pet_by_id():
    # Define the URL of the endpoint
    url = base_url + "/pets/1"

    # Send a GET request to the endpoint
    response = requests.get(url)

    # Check if the response status code is 200 OK
    assert response.status_code == 200

    # Check if the response contains the pet with id 1
    assert json.loads(response.text)["id"] == 1
