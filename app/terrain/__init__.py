from flask import Blueprint

terrain = Blueprint('terrain', __name__)

from . import views, errors