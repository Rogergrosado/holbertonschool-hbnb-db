""" Implement the Amenity Management Endpoints """

import requests
import uuid
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from src.models.amenity import Amenity, PlaceAmenity
from src.models.base import Base
from src import create_app, db as database

API_URL = "http://localhost:5000"
DB_URL = 'sqlite:///development.db'
os.environ['USE_DATABASE'] = 'true'


def setup_database():
    """
    Helper function to set up the database session and engine.
    """
    engine = create_engine(DB_URL)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def create_unique_amenity():
    """
    Helper function to create a new amenity with a unique name
    Sends a POST request to /amenities with new amenity data and returns the created amenity's ID.
    """
    unique_amenity_name = f"Test Amenity {uuid.uuid4()}"
    new_amenity = {"name": unique_amenity_name}
    response = requests.post(f"{API_URL}/amenities", json=new_amenity)
    assert (
        response.status_code == 201
    ), f"Expected status code 201 but got {response.status_code}. Response: {response.text}"
    return response.json()["id"]


def test_get_amenities():
    """
    Test to retrieve all amenities
    Sends a GET request to /amenities and checks that the response status is 200
    and the returned data is a list.
    """
    response = requests.get(f"{API_URL}/amenities")
    assert (
        response.status_code == 200
    ), f"Expected status code 200 but got {response.status_code}. Response: {response.text}"
    assert isinstance(
        response.json(), list
    ), f"Expected response to be a list but got {type(response.json())}"


def test_post_amenity():
    """
    Test to create a new amenity
    Sends a POST request to /amenities with new amenity data and checks that the
    response status is 201 and the returned data matches the sent data.
    """
    unique_amenity_name = f"Test Amenity {uuid.uuid4()}"
    new_amenity = {"name": unique_amenity_name}
    response = requests.post(f"{API_URL}/amenities", json=new_amenity)
    assert (
        response.status_code == 201
    ), f"Expected status code 201 but got {response.status_code}. Response: {response.text}"
    amenity_data = response.json()
    assert (
        amenity_data["name"] == new_amenity["name"]
    ), f"Expected name to be {new_amenity['name']} but got {amenity_data['name']}"
    assert "id" in amenity_data, "Amenity ID not in response"
    assert "created_at" in amenity_data, "Created_at not in response"
    assert "updated_at" in amenity_data, "Updated_at not in response"
    return amenity_data["id"]  # Return the ID of the created amenity for further tests


def test_get_amenity():
    """
    Test to retrieve a specific amenity by ID
    Creates a new amenity, then sends a GET request to /amenities/{id} and checks that the
    response status is 200 and the returned data matches the created amenity's data.
    """
    amenity_id = create_unique_amenity()

    # Retrieve the newly created amenity
    response = requests.get(f"{API_URL}/amenities/{amenity_id}")
    assert (
        response.status_code == 200
    ), f"Expected status code 200 but got {response.status_code}. Response: {response.text}"
    amenity_data = response.json()
    assert (
        amenity_data["id"] == amenity_id
    ), f"Expected amenity ID to be {amenity_id} but got {amenity_data['id']}"
    assert "name" in amenity_data, "Name not in response"
    assert "created_at" in amenity_data, "Created_at not in response"
    assert "updated_at" in amenity_data, "Updated_at not in response"


def test_put_amenity():
    """
    Test to update an existing amenity
    Creates a new amenity, then sends a PUT request to /amenities/{id} with updated amenity data
    and checks that the response status is 200 and the returned data matches the updated data.
    """
    amenity_id = create_unique_amenity()

    # Update the newly created amenity
    updated_amenity = {"name": f"Updated Amenity {uuid.uuid4()}"}
    response = requests.put(f"{API_URL}/amenities/{amenity_id}", json=updated_amenity)
    assert (
        response.status_code == 200
    ), f"Expected status code 200 but got {response.status_code}. Response: {response.text}"
    amenity_data = response.json()
    assert (
        amenity_data["name"] == updated_amenity["name"]
    ), f"Expected updated name to be {updated_amenity['name']} but got {amenity_data['name']}"
    assert "id" in amenity_data, "Amenity ID not in response"
    assert "created_at" in amenity_data, "Created_at not in response"
    assert "updated_at" in amenity_data, "Updated_at not in response"


def test_delete_amenity():
    """
    Test to delete an existing amenity
    Creates a new amenity, then sends a DELETE request to /amenities/{id} and checks that the
    response status is 204 indicating successful deletion.
    """
    amenity_id = create_unique_amenity()

    # Delete the newly created amenity
    response = requests.delete(f"{API_URL}/amenities/{amenity_id}")
    assert (
        response.status_code == 204
    ), f"Expected status code 204 but got {response.status_code}. Response: {response.text}"


if __name__ == "__main__":
    # Run the tests
    session = setup_database()
    app = create_app(session)
    with app.app_context():
        database.create_all()
    test_get_amenities()
    test_post_amenity()
    test_get_amenity()
    test_put_amenity()
    test_delete_amenity()
