from flask import Blueprint, render_template

recepcion = Blueprint('recepcion', __name__, url_prefix='/recepcion')

@recepcion.route('/')
def show_form():
    return render_template('recepcion/recepcion.html')
