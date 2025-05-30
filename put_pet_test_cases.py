import requests
import pytest
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

BASE_URL = "https://petstore.swagger.io/v2"
PET_ENDPOINT = BASE_URL + "/pet"

# Object for the PUT /pet request
VALID_PET = {
    "id": 99, #int and immutable
    "category": {"id": 1, "name": "Dogs"}, #single object with id and name
    "name": "Max", #string
    "photoUrls": ["https://example.com/photo.jpg"], #array of strings
    "tags": [{"id": 1, "name": "playful"}], #array of objects with id and name
    "status": "available" #string, can be "available", "pending", or "sold"
}

# fixtures serves to provide data or setup/teardonw logic to tests.
# using module as scope since the pet will be created once and reused across tests existing in this module
@pytest.fixture(scope="module")
# Ensure pet exists before updating
def setup_pet():
    response = requests.post(PET_ENDPOINT, json=VALID_PET)
    assert response.status_code in [200, 201]
    return VALID_PET

#Verify the user can change the pet's category
def test_put_pet_category(setup_pet):
    updated_pet = setup_pet.copy()
    updated_pet["category"] = {"id": 2, "name": "Birds"}

    response = requests.put(PET_ENDPOINT, json=updated_pet)

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    response_json = response.json()
    assert response_json["id"] == updated_pet["id"]
    assert response_json["category"]["id"] == updated_pet["category"]["id"]
    assert response_json["category"]["name"] == updated_pet["category"]["name"]
    
#Verify the user can change the pet's name
def test_put_pet_name(setup_pet):
    updated_pet = setup_pet.copy()
    updated_pet["name"] = "Maximus"

    response = requests.put(PET_ENDPOINT, json=updated_pet)

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    response_json = response.json()
    assert response_json["id"] == updated_pet["id"]
    assert response_json["name"] == updated_pet["name"]

#Verify the user can change the pet's photo URL
def test_put_pet_update_photo_urls(setup_pet):
    updated_pet = setup_pet.copy()
    updated_pet["photoUrls"] = ["https://example.com/photo1.jpg"]

    response = requests.put(PET_ENDPOINT, json=updated_pet)

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    response_json = response.json()
    assert response_json["id"] == updated_pet["id"]
    assert response_json["photoUrls"] == updated_pet["photoUrls"]

#Verify the user can change the pet's tag
def test_put_pet_change_tag(setup_pet):
    updated_pet = setup_pet.copy()
    updated_pet["tags"] = [{"id": 1, "name": "Trained"}]

    response = requests.put(PET_ENDPOINT, json=updated_pet)

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    response_json = response.json()
    assert response_json["id"] == updated_pet["id"]
    assert len(response_json["tags"]) == len(updated_pet["tags"])
    assert response_json["tags"][0]["name"] == updated_pet["tags"][0]["name"]

#Verify the user can change the pet's status
def test_put_pet_change_status(setup_pet):
    updated_pet = setup_pet.copy()
    updated_pet["status"] = "sold"

    # Leaving debug statements to show how I used the logging module to understand what was happening and build the tests
    logging.debug(f"Updating pet status: {updated_pet}")
    response = requests.put(PET_ENDPOINT, json=updated_pet)
    logging.debug(f"Response status: {response.status_code}")
    logging.debug(f"Response body: {response.text}")

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    response_json = response.json()
    assert response_json["id"] == updated_pet["id"]
    assert response_json["status"] == updated_pet["status"]
