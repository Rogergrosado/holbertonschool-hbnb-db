import unittest
from flask import json
from src import create_app, db
from src.models.user import User
from src.config import TestingConfig

class TestAuth(unittest.TestCase):
    def setUp(self):
        print("Setting up test...")
        self.app = create_app(TestingConfig)
        print("App created")
        self.app.config['DEBUG'] = True
        print("Debug mode enabled")
        self.client = self.app.test_client()
        print("Test client created")
        self.app_context = self.app.app_context()
        self.app_context.push()
        print("App context pushed")
        
        with self.app.app_context():
            db.create_all()
            print("Database tables created")

            # Create test users
            self.normal_user = User(
                email='user@test.com',
                first_name='John',
                last_name='Doe',
                password='password',
                is_admin=False
            )
            self.admin_user = User(
                email='admin@test.com',
                first_name='Admin',
                last_name='User',
                password='adminpass',
                is_admin=True
            )
            
            db.session.add(self.normal_user)
            db.session.add(self.admin_user)
            db.session.commit()
            print("Test users created")

        print("Registered routes:")
        for rule in self.app.url_map.iter_rules():
            print(f"{rule.endpoint}: {rule.rule}")

    def tearDown(self):
        print("Tearing down test...")
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def login(self, email, password):
        print(f"Attempting login with email: {email}")
        response = self.client.post('/users/login', json={
            'email': email,
            'password': password
        })
        print(f"Login response status: {response.status_code}")
        print(f"Login response data: {response.data}")
        return response

    def test_login_success(self):
        response = self.login('user@test.com', 'password')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIn('access_token', data)

    def test_login_failure(self):
        response = self.login('user@test.com', 'wrongpassword')
        self.assertEqual(response.status_code, 401)  # Adjusted to expected behavior

    def test_protected_endpoint(self):
        login_response = self.login('user@test.com', 'password')
        self.assertEqual(login_response.status_code, 200)  # Ensure login is successful
        token = json.loads(login_response.data.decode('utf-8'))['access_token']

        response = self.client.get('/users/protected', headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 200)

    def test_protected_endpoint_no_token(self):
        response = self.client.get('/users/protected')
        self.assertEqual(response.status_code, 401)  # Adjust to expected behavior

    def test_admin_endpoint_as_admin(self):
        login_response = self.login('admin@test.com', 'adminpass')
        self.assertEqual(login_response.status_code, 200)
        token = json.loads(login_response.data.decode('utf-8')).get('access_token')
        self.assertIsNotNone(token, "Access token should not be None")

        # Use the token to access the admin endpoint
        headers = {'Authorization': f'Bearer {token}'}
        response = self.client.get('/users/admin/endpoint', headers=headers)
        
        print(response.data.decode('utf-8'))
        print(f"Admin endpoint response status: {response.status_code}")
        self.assertEqual(response.status_code, 200)
            
        self.assertEqual(response.status_code, 200)
        
    def test_admin_endpoint_as_normal_user(self):
        login_response = self.login('user@test.com', 'password')
        self.assertEqual(login_response.status_code, 200)  # Ensure login is successful
        token = json.loads(login_response.data.decode('utf-8'))['access_token']

        response = self.client.get('/users/admin', headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 403)  # Adjust to expected behavior

if __name__ == '__main__':
    unittest.main()
