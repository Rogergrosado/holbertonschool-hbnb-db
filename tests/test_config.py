import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from src.config import Config, DevelopmentConfig, ProductionConfig, TestingConfig

class TestConfig(unittest.TestCase):

    def test_config_default(self):
        app = Flask(__name__)
        app.config.from_object(Config)

        self.assertFalse(app.config['DEBUG'])
        self.assertFalse(app.config['TESTING'])
        self.assertFalse(app.config['SQLALCHEMY_TRACK_MODIFICATIONS'])
        self.assertEqual(app.config['SECRET_KEY'], 'hohohoitsasecret')
        self.assertEqual(app.config['JWT_SECRET_KEY'], 'hohohoitsasecret')
        self.assertEqual(app.config['JWT_ACCESS_TOKEN_EXPIRES'], 3600)
        self.assertEqual(app.config['SQLALCHEMY_DATABASE_URI'], 'sqlite:///hbnb.db')

    def test_config_development(self):
        app = Flask(__name__)
        app.config.from_object(DevelopmentConfig)

        self.assertTrue(app.config['DEBUG'])
        self.assertFalse(app.config['TESTING'])
        self.assertFalse(app.config['SQLALCHEMY_TRACK_MODIFICATIONS'])
        self.assertEqual(app.config['SECRET_KEY'], 'hohohoitsasecret')
        self.assertEqual(app.config['JWT_SECRET_KEY'], 'hohohoitsasecret')
        self.assertEqual(app.config['JWT_ACCESS_TOKEN_EXPIRES'], 3600)
        self.assertEqual(app.config['SQLALCHEMY_DATABASE_URI'], 'sqlite:///development.db')

    def test_config_production(self):
        app = Flask(__name__)
        app.config.from_object(ProductionConfig)

        self.assertFalse(app.config['DEBUG'])
        self.assertFalse(app.config['TESTING'])
        self.assertFalse(app.config['SQLALCHEMY_TRACK_MODIFICATIONS'])
        self.assertEqual(app.config['SECRET_KEY'], 'hohohoitsasecret')
        self.assertEqual(app.config['JWT_SECRET_KEY'], 'hohohoitsasecret')
        self.assertEqual(app.config['JWT_ACCESS_TOKEN_EXPIRES'], 3600)
        self.assertEqual(app.config['SQLALCHEMY_DATABASE_URI'], 'postgresql://user:password@localhost/hbnb_prod')

    def test_config_testing(self):
        app = Flask(__name__)
        app.config.from_object(TestingConfig)

        self.assertFalse(app.config['DEBUG'])
        self.assertTrue(app.config['TESTING'])
        self.assertFalse(app.config['SQLALCHEMY_TRACK_MODIFICATIONS'])
        self.assertEqual(app.config['SECRET_KEY'], 'hohohoitsasecret')
        self.assertEqual(app.config['JWT_SECRET_KEY'], 'hohohoitsasecret')
        self.assertEqual(app.config['JWT_ACCESS_TOKEN_EXPIRES'], 3600)
        self.assertEqual(app.config['SQLALCHEMY_DATABASE_URI'], 'sqlite:///:memory:')

if __name__ == '__main__':
    unittest.main()
