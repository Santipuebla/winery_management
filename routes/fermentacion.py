from flask import Blueprint, render_template

fermentacion = Blueprint('fermentacion', __name__, url_prefix='/fermentacion')

@fermentacion.route('/')
def form():
    return render_template('fermentacion/fermentacion.html')
