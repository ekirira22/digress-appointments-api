from models.dbmodel import db
from flask import Flask, request, make_response, current_app, jsonify
from flask_restful import Api, Resource
from flask_cors import CORS
from sqlalchemy.exc import IntegrityError
from flask_bcrypt import Bcrypt


def create_app():
    global bcrypt
    # create flask app
    app = Flask(__name__)
    CORS(app)

    # Get specific configs. That we did in DB and ability to track modifications configured in app.py
    app.config.from_object('config.Config')

    # initialize app with db
    db.init_app(app)

    bcrypt = Bcrypt(app)

    api = Api(app)

    # Establish routes

    return app
