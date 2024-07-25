from flask import request, jsonify
from flask_restful import Resource
from city_event import CityEvent

from city_events_database import db


class CityEvents(Resource):
    def get(self):
        city = request.args.get('city')
        events = db.session.query(CityEvent).filter(CityEvent.active)
        events = events.filter(CityEvent.city.like(city)).all()

        if not events:
            return 'No events we\'re found', 404

        response = jsonify([e.to_dict() for e in events])
        response.status_code = 200

        return response

    def post(self):
        payload = request.args
        event = CityEvent(**payload)

        db.session.add(event)
        db.session.commit()

        response = jsonify(event.to_dict())
        response.status_code = 201

        return response

    def put(self):
        event_id = int(request.args.get('id'))
        events = db.session.query(CityEvent).filter(CityEvent.active)
        event = events.filter(CityEvent.id == event_id).first()

        if not event:
            return 'No event was found', 404

        any(setattr(event, key, request.args.get(key)) for key in request.args if getattr(event, key))

        db.session.commit()

        response = jsonify(event.to_dict())
        response.status_code = 200

        return response

    def delete(self):
        event_id = int(request.args.get('id'))
        events = db.session.query(CityEvent).filter(CityEvent.active)
        event = events.filter(CityEvent.id == event_id).first()

        if not event:
            return 'No event was found', 404

        event.active = False
        db.session.commit()

        return 'OK', 200
