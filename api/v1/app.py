#!/usr/bin/python3
""" Status of our API """
from models import storage
from api.v1.views import app_views
from os import getenv
from flask import Flask, make_response, jsonify
from flask import Blueprint
from flask_cors import CORS

"""Host and port env variables"""
host_env = getenv('HBNB_API_HOST') or '0.0.0.0'
port_env = getenv('HBNB_API_PORT') or 5000

app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)
""" Cors access to selected resources from a different origin."""
cors = CORS(app, resources={"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_db(error):
    """ Close db session """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """
    Method to manage the url's that does'nt exist
    """
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    """
    Main Function
    """
    app.run(
        host=host_env, port=port_env,
        debug=True, threaded=True,
    )
