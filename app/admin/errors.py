from flask import render_template
from . import admin

@admin.app_errorhandler(404)
def notFound(e):
    return render_template('error/404.html'), 404


@admin.app_errorhandler(500)
def internalError(e):
    return render_template('error/500.html'), 500