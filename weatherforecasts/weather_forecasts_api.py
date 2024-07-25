from flask import request, jsonify
from flask_restful import Resource
from sqlalchemy import and_
import copy

from weather_forecast import WeatherForecast

from weather_forecasts_databse import db


class WeatherForecasts(Resource):
    def get(self):
        city = request.args.get('city')
        date = request.args.get('date')

        if not (city or date):
            return 'Invalid arguments', 400

        forecasts = db.session.query(WeatherForecast).filter(WeatherForecast.active)

        if city:
            forecasts = forecasts.filter_by(city=city)

        if date:
            forecasts = forecasts.filter_by(date=date)

        forecasts = forecasts.all()

        if not forecasts:
            return 'No weather forecasts for that city were found', 404

        response = jsonify([f.to_dict() for f in forecasts])
        response.status_code = 200

        return response

    def post(self):

        payload = request.form
        forecast = WeatherForecast()

        if not all(key in forecast.to_dict().keys() for key in payload.keys()):
            return 'Invalid arguments', 400

        forecast = WeatherForecast(**payload)
        response_copy = copy.deepcopy(forecast)

        db.session.add(forecast)
        db.session.commit()

        response = jsonify(response_copy.to_dict())
        response.status_code = 201

        return response

    def delete(self):
        forecast_id = request.args['id']

        if not forecast_id:
            return 'Invalid arguments', 400

        forecast_id = int(forecast_id)

        forecast = db.session.query(WeatherForecast).filter(
            and_(WeatherForecast.id == forecast_id, WeatherForecast.active)).first()

        if not forecast:
            return 'Weather forecast was not found', 404

        forecast.active = False
        db.session.commit()

        return 'OK', 201

    def put(self):
        forecast_id = request.args['id']

        if not forecast_id:
            return 'Invalid arguments', 400

        forecast_id = int(forecast_id)

        forecast = db.session.query(WeatherForecast).filter(WeatherForecast.active)
        forecast = forecast.filter(WeatherForecast.id == forecast_id).first()

        if not forecast:
            return 'Weather forecast was not found', 404

        any(setattr(forecast, key, request.form.get(key)) for key in request.form if getattr(forecast, key))

        response_copy = copy.deepcopy(forecast)

        db.session.commit()

        response = jsonify(response_copy.to_dict())
        response.status_code = 201

        return response
