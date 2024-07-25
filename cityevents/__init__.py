import os

from flask_restful import Api

from city_events_database import db

from flask import Flask

from city_events_api import CityEvents

HOST = os.environ.get('HOST', 'localhost')
PORT = os.environ.get('PORT', 5000)
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_USER = os.environ.get('DB_USER', 'myuser')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'mypassword')
DB_NAME = os.environ.get('DB_NAME', 'cityevents')

db_url = f'mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'


def create_app():
    app = Flask('cityevents')
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    db.init_app(app)
    api = Api(app)
    api.add_resource(CityEvents, '/cityevents')
    with app.app_context():
        db.create_all()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host=HOST, port=PORT, debug=True)
