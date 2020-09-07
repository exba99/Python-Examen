from flask import render_template, session, redirect, url_for
from . import terrain
from .. import db
from app.models import *

@terrain.route('/')
def listeTerrain():
    db.create_all()
    return render_template('base.html')


@terrain.route('/detail/<idTerrain>')
def detail(idTerrain):
    terrain = Terrain.query.filter_by(id=idTerrain)
    if terrain is None:
        return redirect(url_for('notFound'))
    else:
        return render_template('terrain/detail.html', terrain = terrain)

@terrain.route('/a-vendre')
def sold():
    terrains = Terrain.query.all()
    return render_template('terrain/vente.html', terrains=terrains)