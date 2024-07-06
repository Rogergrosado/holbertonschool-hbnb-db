""" Implement the Review Management Endpoints """

import requests
import uuid

from tests import test_functions

API_URL = "http://localhost:5000"


def create_user():
    """
    Helper function to create a new user with a unique email.
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


def create_city(country_code: str):
    """
    Helper function to create a new city.
    Sends a POST request to /cities with new city data and returns the created city's ID.
    """
    new_city = {"name": "Test City", "country_code": country_code}
    response = requests.post(f"{API_URL}/cities", json=new_city)
    assert (
        response.status_code == 201
    ), f"Expected status code 201 but got {response.status_code}. Response: {response.text}"
    return response.json()["id"]


def create_place():
    """
    Helper function to create a new place
    Sends a POST request to /places with new place data and returns the created place's ID.
    """
    user_id = create_user()
    city_code = create_city("UY")
    new_place = {
        "name": "Cozy Cottage",
        "description": "A cozy cottage in the countryside.",
        "address": "123 Country Lane",
        "latitude": 34.052235,
        "longitude": -118.243683,
        "host_id": user_id,
        "city_id": city_code,
        "price_per_night": 100,
        "number_of_rooms": 2,
        "number_of_bathrooms": 1,
        "max_guests": 4,
    }
    response = requests.post(f"{API_URL}/places", json=new_place)
    assert (
        response.status_code == 201
    ), f"Expected status code 201 but got {response.status_code}. Response: {response.text}"
    return response.json()["id"]


def test_get_reviews_from_place():
    """
    Test to retrieve all reviews from a place
    Sends a GET request to /places/{place_id}/reviews and checks that the response status is 200
    and the returned data is a list.
    """
    place_id = create_place()
    user_id = create_user()
    new_review = {
        "place_id": place_id,
        "user_id": user_id,
        "comment": "Great place to stay!",
        "rating": 5.0,
    }
    response = requests.post(f"{API_URL}/places/{place_id}/reviews", json=new_review)
    assert (
        response.status_code == 201
    ), f"Expected status code 201 but got {response.status_code}. Response: {response.text}"

    review_id = response.json()["id"]

    response = requests.get(f"{API_URL}/places/{place_id}/reviews")
    assert (
        response.status_code == 200
    ), f"Expected status code 200 but got {response.status_code}. Response: {response.text}"
    assert isinstance(
        response.json(), list
    ), f"Expected response to be a list but got {type(response.json())}"

    assert any(
        review["id"] == review_id for review in response.json()
    ), f"Expected review with ID {review_id} to be in response but it wasn't"


def test_get_reviews_from_user():
    """
    Test to retrieve all reviews from a user
    Sends a GET request to /users/{user_id}/reviews and checks that the response status is 200
    and the returned data is a list.
    """
    place_id = create_place()
    user_id = create_user()
    new_review = {
        "place_id": place_id,
        "user_id": user_id,
        "comment": "Great place to stay!",
        "rating": 5.0,
    }
    response = requests.post(f"{API_URL}/places/{place_id}/reviews", json=new_review)
    assert (
        response.status_code == 201
    ), f"Expected status code 201 but got {response.status_code}. Response: {response.text}"

    review_id = response.json()["id"]

    response = requests.get(f"{API_URL}/users/{user_id}/reviews")
    assert (
        response.status_code == 200
    ), f"Expected status code 200 but got {response.status_code}. Response: {response.text}"
    assert isinstance(
        response.json(), list
    ), f"Expected response to be a list but got {type(response.json())}"

    assert any(
        review["id"] == review_id for review in response.json()
    ), f"Expected review with ID {review_id} to be in response but it wasn't"


def test_post_review():
    """
    Test to create a new review
    Sends a POST request to /reviews with new review data and checks that the
    response status is 201 and the returned data matches the sent data.
    """
    place_id = create_place()
    user_id = create_user()
    new_review = {
        "user_id": user_id,
        "comment": "This place is amazing!",
        "rating": 4.5,
    }
    response = requests.post(f"{API_URL}/places/{place_id}/reviews", json=new_review)
    assert (
        response.status_code == 201
    ), f"Expected status code 201 but got {response.status_code}. Response: {response.text}"
    review_data = response.json()
    for key in new_review:
        assert (
            review_data[key] == new_review[key]
        ), f"Expected {key} to be {new_review[key]} but got {review_data[key]}"
    assert "id" in review_data, "Review ID not in response"
    assert "created_at" in review_data, "Created_at not in response"
    assert "updated_at" in review_data, "Updated_at not in response"
    return review_data["id"]  # Return the ID of the created review for further tests


def test_get_review():
    """
    Test to retrieve a specific review by ID
    Creates a new review, then sends a GET request to /reviews/{id} and checks that the
    response status is 200 and the returned data matches the created review's data.
    """
    place_id = create_place()
    user_id = create_user()
    new_review = {
        "place_id": place_id,
        "user_id": user_id,
        "comment": "Great place to stay!",
        "rating": 5.0,
    }
    response = requests.post(f"{API_URL}/places/{place_id}/reviews", json=new_review)
    assert (
        response.status_code == 201
    ), f"Expected status code 201 but got {response.status_code}. Response: {response.text}"
    review_id = response.json()["id"]

    # Retrieve the newly created review
    response = requests.get(f"{API_URL}/reviews/{review_id}")
    assert (
        response.status_code == 200
    ), f"Expected status code 200 but got {response.status_code}. Response: {response.text}"
    review_data = response.json()
    for key in new_review:
        assert (
            review_data[key] == new_review[key]
        ), f"Expected {key} to be {new_review[key]} but got {review_data[key]}"
    assert "id" in review_data, "Review ID not in response"
    assert "created_at" in review_data, "Created_at not in response"
    assert "updated_at" in review_data, "Updated_at not in response"


def test_put_review():
    """
    Test to update an existing review
    Creates a new review, then sends a PUT request to /reviews/{id} with updated review data
    and checks that the response status is 200 and the returned data matches the updated data.
    """
    place_id = create_place()
    user_id = create_user()
    new_review = {
        "user_id": user_id,
        "comment": "Nice place!",
        "rating": 4.0,
    }
    response = requests.post(f"{API_URL}/places/{place_id}/reviews", json=new_review)
    assert (
        response.status_code == 201
    ), f"Expected status code 201 but got {response.status_code}. Response: {response.text}"
    review_id = response.json()["id"]

    # Update the newly created review
    updated_review = {
        "place_id": place_id,
        "user_id": user_id,
        "comment": "Amazing place, had a great time!",
        "rating": 4.8,
    }
    response = requests.put(f"{API_URL}/reviews/{review_id}", json=updated_review)
    assert (
        response.status_code == 200
    ), f"Expected status code 200 but got {response.status_code}. Response: {response.text}"
    review_data = response.json()
    for key in updated_review:
        assert (
            review_data[key] == updated_review[key]
        ), f"Expected updated {key} to be {updated_review[key]} but got {review_data[key]}"
    assert "id" in review_data, "Review ID not in response"
    assert "created_at" in review_data, "Created_at not in response"
    assert "updated_at" in review_data, "Updated_at not in response"


def test_delete_review():
    """
    Test to delete an existing review
    Creates a new review, then sends a DELETE request to /reviews/{id} and checks that the
    response status is 204 indicating successful deletion.
    """
    place_id = create_place()
    user_id = create_user()
    new_review = {
        "user_id": user_id,
        "comment": "Decent place.",
        "rating": 3.5,
    }
    response = requests.post(f"{API_URL}/places/{place_id}/reviews", json=new_review)
    assert (
        response.status_code == 201
    ), f"Expected status code 201 but got {response.status_code}. Response: {response.text}"
    review_id = response.json()["id"]

    # Delete the newly created review
    response = requests.delete(f"{API_URL}/reviews/{review_id}")
    assert (
        response.status_code == 204
    ), f"Expected status code 204 but got {response.status_code}. Response: {response.text}"


if __name__ == "__main__":
    # Run the tests
    test_functions(
        [
            test_get_reviews_from_place,
            test_get_reviews_from_user,
            test_post_review,
            test_get_review,
            test_put_review,
            test_delete_review,
        ]
    )
