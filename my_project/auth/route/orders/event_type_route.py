from http import HTTPStatus
from flask import Blueprint, jsonify, Response, request, make_response
from my_project.auth.controller import event_type_controller
from my_project.auth.domain import EventType

event_type_bp = Blueprint('event_types', __name__, url_prefix='/event-types')


@event_type_bp.get('')
def get_all_event_types() -> Response:
    """
    Gets all event types from the database.
    ---
    tags:
      - EventType
    responses:
      200:
        description: List of all event types
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
                properties:
                  id: {type: integer}
                  name: {type: string}
                  description: {type: string}
    """
    event_types = event_type_controller.find_all()
    event_types_dto = [et.put_into_dto() for et in event_types]
    return make_response(jsonify(event_types_dto), HTTPStatus.OK)


@event_type_bp.post('')
def create_event_type() -> Response:
    """
    Creates a new event type in the database.
    ---
    tags:
      - EventType
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            name: {type: string}
            description: {type: string}
          required: [name]
    responses:
      201:
        description: Event type created
        content:
          application/json:
            schema:
              type: object
              properties:
                id: {type: integer}
                name: {type: string}
                description: {type: string}
    """
    if not request.is_json:
        return make_response(jsonify({"error": "Content-Type must be application/json"}), 415)
    content = request.get_json()
    event_type = EventType.create_from_dto(content)
    event_type_controller.create(event_type)
    return make_response(jsonify(event_type.put_into_dto()), HTTPStatus.CREATED)


@event_type_bp.get('/<int:event_type_id>')
def get_event_type(event_type_id: int) -> Response:
    """
    Gets event type by ID.
    ---
    tags:
      - EventType
    parameters:
      - in: path
        name: event_type_id
        schema:
          type: integer
        required: true
        description: ID of the event type
    responses:
      200:
        description: Event type found
        content:
          application/json:
            schema:
              type: object
      404:
        description: Event type not found
    """
    event_type = event_type_controller.find_by_id(event_type_id)
    if event_type:
        return make_response(jsonify(event_type.put_into_dto()), HTTPStatus.OK)
    return make_response(jsonify({"error": "Event type not found"}), HTTPStatus.NOT_FOUND)


@event_type_bp.put('/<int:event_type_id>')
def update_event_type(event_type_id: int) -> Response:
    """
    Updates event type by ID.
    ---
    tags:
      - EventType
    consumes:
      - application/json
    parameters:
      - in: path
        name: event_type_id
        schema:
          type: integer
        required: true
        description: ID of the event type
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            name: {type: string}
            description: {type: string}
    responses:
      200:
        description: Event type updated
      404:
        description: Event type not found
    """
    if not request.is_json:
        return make_response(jsonify({"error": "Content-Type must be application/json"}), 415)
    content = request.get_json()
    event_type = EventType.create_from_dto(content)
    event_type_controller.update(event_type_id, event_type)
    return make_response("Event Type updated", HTTPStatus.OK)


@event_type_bp.delete('/<int:event_type_id>')
def delete_event_type(event_type_id: int) -> Response:
    """
    Deletes event type by ID.
    ---
    tags:
      - EventType
    parameters:
      - in: path
        name: event_type_id
        schema:
          type: integer
        required: true
        description: ID of the event type
    responses:
      204:
        description: Event type deleted
      404:
        description: Event type not found
    """
    event_type_controller.delete(event_type_id)
    return make_response("Event Type deleted", HTTPStatus.NO_CONTENT)


@event_type_bp.get('/find-by-name/<string:name>')
def find_event_type_by_name(name: str) -> Response:
    """
    Gets event type(s) by name.
    ---
    tags:
      - EventType
    parameters:
      - in: path
        name: name
        schema:
          type: string
        required: true
        description: Name of the event type
    responses:
      200:
        description: List of event types with given name
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
    """
    event_types = event_type_controller.find_by_name(name)
    return make_response(jsonify([et.put_into_dto() for et in event_types]), HTTPStatus.OK)


@event_type_bp.get('/find-by-email/<string:email>')
def find_event_type_by_email(email: str) -> Response:
    """
    Gets event type(s) by email.
    ---
    tags:
      - EventType
    parameters:
      - in: path
        name: email
        schema:
          type: string
        required: true
        description: Email associated with the event type
    responses:
      200:
        description: List of event types with given email
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
    """
    event_types = event_type_controller.find_by_email(email)
    return make_response(jsonify([et.put_into_dto() for et in event_types]), HTTPStatus.OK)
