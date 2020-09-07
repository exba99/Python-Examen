from flask import Blueprint

titre = Blueprint('titre', __name__)

from . import views, errors