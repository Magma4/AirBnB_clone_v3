#!/usr/bin/python3
"""the first version of the airbnb api"""
from flask import Flask, request, jsonify, json
import os
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(self):
    """closes the filestorage"""
    storage.close()


@app.errorhandler(404)
def page_not_found(ex):
    """handles error for bad api url"""
    if request.path.startswith('/api/v1/'):
        res = ex.get_response()
        res.data = json.dumps({"error": "Not found"})
    return res


if __name__ == "__main__":
    host = '0.0.0.0'
    port = '5000'
    if os.getenv('HBNB_API_HOST'):
        host = os.getenv('HBNB_API_HOST')
    if os.getenv('HBNB_API_PORT'):
        port = os.getenv('HBNB_API_PORT')
    app.run(host=host, port=port, threaded=True)
