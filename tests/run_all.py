from tests import test_functions

import tests.test_amenities as test_amenities
import tests.test_countries as test_countries
import tests.test_users as test_users
import tests.test_reviews as test_reviews
import tests.test_places as test_places


def main():
    print(f"Executing tests: '{test_users.__doc__}'")
    r1 = test_functions(
        [
            test_users.test_get_users,
            test_users.test_get_user,
            test_users.test_post_user,
            test_users.test_put_user,
            test_users.test_delete_user,
        ]
    )

    print(f"Executing tests: '{test_countries.__doc__}'")
    r2 = test_functions(
        [
            test_countries.test_get_countries,
            test_countries.test_get_country,
            test_countries.test_get_country_cities,
            test_countries.test_get_cities,
            test_countries.test_get_city,
            test_countries.test_post_city,
            test_countries.test_put_city,
            test_countries.test_delete_city,
        ]
    )

    print(f"Executing tests: '{test_amenities.__doc__}'")
    r3 = test_functions(
        [
            test_amenities.test_get_amenities,
            test_amenities.test_get_amenity,
            test_amenities.test_post_amenity,
            test_amenities.test_put_amenity,
            test_amenities.test_delete_amenity,
        ]
    )

    print(f"Executing tests: '{test_places.__doc__}'")
    r4 = test_functions(
        [
            test_places.test_get_places,
            test_places.test_get_place,
            test_places.test_post_place,
            test_places.test_put_place,
            test_places.test_delete_place,
        ]
    )

    print(f"Executing tests: '{test_reviews.__doc__}'")
    r5 = test_functions(
        [
            test_reviews.test_get_reviews_from_place,
            test_reviews.test_get_reviews_from_user,
            test_reviews.test_get_review,
            test_reviews.test_post_review,
            test_reviews.test_put_review,
            test_reviews.test_delete_review,
        ]
    )

    tests = [
        (r1, test_users.__doc__),
        (r2, test_countries.__doc__),
        (r3, test_amenities.__doc__),
        (r4, test_places.__doc__),
        (r5, test_reviews.__doc__),
    ]

    print("# ------------------------- #")
    print("Results (Passed/Total):")
    for results, docstring in tests:
        print(f"{docstring.strip()} ({results['ok']}/{results['total']}):")
        print(f"Score: {results['ok']/results['total'] * 100}%")


if __name__ == "__main__":
    main()
