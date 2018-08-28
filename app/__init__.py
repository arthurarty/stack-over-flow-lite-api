from flask import Flask, request, jsonify
# local import
from app.config import app_config
import json

def create_app():
    from flask_jwt_extended import (
    JWTManager)

    app = Flask(__name__, instance_relative_config=True)
    app.config['JWT_SECRET_KEY'] = 'qweBas12@!asBASD'
    jwt = JWTManager(app)
    
    return app
