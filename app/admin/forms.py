from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length
from wtforms.fields.html5 import EmailField


class AdminLogin(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Se Connecter")

class PropLogin(FlaskForm):
    email = EmailField("email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Se Connecter")

class NewTerrain(FlaskForm):
    numero = StringField("Numero terrain", validators=[DataRequired()])
    longueur = IntegerField("Longueur", validators=[DataRequired()])
    largeur = IntegerField("Largeur", validators=[DataRequired()])
    secteur = SelectField("Secteur")
    submit = SubmitField("Ajouter")

class PropRegister(FlaskForm):
    cin = StringField("CIN", validators=[DataRequired()])
    nom = StringField("Nom", validators=[DataRequired()])
    prenom = StringField("Prenom", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("PAssword", validators=[DataRequired()])
    adresse = TextAreaField("Adresse", validators=[DataRequired()])
    profil = SelectField("Type")
    submit = SubmitField("S'inscrire")