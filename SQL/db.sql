-- Create Users table
CREATE TABLE users (
    id INT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create countries table
CREATE TABLE countries (
    code CHAR(2) PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

-- Create cities table
CREATE TABLE cities (
    id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    country_code CHAR(2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (country_code) REFERENCES countries(code)
);

-- Create Places table
CREATE TABLE places (
    id INT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    address VARCHAR(255) NOT NULL,
    city_id INT NOT NULL,
    country CHAR(2) NOT NULL,
    price_per_night DECIMAL(10, 2) NOT NULL,
    max_guests INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (city_id) REFERENCES cities(id)
);

-- Create Amenities table
CREATE TABLE amenities (
    id INT PRIMARY KEY,
    name VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create Place_Amenities table (for many-to-many relationship)
CREATE TABLE place_amenities (
    place_id INT NOT NULL,
    amenity_id INT NOT NULL,
    PRIMARY KEY (place_id, amenity_id),
    FOREIGN KEY (place_id) REFERENCES places(id),
    FOREIGN KEY (amenity_id) REFERENCES amenities(id)
);

-- Create Reviews table
CREATE TABLE reviews (
    id INT PRIMARY KEY,
    place_id INT NOT NULL,
    user_id INT NOT NULL,
    rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (place_id) REFERENCES places(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Insert initial data into Users table
INSERT INTO users (id, username, email, password, first_name, last_name)
VALUES (1, 'johndoe', 'john@example.com', 'hashedpassword', 'John', 'Doe');

-- Insert initial data into Countries table
INSERT INTO countries (code, name)
VALUES ('US', 'United States');

-- Insert initial data into Cities table
INSERT INTO cities (id, name, country_code)
VALUES (1, 'New York', 'US');

-- Insert initial data into Places table
INSERT INTO places (id, user_id, title, description, address, city_id, country, price_per_night, max_guests)
VALUES (1, 1, 'Cozy Apartment', 'A nice and cozy apartment in the city center.', '123 Main St', 1, 'US', 75.00, 2);

-- Insert initial data into Amenities table
INSERT INTO amenities (id, name)
VALUES (1, 'Wi-Fi');

-- Insert initial data into Place_Amenities table
INSERT INTO place_amenities (place_id, amenity_id)
VALUES (1, 1);

-- Insert initial data into Reviews table
INSERT INTO reviews (id, place_id, user_id, rating, comment)
VALUES (1, 1, 1, 5, 'Great place!');

-- Display data from all tables
SELECT 'Users' AS table_name;
SELECT * FROM users;

SELECT 'Countries' AS table_name;
SELECT * FROM countries;

SELECT 'Cities' AS table_name;
SELECT * FROM cities;

SELECT 'Places' AS table_name;
SELECT * FROM places;

SELECT 'Amenities' AS table_name;
SELECT * FROM amenities;

SELECT 'Place Amenities' AS table_name;
SELECT * FROM place_amenities;

SELECT 'Reviews' AS table_name;
SELECT * FROM reviews;
