from flask import request, jsonify
from flask_restful import Resource
from city_event import CityEvent
import copy

from city_events_database import db


class CityEvents(Resource):
    def get(self):
        city = request.args.get('city')

        if not city:
            return 'Invalid arguments', 400

        events = db.session.query(CityEvent).filter(CityEvent.active)
        events = events.filter(CityEvent.city.like(city)).all()

        if not events:
            return 'No events we\'re found', 404

        response = jsonify([e.to_dict() for e in events])
        response.status_code = 200

        return response

    def post(self):
        payload = request.form
        event = CityEvent()

        if not all(key in event.to_dict().keys() for key in payload.keys()):
            return 'Invalid arguments', 400

        event = CityEvent(**payload)
        response_copy = CityEvent(**payload)

        db.session.add(event)
        db.session.commit()

        response = jsonify(response_copy.to_dict())
        response.status_code = 201

        return response

    def put(self):
        event_id = request.args.get('id')

        if not event_id:
            return 'Invalid arguments', 400

        event_id = int(event_id)

        events = db.session.query(CityEvent).filter(CityEvent.active)
        event = events.filter(CityEvent.id == event_id).first()

        if not event:
            return 'No event was found', 404

        any(setattr(event, key, request.form.get(key)) for key in request.form if getattr(event, key))

        response_copy = copy.deepcopy(event)

        db.session.commit()

        response = jsonify(response_copy.to_dict())
        response.status_code = 200

        return response

    def delete(self):
        event_id = request.args.get('id')

        if not event_id:
            return 'Invalid arguments', 400

        event_id = int(event_id)

        events = db.session.query(CityEvent).filter(CityEvent.active)
        event = events.filter(CityEvent.id == event_id).first()

        if not event:
            return 'No event was found', 404

        event.active = False
        db.session.commit()

        return 'OK', 200
