from flask import Blueprint

users = Blueprint('users', __name__, '/users/')

from .models import User