from datetime import datetime

from weather_forecasts_databse import db


class WeatherForecast(db.Model):
    __table__name = 'weatherforecast'

    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(64))
    date = db.Column(db.Date)
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Integer)
    description = db.Column(db.Text)
    active = db.Column(db.Boolean, default=True)

    def __init__(self, city='', date='1000-01-01', temperature=0, humidity=0, description=''):
        self.city = city
        self.date = datetime.strptime(date, '%Y-%m-%d').date()
        self.temperature = temperature
        self.humidity = humidity
        self.description = description

    def to_dict(self):
        return {key: str(self.__dict__[key]) for key in self.__dict__.keys() if '_state' not in key}
