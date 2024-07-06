""" Another way to run the app"""

from src import create_app
import os

app = create_app('src.config.ProductionConfig' if os.environ.get('ENV') == 'prod'
                 else 'src.config.DevelopmentConfig')

if __name__ == "__main__":
    app.run()
