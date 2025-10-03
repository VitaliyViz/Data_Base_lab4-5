from http import HTTPStatus
from flask import Blueprint, jsonify, Response, request, make_response
from my_project.auth.controller import agencies_controller
from my_project.auth.domain.orders.agencies import Agencies

agencies_bp = Blueprint('agencies', __name__, url_prefix='/agencies')


@agencies_bp.get('')
def get_all_agencies() -> Response:
    """
    Gets all agencies from the database.
    ---
    tags:
      - Agencies
    responses:
      200:
        description: List of all agencies
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
                properties:
                  id: {type: integer}
                  name: {type: string}
                  phone: {type: string}
                  email: {type: string}
                  address: {type: string}
    """
    agencies = agencies_controller.find_all()
    agencies_dto = [agency.put_into_dto() for agency in agencies]
    return make_response(jsonify(agencies_dto), HTTPStatus.OK)


# @agencies_bp.post('')
# def create_agency() -> Response:
#     """
#     Creates a new agency in the database.
#     ---
#     tags:
#       - Agencies
#     consumes:
#       - application/json
#     parameters:
#       - in: body
#         name: body
#         required: true
#         schema:
#           type: object
#           properties:
#             name: {type: string}
#             phone: {type: string}
#             email: {type: string}
#             address: {type: string}
#           required: [name, phone, email]
#     responses:
#       201:
#         description: Agency created
#         content:
#           application/json:
#             schema:
#               type: object
#               properties:
#                 id: {type: integer}
#                 name: {type: string}
#                 phone: {type: string}
#                 email: {type: string}
#                 address: {type: string}
#     """
#     if not request.is_json:
#         return make_response(jsonify({"error": "Content-Type must be application/json"}), 415)
#     content = request.get_json()
#     agency = Agencies.create_from_dto(content)
#     agencies_controller.create_agency(agency)
#     return make_response(jsonify(agency.put_into_dto()), HTTPStatus.CREATED)


@agencies_bp.get('/<int:agency_id>')
def get_agency(agency_id: int) -> Response:
    """
    Gets agency by ID.
    ---
    tags:
      - Agencies
    parameters:
      - in: path
        name: agency_id
        schema:
          type: integer
        required: true
        description: ID of the agency
    responses:
      200:
        description: Agency found
        content:
          application/json:
            schema:
              type: object
      404:
        description: Agency not found
    """
    agency = agencies_controller.find_by_id(agency_id)
    if agency:
        return make_response(jsonify(agency.put_into_dto()), HTTPStatus.OK)
    return make_response(jsonify({"error": "Agency not found"}), HTTPStatus.NOT_FOUND)


@agencies_bp.put('/<int:agency_id>')
def update_agency(agency_id: int) -> Response:
    """
    Updates agency by ID.
    ---
    tags:
      - Agencies
    consumes:
      - application/json
    parameters:
      - in: path
        name: agency_id
        schema:
          type: integer
        required: true
        description: ID of the agency
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            name: {type: string}
            phone: {type: string}
            email: {type: string}
            address: {type: string}
    responses:
      200:
        description: Agency updated
      404:
        description: Agency not found
    """
    if not request.is_json:
        return make_response(jsonify({"error": "Content-Type must be application/json"}), 415)
    content = request.get_json()
    agency = Agencies.create_from_dto(content)
    agencies_controller.update_agency(agency_id, agency)
    return make_response("Agency updated", HTTPStatus.OK)


@agencies_bp.delete('/<int:agency_id>')
def delete_agency(agency_id: int) -> Response:
    """
    Deletes agency by ID.
    ---
    tags:
      - Agencies
    parameters:
      - in: path
        name: agency_id
        schema:
          type: integer
        required: true
        description: ID of the agency
    responses:
      204:
        description: Agency deleted
      404:
        description: Agency not found
    """
    agencies_controller.delete_agency(agency_id)
    return make_response("Agency deleted", HTTPStatus.NO_CONTENT)


@agencies_bp.get('/name/<string:name>')
def get_agencies_by_name(name: str) -> Response:
    """
    Gets agencies by name.
    ---
    tags:
      - Agencies
    parameters:
      - in: path
        name: name
        schema:
          type: string
        required: true
        description: Name of the agency
    responses:
      200:
        description: List of agencies with given name
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
    """
    agencies = agencies_controller.get_agencies_by_name(name)
    return make_response(jsonify([agency.put_into_dto() for agency in agencies]), HTTPStatus.OK)


@agencies_bp.get('/phone/<string:phone>')
def get_agencies_by_phone(phone: str) -> Response:
    """
    Gets agencies by phone.
    ---
    tags:
      - Agencies
    parameters:
      - in: path
        name: phone
        schema:
          type: string
        required: true
        description: Phone number of the agency
    responses:
      200:
        description: List of agencies with given phone
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
    """
    agencies = agencies_controller.get_agencies_by_phone(phone)
    return make_response(jsonify([agency.put_into_dto() for agency in agencies]), HTTPStatus.OK)
