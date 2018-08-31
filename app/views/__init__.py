import re

from flasgger import swag_from
from flask import Flask, jsonify, request
from flask_jwt_extended import (JWTManager, create_access_token,
                                get_jwt_identity, jwt_required)
from werkzeug.security import check_password_hash, generate_password_hash

from app import create_app
from app.database import Database
from app.models.answer import Answer

app = create_app()
db_conn = Database()
empty_field = {'msg': 'A field is empty'}

# import auth views
from app.views import auth

# import question views.
from app.views import questions

# import answers views
from app.views import answers
