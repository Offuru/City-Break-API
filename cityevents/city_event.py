from datetime import datetime

from city_events_database import db


class CityEvent(db.Model):
    __tablename__ = 'cityevents'

    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(64))
    date = db.Column(db.Date)
    location = db.Column(db.String(128))
    description = db.Column(db.Text)
    price = db.Column(db.Float)
    active = db.Column(db.Boolean, default=True)

    def __init__(self, city, date, location, description, price):
        self.city = city
        self.date = datetime.strptime(date, '%Y-%m-%d').date()
        self.location = location
        self.description = description
        self.price = float(price)

    def to_dict(self):
        return {key: str(self.__dict__[key]) for key in self.__dict__.keys() if '_state' not in key}
