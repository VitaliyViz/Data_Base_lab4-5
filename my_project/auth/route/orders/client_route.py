from http import HTTPStatus

from flask import Blueprint, jsonify, Response, request, make_response

from my_project.auth.controller import client_controller
from my_project.auth.domain import Client

client_bp = Blueprint('clients', __name__, url_prefix='/clients')


@client_bp.get('')
def get_all_clients() -> Response:
    """
    Gets all objects from table using Client layer.
    :return: Response object
    """
    return make_response(jsonify(client_controller.find_all()), HTTPStatus.OK)


@client_bp.post('')
def create_client() -> Response:
    """
    Gets all objects from table using Client layer.
    :return: Response object
    """
    content = request.get_json()
    client = Client.create_from_dto(content)
    client_controller.create(client)
    return make_response(jsonify(client.put_into_dto()), HTTPStatus.CREATED)


@client_bp.get('/<int:client_id>')
def get_client(client_id: int) -> Response:
    """
    Gets client by ID.
    :return: Response object
    """
    return make_response(jsonify(client_controller.find_by_id(client_id)), HTTPStatus.OK)


@client_bp.put('/<int:client_id>')
def update_client(client_id: int) -> Response:
    """
    Updates client by ID.
    :return: Response object
    """
    content = request.get_json()
    client = Client.create_from_dto(content)
    client_controller.update(client_id, client)
    return make_response("Client updated", HTTPStatus.OK)


@client_bp.patch('/<int:client_id>')
def patch_client(client_id: int) -> Response:
    """
    Patches client by ID.
    :return: Response object
    """
    content = request.get_json()
    client_controller.patch(client_id, content)
    return make_response("Client updated", HTTPStatus.OK)


@client_bp.delete('/<int:client_id>')
def delete_client(client_id: int) -> Response:
    """
    Deletes client by ID.
    :return: Response object
    """
    client_controller.delete(client_id)
    return make_response("Client deleted", HTTPStatus.OK)


@client_bp.get('/get-clients-after-number/<int:in_num>')
def get_clients_after_number(in_num: int) -> Response:
    """
    Gets Client objects from database table with field 'number' >= in_number using Client layer.
    :param in_num: number value
    :return: Response object
    """
    return make_response(jsonify(client_controller.get_clients_after_number(in_num)), HTTPStatus.OK)


@client_bp.get('/get-client-with-name/<string:name_filter>/after-number/<int:in_num>')
def get_clients_with_name_and_number_filter(name_filter: str, in_num: int) -> Response:
    """
    Gets Client objects from database table with field 'number' >= in_number using Client layer.
    :param name_filter: first letters of name
    :param in_num: number value
    :return: Response object
    """
    return make_response(jsonify(client_controller.get_clients_with_name_and_number_filter(name_filter, in_num)),
                         HTTPStatus.OK)
