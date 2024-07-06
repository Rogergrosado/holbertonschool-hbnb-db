# HBNB Solution Part 1

This solution successfully implements the repository pattern.
It passes the tests provided in the `/hbnb/part1/tests` directory.

## Some things to note

- Doesn't implement the place_amenities `endpoints` yet.
- The repositories impletented are `FileRepository` and `MemoryRepository`, and also has a placeholder for a `DBRepository`.
- The `MemoryRepository` doesn't persists the data between runs.
- The `FileRepository` persists the data in a JSON file by default called `data.json`.
- It was designed at first to work with memory just to test the tests.

## What you need to know about the solution?

- The repositories has a base class called Repository that has the methods that the repositories should implement. The class itself is an abstract class, and all the methods are abstract methods.
- - The methods are: `get`, `get_all`, `reload`, `save`, `update`, `delete`.
- The models has a base class called Base which is an abstract class, it contains three types of methods:
- - @abstractmethods - methods that the class that inherits from Base should implement. The methods are: `to_dict`
- - @classmethods - This methods are: `get`, `get_all`, `delete`. The logic for these methods is the same for all the models, so it was implemented in the Base class.
- - @staticabstractmethods - methods that the class that inherits from Base should implement, but are static methods. The methods are: `create`, `update`.

> [!TIP]
> You can preload the persistence layer selected via the `reload` method in the `Repository` class.
> This method is called in the `__init__` method of the `Repository` class.

---

> [!IMPORTANT]
> The tests won't pass if there isn't a dummy country created, for example `MemoryRepository` on the reload function creates a dummy `UY` country via the `reload` method which also calls the `populate_db` function in the `utils/populate.py` file.

## MVC

The solution is divided into four main parts: `Models`, `Controllers`, and `Persistence`, but not uses Views because it is just a REST API.

- In the `controllers` package you will find the logic for the API endpoints.
- In the `models` package you will find the classes that represent the data.
- In the `routes` package you will find the routes for the API, which are routes that call the controllers.
- In the `persistence` package you will find the repositories that handle the data.

## How the solution works?

The application is built using the factory pattern. The `create_app` function in the `src/__init__.py` file creates the application and returns it. The function accepts a `config` object which is used to configure the application. It registers the routes, the error handlers, cors, and then returns the application.

To run the application you can simply run the app object returned by the `create_app` function just like the `hbnb.py` file does. Or you can run the `manage.py` file, which uses the `Flask CLI`, with `python manage.py run` to run the application.

The routes are divided into `Blueprints` and are registered in the `create_app` function mentioned above. The routes are located in the `src/routes` directory.

The routes defined in the files use the controllers to handle the requests. The controllers are in the `src/controllers` directory.

Then the controllers queries the models to retrieve or save the data. The models are in the `src/models` directory.

And the models use the current selected repository to handle the data. The repositories are in the `src/persistence` directory. The `src/persistence/__init__.py` exports a `db` object that is the current selected repository.

So, the flow is like this:

```text
Request -> Route -> Controller -> Model -> Repository
(then all the way back)
Response <- Route <- Controller <- Model <- Repository
```

You can choose the repository you want to use by setting the `REPOSITORY_TYPE` environment variable to `memory`, `file`, or `db`. The default is `memory`.

---
Just to mention, there is a `utils` package that for now contains only two files, `constants.py` and `populate.py`. The `constants.py` file contains the constants used in the application, and the `populate.py` file contains the logic to populate the database with some data.

You can change the constants arbitrarily.

## How to run

To run the solution first install the requirements with `pip install -r requirements.txt`. Then there is a few ways to run it:

- Run the `manage.py` file with the command `python manage.py run` and specify flags like `--port {port} --host {host}` if you want to run it in a different port or host.
- Run the `hbnb.py`. This file calls a function before running the app that will populate the database with some data.
- Build and run the Dockerfile.
 
---

# HBnB Evolution: Part 2 (Database Persistence)

## Integrating SQLAlchemy

This task involves integrating SQLAlchemy into your HBnB Evolution project, enabling a transition from your current data management system to a robust database-backed system using an ORM (Object-Relational Mapper). Given the flexibility suggested by the DataManager pattern used earlier, this task will build upon that architecture to incorporate SQLAlchemy effectively.

### Objectives

