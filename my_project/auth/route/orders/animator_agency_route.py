from http import HTTPStatus
from flask import Blueprint, jsonify, make_response

from my_project.auth.controller import animator_agency_controller

animator_agency_bp = Blueprint('animator_agency', __name__, url_prefix='/animator_agency')


@animator_agency_bp.get('/')
def get_all_relationships():
    """
    Gets all relationships between animators and agencies.
    ---
    tags:
      - AnimatorAgency
    responses:
      200:
        description: List of all animator-agency relationships
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
                properties:
                  animator_id: {type: integer}
                  agency_id: {type: integer}
    """
    relationships = animator_agency_controller.get_all_relationships()
    return make_response(jsonify(relationships), HTTPStatus.OK)


@animator_agency_bp.get('/agency/<int:agency_id>')
def get_animators_by_agency(agency_id: int):
    """
    Gets all animators for a specific agency.
    ---
    tags:
      - AnimatorAgency
    parameters:
      - in: path
        name: agency_id
        schema:
          type: integer
        required: true
        description: ID of the agency
    responses:
      200:
        description: List of animators for the given agency
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
    animators = animator_agency_controller.get_animators_by_agency(agency_id)
    return make_response(jsonify([animator.put_into_dto() for animator in animators]), HTTPStatus.OK)


@animator_agency_bp.get('/animator/<int:animator_id>')
def get_agencies_by_animator(animator_id: int):
    """
    Gets all agencies for a specific animator.
    ---
    tags:
      - AnimatorAgency
    parameters:
      - in: path
        name: animator_id
        schema:
          type: integer
        required: true
        description: ID of the animator
    responses:
      200:
        description: List of agencies for the given animator
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
    agencies = animator_agency_controller.get_agencies_by_animator(animator_id)
    return make_response(jsonify([agency.put_into_dto() for agency in agencies]), HTTPStatus.OK)
