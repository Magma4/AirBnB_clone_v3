#!/usr/bin/python3
"""state view"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State
import json


@app_views.route('/states', strict_slashes=False)
def states():
    """retrieves all state objects"""
    objs = storage.all(State)
    objs_list = []
    for key,val in objs.items():
        objs_list.append(val.to_dict())
    return jsonify(objs_list)


@app_views.route('/states/<state_id>', strict_slashes=False)
def one_state(state_id):
    """retrieves one state object given the id"""
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """deletes the state object"""
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    return jsonify(dict())


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """creates a state object"""
    try:
        body = request.get_json()
    except(exception):
        return "Not a JSON", 400
    if 'name' not in body.keys():
        return "Missing name", 400
    obj = State(**body)
    storage.new(obj)
    storage.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """updates a state obj"""
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    try:
        body = request.get_json()
    except(exception):
        return "Not a JSON", 400
    obj = obj.to_dict()
    new_obj = {**obj, **body}
    obj = State(**new_obj)
    storage.save()
    return jsonify(obj.to_dict())
