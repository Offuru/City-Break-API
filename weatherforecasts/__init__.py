import os

from flask_restful import Api

from weather_forecasts_databse import db

from flask import Flask

from weather_forecasts_api import WeatherForecasts

HOST = os.environ.get('HOST', 'localhost')
PORT = os.environ.get('PORT', 5000)
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_USER = os.environ.get('DB_USER', 'myuser')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'mypassword')
DB_NAME = os.environ.get('DB_NAME', 'weatherforecasts')

db_url = f'mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'


def create_app():
    app = Flask('weatherforecasts')
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    db.init_app(app)
    api = Api(app)
    api.add_resource(WeatherForecasts, '/weatherforecasts')
    with app.app_context():
        db.create_all()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host=HOST, port=PORT, debug=True)
