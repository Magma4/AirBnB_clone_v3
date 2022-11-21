#!/usr/bin/python3
"""This is the view module for states. It
implements all endpoints to get, delete, create and update
a new state object
"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State
import json


@app_views.route('/states', strict_slashes=False)
def states():
    """retrieves all state objects from the filestore or db and returns it"""
    objs = storage.all(State)
    objs_list = []
    for key, val in objs.items():
        objs_list.append(val.to_dict())
    return jsonify(objs_list)


@app_views.route('/states/<state_id>', strict_slashes=False)
def one_state(state_id):
    """retrieves one state object given the id and returns it"""
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """deletes the state object from the file storage or db"""
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify(dict())


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """creates a new state object and saves it to the file or db"""
    try:
        body = request.get_json()
    except(exception):
        return "Not a JSON", 400
    if 'name' not in body.keys():
        return "Missing name", 400
    obj = State(**body)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """updates a state obj with new information and saves the changes"""
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    try:
        body = request.get_json()
    except(exception):
        return "Not a JSON", 400
    storage.delete(obj)
    obj = obj.to_dict()
    new_obj = {**obj, **body}
    obj = State(**new_obj)
    obj.save()
    return jsonify(obj.to_dict())
