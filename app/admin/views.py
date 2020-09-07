from flask import render_template, session, redirect, url_for, request, flash, jsonify
from . import admin as adminbp
from .. import db
from flask_login import login_required, login_user, logout_user
from app.models import *
from .forms import *
import sys
from datetime import date, timedelta
import calendar
from pprint import pprint

@adminbp.route('/login')
def login():
    form = PropLogin()
    if form.validate_on_submit():
        prop = Proprietaire.query.filter_by(login = form.username.data).first()
        if prop is not None and prop.verify_password(form.password.data):
            login_user(prop)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                return redirect(next) 
        flash('Login ou mot de passe incorrect')
    return render_template('admin/userlogin.html', form=form)

@adminbp.route('/logoutAdmin')
@login_required
def logout():
    logout_user()
    return redirect('/admin')

@adminbp.route('/register', methods=['GET', 'POST'])
def register():
    form = PropRegister()
    types = TypeProprietaire.query.all()
    form.profil.choices = [(sec.id, sec.libelle) for sec in types]
    if form.is_submitted():
        prop = Proprietaire()
        prop.identification = form.cin.data
        prop.nom = form.nom.data
        prop.prenom = form.prenom.data
        prop.adresse = form.adresse.data
        prop.email = form.email.data
        prop.password = form.password.data
        prop.type_proprio = form.profil.data
        db.session.add(prop)
        db.session.commit()
        flash('Inscription Réussie')
        return redirect('login')

    return render_template('admin/userregister.html', form=form)

@adminbp.route('/admin', methods=['GET', 'POST'])
def adminLog():
    form = AdminLogin()

    if form.validate_on_submit():
        user = User.query.filter_by(login = form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            next = request.args.get('next')
            if next is not None:
                return redirect(next)
            return redirect('/dashboard')
        flash('Login ou mot de passe incorrect')

    return render_template('admin/adminlogin.html', form=form)


@adminbp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = NewTerrain()
    secteurs = Secteur.query.all()
    form.secteur.choices = [(sec.id, sec.numero) for sec in secteurs]

    if form.is_submitted():
        terrain = Terrain()
        terrain.numero = form.numero.data
        terrain.largeur = form.largeur.data
        terrain.longueur = form.longueur.data
        terrain.secteur_id = form.secteur.data
        db.session.add(terrain)
        db.session.commit()
        flash('Terrain ajouté avec succès')

    terrains = Terrain.query.all()
    return render_template('admin/dashboard.html', form=form, array=terrains)

@adminbp.route('/titre')
@login_required
def titre():
    demandes = db.session.query(TypeDemande, Terrain, Secteur, Proprietaire, Demande, Arrondissement, Region, Departement).filter(Demande.type_demande == TypeDemande.id, Demande.terrain_id == Terrain.id, Demande.landlord_id == Proprietaire.id, Terrain.secteur_id == Secteur.id, Secteur.arrondissement_id == Arrondissement.id, Arrondissement.departement_id == Departement.id, Departement.region_id == Region.id).all()
    #demandes = Demande.query.join(TypeDemande).join((Terrain.query.join(Secteur))).join(Proprietaire).all()
    return render_template('admin/titre.html', array=demandes)

@adminbp.route('/rejeter/<id>')
@login_required
def regeter(id):
    demande = Demande.query.get(id)
    demande.etat = "rejeter"
    db.session.add(demande)
    db.session.commit()
    return '1'

@adminbp.route('/accepter/<id>')
@login_required
def accepter(id):
    demande = db.session.query(TypeDemande, Demande).filter(Demande.type_demande == TypeDemande.id, Demande.id == id).first()
    if demande.TypeDemande.libelle == 'Bails':
        bail = Bail()
        bail.numero = "BAIL-" + demande.Demande.id
        bail.dateDebut = date.today()
        days_in_month = calendar.monthrange(bail.dateDebut.year, bail.dateDebut.month)[1]
        end_date = start_date + timedelta(days=days_in_month)
        bail.dateFin = end_date
        bail.loyer = 300000
        bail.terrain_id = demande.Demande.terrain_id
        bail.owner_id = demande.Demande.landlord_id
        db.session.add(bail)
        db.session.commit()
    elif demande.TypeDemande.libelle == 'Titre Foncier':
        titre = TitreFoncier()
        titre.nicad = "NICAD-0" + str(demande.Demande.terrain_id)
        titre.numeroLot = "LOT-0" + str(demande.Demande.terrain_id)
        titre.proprietaire_id = demande.Demande.landlord_id
        titre.terrain_id = demande.Demande.terrain_id
        db.session.add(titre)
        db.session.commit()
    demande.Demande.etat = "accepter"
    dem = Demande()
    dem = demande.Demande
    db.session.add(dem)
    db.session.commit()
    return '1'