- Integrate SQLAlchemy ORM into the Flask application, leveraging the existing DataManager structure.
- Adapt current data models to work as SQLAlchemy ORM classes while maintaining compatibility with the DataManager interface.
- Ensure the application can dynamically switch between the existing file-based system and the new database-backed system based on configuration.

### Requirements

- SQLAlchemy Integration: Incorporate SQLAlchemy to manage database interactions.
- Model Adaptation: Convert existing models to use SQLAlchemy’s ORM features, including the newly added fields (password and is_admin) needed for authentication and authorization.
- Flexible Persistence Switching: Enable seamless switching between file-based and database persistence modes using environment configuration.

### Instructions

1. **Update Project Dependencies:**
    - Ensure SQLAlchemy and Flask-SQLAlchemy are included in your project dependencies. Add these to your `requirements.txt` to manage installations efficiently.

2. **Initialize SQLAlchemy in Your Flask Application:**
    - Configure your Flask app to use SQLAlchemy, initially connecting to a SQLite database for development purposes.
    - Example configuration:

    ```python
    from flask_sqlalchemy import SQLAlchemy

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///development.db'
    db = SQLAlchemy(app)
    ```

3. **Refactor Existing Models to Extend SQLAlchemy:**
    - Modify your data models to extend from `db.Model`, SQLAlchemy’s declarative base, ensuring they implement the methods defined by your DataManager interface.
    - Define attributes using SQLAlchemy’s column types and relationships.
    - Example for a User model:

    ```python
    class User(db.Model):
        id = db.Column(db.String(36), primary_key=True)
        email = db.Column(db.String(120), unique=True, nullable=False)
        password = db.Column(db.String(128), nullable=False)  # Ensure secure storage
        is_admin = db.Column(db.Boolean, default=False)
        created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
        updated_at = db.Column(db.DateTime, onupdate=db.func.current_timestamp())
    ```

4. **Enhance DataManager to Handle Both Persistence Types:**
    - Adjust the DataManager to manage both file-based and database interactions, possibly using an environment variable to switch between the modes.
    - Implement conditional logic within the DataManager methods to direct queries to the appropriate storage type based on the configuration.
    - Example of conditional persistence logic:

    ```python
    class DataManager:
        def save_user(self, user):
            if app.config['USE_DATABASE']:
                db.session.add(user)
                db.session.commit()
            else:
                # Implement file-based save logic
                pass
    ```

5. **Testing and Validation:**
    - Develop comprehensive tests to ensure that both the database interactions via SQLAlchemy and the fallback to file-based operations function as expected.
    - Test CRUD operations, relationship management, and the dynamic switching mechanism to verify full system integrity.

### Configurable Database Selection

#### Objectives

1. **Develop a dynamic database configuration system that allows switching between SQLite and PostgreSQL based on environment settings.**
2. **Ensure the application initializes the correct database type at startup and connects successfully.**
3. **Implement functionality to support easy transition and configuration for different deployment scenarios.**

#### Requirements

- Flexible Database Configuration: Implement a system that uses environment variables or configuration files to select the appropriate database at startup.
- Database Initialization: Ensure that the SQLite database is automatically created if it does not exist when the application is run in development mode.
- Connection Details for Production Database: Set up and test connection parameters for a PostgreSQL database when in production mode.

#### Instructions

1. **Environment Setup:**
    - Define environment variables that specify the database type (SQLite for development and PostgreSQL for production).
    - These variables should be easily configurable, e.g., through a `.env` file or a configuration module within the application.
    - Example environment variables:

    ```bash
    DATABASE_TYPE=sqlite  # Options: 'sqlite', 'postgresql'
    DATABASE_URL=sqlite:///dev.db  # URL for SQLite or connection string for PostgreSQL
    ```

2. **Database Configuration in Application:**
    - Modify the application configuration to dynamically set the database connection based on the environment variables.
    - Use a configuration class or a similar approach to manage different settings for development, testing, and production environments.
    - Example configuration setup in Flask:

    ```python
    import os
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy

    class Config:
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

    class DevelopmentConfig(Config):
        DEBUG = True

    class ProductionConfig(Config):
        DEBUG = False

    app = Flask(__name__)
    env = os.environ.get('ENV', 'development')
    if env == 'development':
        app.config.from_object(DevelopmentConfig)
    else:
        app.config.from_object(ProductionConfig)

    db = SQLAlchemy(app)
    ```

