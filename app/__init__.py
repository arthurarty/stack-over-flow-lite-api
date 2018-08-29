from flask import Flask, request, jsonify
# local import
from app.config import app_config
from flasgger import Swagger
import json

def create_app():
    from flask_jwt_extended import (
    JWTManager)

    app = Flask(__name__, instance_relative_config=True)
    swag= Swagger(app)
    app.config['JWT_SECRET_KEY'] = 'qweBas12@!asBASD'
    JWTManager(app)
    
    return app
