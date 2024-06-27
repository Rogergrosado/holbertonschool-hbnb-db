-- Create database
CREATE DATABASE hbnb;

-- Use the database
USE hbnb;

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

-- Insert initial data into Users table
INSERT INTO users (username, email, password, first_name, last_name) VALUES
('host1', 'host1@example.com', 'password1', 'Host', 'One'),
('guest1', 'guest1@example.com', 'password2', 'Guest', 'One');

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
    host_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    address VARCHAR(255) NOT NULL,
    city_id INT NOT NULL,
    country VARCHAR(100) NOT NULL,
    price_per_night DECIMAL(10, 2) NOT NULL,
    max_guests INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (host_id, city_id) REFERENCES users(id)
);

-- Insert initial data into Places table
INSERT INTO places (host_id, title, description, address, city, country, price_per_night, max_guests) VALUES
(1, 'Cozy Cottage', 'A cozy cottage in the countryside', '123 Country Lane', 'Countryside', 'USA', 100.00, 4),
(1, 'Modern Apartment', 'A modern apartment in the city center', '456 City Street', 'Cityville', 'USA', 150.00, 2);

-- Create Amenities table
CREATE TABLE amenities (
    id VARCHAR(36) PRIMARY KEY,
    place_id VARCHAR(36) NOT NULL,
    name VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (place_id) REFERENCES places(id)
);

-- Insert initial data into Amenities table
INSERT INTO amenities (name) VALUES
('WiFi'),
('Air Conditioning'),
('Kitchen'),
('Parking');

-- Create Place_Amenities table (for many-to-many relationship)
CREATE TABLE place_amenities (
    place_id INT NOT NULL,
    amenity_id INT NOT NULL,
    PRIMARY KEY (place_id, amenity_id),
    FOREIGN KEY (place_id) REFERENCES places(id),
    FOREIGN KEY (amenity_id) REFERENCES amenities(id)
);

-- Insert initial data into Place_Amenities table
INSERT INTO place_amenities (place_id, amenity_id) VALUES
(1, 1), -- Cozy Cottage has WiFi
(1, 3), -- Cozy Cottage has Kitchen
(2, 1), -- Modern Apartment has WiFi
(2, 2), -- Modern Apartment has Air Conditioning
(2, 4); -- Modern Apartment has Parking

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

-- Insert initial data into Reviews table
INSERT INTO reviews (place_id, user_id, rating, comment) VALUES
(1, 2, 5, 'Amazing stay! The cottage was cozy and comfortable.'),
(2, 2, 4, 'Great location and amenities, but a bit noisy at night.');
