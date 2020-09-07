from flask import render_template, redirect, session, url_for
from . import titre
from .. import db
from app.models import Terrain, TitreFoncier

@titre.route('/new/<idTerrain>')
def nouveauTitre(idTerrain):
    terrain = Terrain.query.filter_by(id=idTerrain)
    