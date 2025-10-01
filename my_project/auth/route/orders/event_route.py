from http import HTTPStatus
from flask import Blueprint, jsonify, Response, request, make_response
from my_project.auth.controller import event_controller
from my_project.auth.domain.orders.event import Event
from datetime import datetime

event_bp = Blueprint('event', __name__, url_prefix='/event')


@event_bp.get('')
def get_all_events() -> Response:
    """
    Gets all events from the database.
    ---
    tags:
      - Event
    responses:
      200:
        description: List of all events
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
                properties:
                  id: {type: integer}
                  event_date: {type: string, format: date}
                  event_duration: {type: integer}
                  address: {type: string}
                  total_cost: {type: number}
                  event_type_id: {type: integer}
    """
    events = event_controller.find_all()
    event_dto = [event.put_into_dto() for event in events]
    return make_response(jsonify(event_dto), HTTPStatus.OK)


@event_bp.post('')
def create_event() -> Response:
    """
    Creates a new event in the database.
    ---
    tags:
      - Event
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            event_date: {type: string, format: date}
            event_duration: {type: integer}
            address: {type: string}
            total_cost: {type: number}
            event_type_id: {type: integer}
          required: [event_date, event_duration, address, total_cost, event_type_id]
    responses:
      201:
        description: Event created
        content:
          application/json:
            schema:
              type: object
              properties:
                id: {type: integer}
                event_date: {type: string, format: date}
                event_duration: {type: integer}
                address: {type: string}
                total_cost: {type: number}
                event_type_id: {type: integer}
    """
    content = request.get_json()
    if 'event_date' in content:
        content['event_date'] = datetime.fromisoformat(content['event_date']).date()
    event = Event.create_from_dto(content)
    event_controller.create(event)
    return make_response(jsonify(event.put_into_dto()), HTTPStatus.CREATED)


@event_bp.get('/<int:event_id>')
def get_event(event_id: int) -> Response:
    """
    Gets event by ID.
    ---
    tags:
      - Event
    parameters:
      - in: path
        name: event_id
        schema:
          type: integer
        required: true
        description: ID of the event
    responses:
      200:
        description: Event found
        content:
          application/json:
            schema:
              type: object
      404:
        description: Event not found
    """
    event = event_controller.find_by_id(event_id)
    if event:
        return make_response(jsonify(event.put_into_dto()), HTTPStatus.OK)
    return make_response(jsonify({"error": "Event not found"}), HTTPStatus.NOT_FOUND)


@event_bp.put('/<int:event_id>')
def update_event(event_id: int) -> Response:
    """
    Updates event by ID.
    ---
    tags:
      - Event
    consumes:
      - application/json
    parameters:
      - in: path
        name: event_id
        schema:
          type: integer
        required: true
        description: ID of the event
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            event_date: {type: string, format: date}
            event_duration: {type: integer}
            address: {type: string}
            total_cost: {type: number}
            event_type_id: {type: integer}
    responses:
      200:
        description: Event updated
      404:
        description: Event not found
    """
    content = request.get_json()
    if 'event_date' in content:
        content['event_date'] = datetime.fromisoformat(content['event_date']).date()
    event = Event.create_from_dto(content)
    event_controller.update(event_id, event)
    return make_response("Event updated", HTTPStatus.OK)


@event_bp.delete('/<int:event_id>')
def delete_event(event_id: int) -> Response:
    """
    Deletes event by ID.
    ---
    tags:
      - Event
    parameters:
      - in: path
        name: event_id
        schema:
          type: integer
        required: true
        description: ID of the event
    responses:
      204:
        description: Event deleted
      404:
        description: Event not found
    """
    event_controller.delete(event_id)
    return make_response("Event deleted", HTTPStatus.NO_CONTENT)
