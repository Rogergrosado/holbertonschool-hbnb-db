""" Implement the Places Management Endpoints """

import requests
import uuid

from tests import test_functions

API_URL = "http://localhost:5000"


def create_unique_user():
    """
    Helper function to create a new user with a unique email
    Sends a POST request to /users with new user data and returns the created user's ID.
    """
    unique_email = f"test.user.{uuid.uuid4()}@example.com"
    new_user = {
        "email": unique_email,
        "first_name": "Test",
        "last_name": "User",
    }
    response = requests.post(f"{API_URL}/users", json=new_user)
    assert (
        response.status_code == 201
    ), f"Expected status code 201 but got {response.status_code}. Response: {response.text}"
    return response.json()["id"]


def create_city():
    """
    Helper function to create a new city
    Sends a POST request to /cities with new city data and returns the created city's ID.
    """
    new_city = {"name": "Test City", "country_code": "UY"}
    response = requests.post(f"{API_URL}/cities", json=new_city)
    assert (
        response.status_code == 201
    ), f"Expected status code 201 but got {response.status_code}. Response: {response.text}"
    return response.json()["id"]


def test_get_places():
    """
    Test to retrieve all places
    Sends a GET request to /places and checks that the response status is 200
    and the returned data is a list.
    """
    response = requests.get(f"{API_URL}/places")
    assert (
        response.status_code == 200
    ), f"Expected status code 200 but got {response.status_code}. Response: {response.text}"
    assert isinstance(
        response.json(), list
    ), f"Expected response to be a list but got {type(response.json())}"


def test_post_place():
    """
    Test to create a new place
    Sends a POST request to /places with new place data and checks that the
    response status is 201 and the returned data matches the sent data.
    """
    city_id = create_city()
    user_id = create_unique_user()
    new_place = {
        "name": "Cozy Cottage",
        "description": "A cozy cottage in the countryside.",
        "address": "123 Country Lane",
        "latitude": 34.052235,
        "longitude": -118.243683,
        "host_id": user_id,
        "city_id": city_id,
        "price_per_night": 100,
        "number_of_rooms": 2,
        "number_of_bathrooms": 1,
        "max_guests": 4,
    }
    response = requests.post(f"{API_URL}/places", json=new_place)
    assert (
        response.status_code == 201
    ), f"Expected status code 201 but got {response.status_code}. Response: {response.text}"
    place_data = response.json()
    for key in new_place:
        assert (
            place_data[key] == new_place[key]
        ), f"Expected {key} to be {new_place[key]} but got {place_data[key]}"
    assert "id" in place_data, "Place ID not in response"
    assert "created_at" in place_data, "Created_at not in response"
    assert "updated_at" in place_data, "Updated_at not in response"
    return place_data["id"]  # Return the ID of the created place for further tests


def test_get_place():
    """
    Test to retrieve a specific place by ID
    Creates a new place, then sends a GET request to /places/{id} and checks that the
    response status is 200 and the returned data matches the created place's data.
    """
    city_id = create_city()
    user_id = create_unique_user()
    new_place = {
        "name": "Sunny Villa",
        "description": "A sunny villa near the beach.",
        "address": "456 Beach Road",
        "latitude": 36.778259,
        "longitude": -119.417931,
        "host_id": user_id,
        "city_id": city_id,
        "price_per_night": 200,
        "number_of_rooms": 3,
        "number_of_bathrooms": 2,
        "max_guests": 6,
    }
    response = requests.post(f"{API_URL}/places", json=new_place)
    assert (
        response.status_code == 201
    ), f"Expected status code 201 but got {response.status_code}. Response: {response.text}"
    place_id = response.json()["id"]

    # Retrieve the newly created place
    response = requests.get(f"{API_URL}/places/{place_id}")
    assert (
        response.status_code == 200
    ), f"Expected status code 200 but got {response.status_code}. Response: {response.text}"
    place_data = response.json()
    for key in new_place:
        assert (
            place_data[key] == new_place[key]
        ), f"Expected {key} to be {new_place[key]} but got {place_data[key]}"
    assert "id" in place_data, "Place ID not in response"
    assert "created_at" in place_data, "Created_at not in response"
    assert "updated_at" in place_data, "Updated_at not in response"


def test_put_place():
    """
    Test to update an existing place
    Creates a new place, then sends a PUT request to /places/{id} with updated place data
    and checks that the response status is 200 and the returned data matches the updated data.
    """
    city_id = create_city()
    user_id = create_unique_user()
    new_place = {
        "name": "Mountain Retreat",
        "description": "A peaceful retreat in the mountains.",
        "address": "789 Mountain Path",
        "latitude": 40.712776,
        "longitude": -74.005974,
        "host_id": user_id,
        "city_id": city_id,
        "price_per_night": 150,
        "number_of_rooms": 4,
        "number_of_bathrooms": 3,
        "max_guests": 8,
    }
    response = requests.post(f"{API_URL}/places", json=new_place)
    assert (
        response.status_code == 201
    ), f"Expected status code 201 but got {response.status_code}. Response: {response.text}"
    place_id = response.json()["id"]

    # Update the newly created place
    updated_place = {
        "name": "Lakeside Cabin",
        "description": "A charming cabin by the lake.",
        "address": "101 Lakeside Drive",
        "latitude": 38.89511,
        "longitude": -77.03637,
        "host_id": user_id,
        "city_id": city_id,
        "price_per_night": 180,
        "number_of_rooms": 3,
        "number_of_bathrooms": 2,
        "max_guests": 6,
    }
    response = requests.put(f"{API_URL}/places/{place_id}", json=updated_place)
    assert (
        response.status_code == 200
    ), f"Expected status code 200 but got {response.status_code}. Response: {response.text}"
    place_data = response.json()
    for key in updated_place:
        assert (
            place_data[key] == updated_place[key]
        ), f"Expected updated {key} to be {updated_place[key]} but got {place_data[key]}"
    assert "id" in place_data, "Place ID not in response"
    assert "created_at" in place_data, "Created_at not in response"
    assert "updated_at" in place_data, "Updated_at not in response"


def test_delete_place():
    """
    Test to delete an existing place
    Creates a new place, then sends a DELETE request to /places/{id} and checks that the
    response status is 204 indicating successful deletion.
    """
    city_id = create_city()
    user_id = create_unique_user()
    new_place = {
        "name": "Urban Apartment",
        "description": "A modern apartment in the city center.",
        "address": "202 City Plaza",
        "latitude": 37.774929,
        "longitude": -122.419418,
        "host_id": user_id,
        "city_id": city_id,
        "price_per_night": 120,
        "number_of_rooms": 2,
        "number_of_bathrooms": 1,
        "max_guests": 4,
    }
    response = requests.post(f"{API_URL}/places", json=new_place)
    assert (
        response.status_code == 201
    ), f"Expected status code 201 but got {response.status_code}. Response: {response.text}"
    place_id = response.json()["id"]

    # Delete the newly created place
    response = requests.delete(f"{API_URL}/places/{place_id}")
    assert (
        response.status_code == 204
    ), f"Expected status code 204 but got {response.status_code}. Response: {response.text}"


if __name__ == "__main__":
    # Run the tests
    test_functions(
        [
            test_get_places,
            test_post_place,
            test_get_place,
            test_put_place,
            test_delete_place,
        ]
    )
