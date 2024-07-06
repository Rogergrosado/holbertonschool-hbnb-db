import unittest
from flask import current_app
from src import create_app, db
from src.config import TestingConfig
from src.models.user import User

class TestDatabaseConnections(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config_class=TestingConfig)
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.init_app(self.app)
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_sqlite_connection(self):
        with self.app.app_context():
            self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
            db.create_all()
            self.assertIn('sqlite', current_app.config['SQLALCHEMY_DATABASE_URI'])

            user = User(
                email='test@example.com',
                first_name='Test',
                last_name='User',
                password='testpassword',
                is_admin=False
            )
            db.session.add(user)
            db.session.commit()

            retrieved_user = User.query.filter_by(email='test@example.com').first()
            self.assertIsNotNone(retrieved_user)
            self.assertEqual(retrieved_user.email, 'test@example.com')
            self.assertEqual(retrieved_user.first_name, 'Test')
            self.assertEqual(retrieved_user.last_name, 'User')

    def test_postgresql_connection(self):
        with self.app.app_context():
            self.app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost/hbnb_test'
            db.create_all()
            self.assertIn('postgresql', current_app.config['SQLALCHEMY_DATABASE_URI'])

            user = User(
                email='test@example.com',
                first_name='Test',
                last_name='User',
                password='testpassword',
                is_admin=False
            )
            db.session.add(user)
            db.session.commit()

            retrieved_user = User.query.filter_by(email='test@example.com').first()
            self.assertIsNotNone(retrieved_user)
            self.assertEqual(retrieved_user.email, 'test@example.com')
            self.assertEqual(retrieved_user.first_name, 'Test')
            self.assertEqual(retrieved_user.last_name, 'User')

if __name__ == '__main__':
    unittest.main()