3. **Database Initialization for Development:**
    - Implement logic to check if the SQLite database exists and create it if it does not.
    - This step is crucial to ensure a smooth development experience.
    - Ensure that SQLAlchemy is configured to handle this initialization automatically where possible, or write scripts to set up the database initially.

4. **Testing Connection and Transitions:**
    - Write tests to verify that the application correctly determines which database to connect to based on the environment settings.
    - Test the application’s ability to connect to both SQLite and PostgreSQL databases and perform basic CRUD operations to validate the connections.
    - Ensure that switching from one database type to another does not require changes in the business logic of the application.

---

## Implementing Authentication with JWT

### Objectives

1. **Implement JWT-based authentication to secure API endpoints.**
2. **Create a login endpoint to validate user credentials and issue JWTs.**
3. **Update the User model to include password storage using best practices for security and a boolean flag to denote administrative status.**
4. **Ensure only authenticated users can access protected endpoints, with additional checks for administrative privileges where necessary.**

### Instructions

1. **Set Up JWT Authentication:**
    - Install Flask-JWT-Extended and add it to your project dependencies.
    - Configure JWT in your Flask application, setting up secret keys and any relevant JWT properties.
    - Example configuration:

    ```python
    from flask import Flask
    from flask_jwt_extended import JWTManager

    app = Flask(__name__)
    app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
    jwt = JWTManager(app)
    ```

2. **Create a Login Endpoint:**
    - Develop a login endpoint that authenticates users based on their email and password.
    - Upon successful authentication, issue a JWT that will be used to access protected endpoints.
    - Example login endpoint:

    ```python
    from flask import request, jsonify
    from flask_jwt_extended import create_access_token

    @app.route('/login', methods=['POST'])
    def login():
        username = request.json.get('username', None)
        password = request.json.get('password', None)
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            access_token = create_access_token(identity=username)
            return jsonify(access_token=access_token), 200
        return 'Wrong username or password', 401
    ```

3. **Modify User Model for Authentication:**
    - Update the User model to include a password field and an is_admin field.
    - Use bcrypt to hash passwords before storing them in the database.
    - Example User model update:

    ```python
    from flask_bcrypt import Bcrypt

    bcrypt = Bcrypt(app)

    class User(db.Model):
        # existing fields...
        password_hash = db.Column(db.String(128))
        is_admin = db.Column(db.Boolean, default=False)

        def set_password(self, password):
            self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

        def check_password(self, password):
            return bcrypt.check_password_hash(self.password_hash, password)
    ```

4. **Secure API Endpoints:**
    - Update API endpoints to require a valid JWT for access.
    - Use Flask-JWT-Extended decorators to handle these requirements.
    - Implement additional checks for endpoints that require administrative privileges.
    - Example of securing an endpoint:

    ```python
    from flask_jwt_extended import jwt_required, get_jwt_identity

    @app.route('/protected', methods=['GET'])
    @jwt_required()
    def protected():
        current_user = get_jwt_identity()
        return jsonify(logged_in_as=current_user), 200
    ```

5. **Testing and Validation:**
    - Develop tests to ensure that the login process works correctly and that JWTs are issued as expected.
    - Test protected endpoints to verify that they correctly authenticate access based on the provided JWT.
    - Ensure that administrative endpoints are only accessible to users with the appropriate privileges.

---

## Database Schema Design and Migration

### Objectives

1. **Create a detailed database schema diagram reflecting the relationships and structures decided in the UML design phase.**
2. **Write SQL scripts to create the database, tables, and initial data.**
3. **Optionally, implement database migration scripts using Alembic to manage changes to the database structure over time.**
4. **Ensure the application can handle schema changes without data loss and with minimal downtime.**

### Instructions

1. **Designing the Database Schema:**
    - Translate the UML class diagrams into a relational database schema. This includes defining tables for each entity, their relationships, and ensuring that any necessary constraints and indexes are included.
    - Use SQLAlchemy to define your models and their relationships.
    - Example of defining a relationship:

    ```python
    class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(80), unique=True, nullable=False)
        email = db.Column(db.String(120), unique=True, nullable=False)

        # Define a relationship
        posts = db.relationship('Post', backref='author', lazy=True)
    ```

2. **Writing SQL Scripts:**
    - Create SQL scripts to set up the database and insert initial data.
    - Example SQL script:

    ```sql
    CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(80) NOT NULL UNIQUE,
        email VARCHAR(120) NOT NULL UNIQUE,
        password_hash VARCHAR(128) NOT NULL,
        is

