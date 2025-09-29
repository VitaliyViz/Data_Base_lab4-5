from http import HTTPStatus
from flask import Blueprint, jsonify, Response, request, make_response
from my_project.auth.controller import animator_controller
from my_project.auth.domain.orders.animator import Animator

animator_bp = Blueprint('animator', __name__, url_prefix='/animator')


@animator_bp.get('')
def get_all_animators() -> Response:
    """
    Gets all animators from the database.
    ---
    tags:
      - Animator
    responses:
      200:
        description: List of all animators
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
                properties:
                  id: {type: integer}
                  name: {type: string}
                  last_name: {type: string}
                  phone: {type: string}
                  email: {type: string}
                  gender: {type: string}
                  birth_date: {type: string}
                  experience_years: {type: integer}
    """
    animators = animator_controller.find_all()
    animator_dto = [animator.put_into_dto() for animator in animators]
    return make_response(jsonify(animator_dto), HTTPStatus.OK)


@animator_bp.post('')
def create_animator() -> Response:
    """
    Creates a new animator in the database.
    ---
    tags:
      - Animator
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
            last_name: {type: string}
            phone: {type: string}
            email: {type: string}
            gender: {type: string}
            birth_date: {type: string, format: date}
            experience_years: {type: integer}
          required: [name, last_name, phone, email]
    responses:
      201:
        description: Animator created
        content:
          application/json:
            schema:
              type: object
              properties:
                id: {type: integer}
                name: {type: string}
                last_name: {type: string}
                phone: {type: string}
                email: {type: string}
                gender: {type: string}
                birth_date: {type: string}
                experience_years: {type: integer}
    """
    if not request.is_json:
        return make_response(jsonify({"error": "Content-Type must be application/json"}), 415)
    content = request.get_json()
    animator = Animator.create_from_dto(content)
    animator_controller.create_animator(animator)
    return make_response(jsonify(animator.put_into_dto()), HTTPStatus.CREATED)


@animator_bp.get('/<int:animator_id>')
def get_animator(animator_id: int) -> Response:
    """
    Gets animator by ID.
    ---
    tags:
      - Animator
    parameters:
      - in: path
        name: animator_id
        schema:
          type: integer
        required: true
        description: ID of the animator
    responses:
      200:
        description: Animator found
        content:
          application/json:
            schema:
              type: object
      404:
        description: Animator not found
    """
    animator = animator_controller.find_by_id(animator_id)
    if animator:
        return make_response(jsonify(animator.put_into_dto()), HTTPStatus.OK)
    return make_response(jsonify({"error": "Animator not found"}), HTTPStatus.NOT_FOUND)


@animator_bp.put('/<int:animator_id>')
def update_animator(animator_id: int) -> Response:
    """
    Updates animator by ID.
    ---
    tags:
      - Animator
    consumes:
      - application/json
    parameters:
      - in: path
        name: animator_id
        schema:
          type: integer
        required: true
        description: ID of the animator
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            name: {type: string}
            last_name: {type: string}
            phone: {type: string}
            email: {type: string}
            gender: {type: string}
            birth_date: {type: string, format: date}
            experience_years: {type: integer}
    responses:
      200:
        description: Animator updated
      404:
        description: Animator not found
    """
    if not request.is_json:
        return make_response(jsonify({"error": "Content-Type must be application/json"}), 415)
    content = request.get_json()
    animator = Animator.create_from_dto(content)
    animator_controller.update_animator(animator_id, animator)
    return make_response("Animator updated", HTTPStatus.OK)


@animator_bp.delete('/<int:animator_id>')
def delete_animator(animator_id: int) -> Response:
    """
    Deletes animator by ID.
    ---
    tags:
      - Animator
    parameters:
      - in: path
        name: animator_id
        schema:
          type: integer
        required: true
        description: ID of the animator
    responses:
      204:
        description: Animator deleted
      404:
        description: Animator not found
    """
    animator_controller.delete_animator(animator_id)
    return make_response("Animator deleted", HTTPStatus.NO_CONTENT)


@animator_bp.get('/name/<string:name>')
def get_animator_by_name(name: str) -> Response:
    """
    Gets animator(s) by name.
    ---
    tags:
      - Animator
    parameters:
      - in: path
        name: name
        schema:
          type: string
        required: true
        description: Name of the animator
    responses:
      200:
        description: List of animators with given name
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
    """
    animators = animator_controller.get_animator_by_name(name)
    return make_response(jsonify([animator.put_into_dto() for animator in animators]), HTTPStatus.OK)


@animator_bp.get('/phone/<string:phone>')
def get_animator_by_phone(phone: str) -> Response:
    """
    Gets animator(s) by phone.
    ---
    tags:
      - Animator
    parameters:
      - in: path
        name: phone
        schema:
          type: string
        required: true
        description: Phone number of the animator
    responses:
      200:
        description: List of animators with given phone
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
    """
    animators = animator_controller.get_animator_by_phone(phone)
    return make_response(jsonify([animator.put_into_dto() for animator in animators]), HTTPStatus.OK)
