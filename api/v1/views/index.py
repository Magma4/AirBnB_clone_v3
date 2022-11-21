#!/usr/bin/python3
"""the index file"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models.review import Review
from models.city import City


@app_views.route('/status')
def status():
    """returns the status of the request"""
    return jsonify({'status': 'OK'})


@app_views.route('/stats')
def count_all_objs():
    """returns the number of all objects"""
    classes = {"amenities": Amenity, "cities": City,
               "places": Place, "reviews": Review,
               "states": State, "users": User}
    objs = dict()
    for key, val in classes.items():
        objs[key] = storage.count(val)
    return jsonify_error(objs)
