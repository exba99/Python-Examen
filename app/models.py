from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Proprietaire(db.Model):
    __tablename__ = "proprietaire"
    id = db.Column(db.Integer, primary_key=True)
    identification = db.Column(db.String(20), unique=True)
    nom = db.Column(db.String(20))
    prenom = db.Column(db.String(20))
    adresse = db.Column(db.String(50))
    email = db.Column(db.String(20), unique=True)
    password_hash = db.Column(db.String(255))
    bails = db.relationship('Bail', backref='proprietaire', lazy='dynamic')
    titres = db.relationship('TitreFoncier', backref='proprietaire', lazy='dynamic')
    demandes = db.relationship('Demande', backref='landlord', lazy='dynamic')
    type_proprio = db.Column(db.Integer, db.ForeignKey('type_proprietaire.id'))
    

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class TypeProprietaire(db.Model):
    __tablename__ = 'type_proprietaire'
    id = db.Column(db.Integer, primary_key=True) 
    libelle = db.Column(db.String(64), unique=True)
    propietaires = db.relationship('Proprietaire', backref='typeProprietaire', lazy='dynamic')

    def __repr__(self):
        return '<TypeProprietaire %r>' % self.name

class TitreFoncier(db.Model):
    __tablename__ = 'titrefoncier'
    id = db.Column(db.Integer, primary_key=True)
    nicad = db.Column(db.String(16), unique=True, nullable=False)
    numeroLot = db.Column(db.String(20), unique=True)
    terrain_id = db.Column(db.Integer, db.ForeignKey('terrain.id'))
    proprietaire_id = db.Column(db.Integer, db.ForeignKey('proprietaire.id'))

    def __repr__(self):
        return '<TitreFoncier %r>' % self.nicad

class Bail(db.Model):
    __tablename__ = 'bail'
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(10), unique=True)
    dateDebut = db.Column(db.DateTime)
    dateFin = db.Column(db.DateTime)
    loyer = db.Column(db.Float)
    terrain_id = db.Column(db.Integer, db.ForeignKey('terrain.id'))
    owner_id = db.Column(db.Integer, db.ForeignKey('proprietaire.id'))

    def __repr__(self):
        return '<Bail %r>' % self.numero

class TypeDemande(db.Model):
    __tablename__ = 'type_demande'
    id = db.Column(db.Integer, primary_key=True)
    libelle = db.Column(db.String(20), unique=True)
    
    demandes = db.relationship('Demande', backref='typeDemande', lazy='dynamic')

    def __repr__(self):
        return '<TypeDemande %r>' % self.libelle

class Demande(db.Model):
    __tablename__ = 'demande'
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(20), unique=True)
    date = db.Column(db.DateTime)
    acte = db.Column(db.Text)
    plan = db.Column(db.Text)
    etat = db.Column(db.String(20))
    type_demande = db.Column(db.Integer, db.ForeignKey('type_demande.id'))
    terrain_id = db.Column(db.Integer, db.ForeignKey('terrain.id'))
    landlord_id = db.Column(db.Integer, db.ForeignKey('proprietaire.id'))

class Terrain(db.Model):
    __tablename__ = 'terrain'
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(20), unique=True)
    longueur = db.Column(db.Float)
    largeur = db.Column(db.Float)
    etat = db.Column(db.Boolean)
    titre = db.relationship('TitreFoncier', uselist=False, backref = 'terrain_titre')
    bail = db.relationship('Bail', uselist=False, backref = 'terrain_bail')
    demandes = db.relationship('Demande', backref='terrain_demandes', lazy='dynamic')
    secteur_id = db.Column(db.Integer, db.ForeignKey('secteur.id'))

    def __repr__(self):
        return '<Terrain %r>' % self.numero

class Secteur(db.Model):
    __tablename__ = 'secteur'
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(10), unique=True)
    terrains = db.relationship('Terrain', backref='secteur')
    arrondissement_id = db.Column(db.Integer, db.ForeignKey('arrondissement.id'))

    def __repr__(self):
        return '<Secteur %r>' % self.numero

class Arrondissement(db.Model):
    __tablename__ = 'arrondissement'
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(10))
    nom = db.Column(db.String(30))
    departement_id = db.Column(db.Integer, db.ForeignKey('departement.id'))
    secteurs = db.relationship('Secteur', backref='arrondissement')

    def __repr__(self):
        return '<Arrondissement %r>' % self.numero

class Region(db.Model):
    __tablename__ = 'departement'
    __tablename__ = 'region'
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(10))
    nom = db.Column(db.String(30))
    departements = db.relationship('Departement', backref='region')

class Departement(db.Model):
    def __repr__(self):
        return '<Region %r>' % self.numero
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(10))
    nom = db.Column(db.String(30))
    arrondissements = db.relationship('Arrondissement', backref='departement')
    region_id = db.Column(db.Integer, db.ForeignKey('region.id'))

    def __repr__(self):
        return '<Departement %r>' % self.numero

class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(20))
    prenom = db.Column(db.String(20))
    adresse = db.Column(db.String(50))
    login = db.Column(db.String(20), unique=True)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
