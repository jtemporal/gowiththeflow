"""API for go with the flow presentaiton"""
from flask import Flask, jsonify, make_response
from flask_cors import cross_origin

from config import config

from utils.decorators import requires_auth

app = Flask(__name__)


@app.get('/home')
def home():
    """unprotected home endpoint"""
    response = {
        "message": "there's no place like home"
    }
    return make_response(jsonify(response), 200)


@app.get('/door')
@cross_origin(allow_headers=["Content-Type", "Authorization"])
@requires_auth
def door():
    """door endpoint"""
    response = {
        "message": "You got through the door"
    }
    return make_response(jsonify(response), 200)
