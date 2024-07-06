""" Implement the Country and City Management Endpoints """

import requests
import uuid

from tests import test_functions

API_URL = "http://localhost:5000"
country_code = "UY"


def test_get_countries():
    """
    Test to retrieve all countries
    Sends a GET request to /countries and checks that the response status is 200
    and the returned data is a list.
    """
    response = requests.get(f"{API_URL}/countries")
    assert (
        response.status_code == 200
    ), f"Expected status code 200 but got {response.status_code}. Response: {response.text}"
    assert isinstance(
        response.json(), list
    ), f"Expected response to be a list but got {type(response.json())}"


def test_get_country():
    """
    Test to retrieve a specific country by code
    Sends a GET request to /countries/{code} and checks that the response status is 200
    and the returned data contains the expected fields.
    """
    country_code = "UY"  # Use an existing country code for this test
    response = requests.get(f"{API_URL}/countries/{country_code}")
    assert (
        response.status_code == 200
    ), f"Expected status code 200 but got {response.status_code}. Response: {response.text}"
    country_data = response.json()
    assert (
        country_data["code"] == country_code
    ), f"Expected country code to be {country_code} but got {country_data['code']}"
    assert "name" in country_data, "Name not in response"


def test_get_country_cities():
    """
    Test to retrieve all cities for a specific country by code
    Sends a GET request to /countries/{code}/cities and checks that the response status is 200
    and the returned data is a list of cities.
    """
    country_code = "UY"  # Use an existing country code for this test
    response = requests.get(f"{API_URL}/countries/{country_code}/cities")
    assert (
        response.status_code == 200
    ), f"Expected status code 200 but got {response.status_code}. Response: {response.text}"
    cities_data = response.json()
    assert isinstance(
        cities_data, list
    ), f"Expected response to be a list but got {type(cities_data)}"
    # assert len(cities_data) > 0, "Expected at least one city in the response"
    # assert "name" in cities_data[0], "City name not in response"
    # assert "country_code" in cities_data[0], "Country code not in response"


def test_get_cities():
    """
    Test to retrieve all cities
    Sends a GET request to /cities and checks that the response status is 200
    and the returned data is a list.
    """
    response = requests.get(f"{API_URL}/cities")
    assert (
        response.status_code == 200
    ), f"Expected status code 200 but got {response.status_code}. Response: {response.text}"
    assert isinstance(
        response.json(), list
    ), f"Expected response to be a list but got {type(response.json())}"


def test_post_city():
    """
    Test to create a new city
    Sends a POST request to /cities with new city data and checks that the
    response status is 201 and the returned data matches the sent data.
    """
    new_city = {"name": f"Test City {uuid.uuid4()}", "country_code": country_code}
    response = requests.post(f"{API_URL}/cities", json=new_city)
    assert (
        response.status_code == 201
    ), f"Expected status code 201 but got {response.status_code}. Response: {response.text}"
    city_data = response.json()
    assert (
        city_data["name"] == new_city["name"]
    ), f"Expected city name to be {new_city['name']} but got {city_data['name']}"
    assert (
        city_data["country_code"] == new_city["country_code"]
    ), f"Expected country code to be {new_city['country_code']} but got {city_data['country_code']}"
    assert "id" in city_data, "City ID not in response"
    assert "created_at" in city_data, "Created_at not in response"
    assert "updated_at" in city_data, "Updated_at not in response"
    return city_data["id"]  # Return the ID of the created city for further tests


def test_get_city():
    """
    Test to retrieve a specific city by ID
    Creates a new city, then sends a GET request to /cities/{id} and checks that the
    response status is 200 and the returned data matches the created city's data.
    """
    city_id = test_post_city()

    # Retrieve the newly created city
    response = requests.get(f"{API_URL}/cities/{city_id}")
    assert (
        response.status_code == 200
    ), f"Expected status code 200 but got {response.status_code}. Response: {response.text}"
    city_data = response.json()
    assert (
        city_data["id"] == city_id
    ), f"Expected city ID to be {city_id} but got {city_data['id']}"
    assert "name" in city_data, "Name not in response"
    assert "country_code" in city_data, "Country code not in response"
    assert "created_at" in city_data, "Created_at not in response"
    assert "updated_at" in city_data, "Updated_at not in response"


def test_put_city():
    """
    Test to update an existing city
    Creates a new city, then sends a PUT request to /cities/{id} with updated city data
    and checks that the response status is 200 and the returned data matches the updated data.
    """
    city_id = test_post_city()
    updated_city = {"name": f"Updated City {uuid.uuid4()}", "country_code": "US"}
    response = requests.put(f"{API_URL}/cities/{city_id}", json=updated_city)
    assert (
        response.status_code == 200
    ), f"Expected status code 200 but got {response.status_code}. Response: {response.text}"
    city_data = response.json()
    assert (
        city_data["name"] == updated_city["name"]
    ), f"Expected updated city name to be {updated_city['name']} but got {city_data['name']}"
    assert (
        city_data["country_code"] == updated_city["country_code"]
    ), f"Expected updated country code to be {updated_city['country_code']} but got {city_data['country_code']}"
    assert "id" in city_data, "City ID not in response"
    assert "created_at" in city_data, "Created_at not in response"
    assert "updated_at" in city_data, "Updated_at not in response"


def test_delete_city():
    """
    Test to delete an existing city
    Creates a new city, then sends a DELETE request to /cities/{id} and checks that the
    response status is 204 indicating successful deletion.
    """
    city_id = test_post_city()

    # Delete the newly created city
    response = requests.delete(f"{API_URL}/cities/{city_id}")
    assert (
        response.status_code == 204
    ), f"Expected status code 204 but got {response.status_code}. Response: {response.text}"


if __name__ == "__main__":
    # Run the tests
    test_functions(
        [
            test_get_countries,
            test_get_country,
            test_get_country_cities,
            test_get_cities,
            test_post_city,
            test_get_city,
            test_put_city,
            test_delete_city,
        ]
    )
