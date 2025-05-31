from flask import Blueprint, render_template

crianza = Blueprint('crianza', __name__)

@crianza.route('/crianza')
def crianza_page():
    return render_template('crianza/crianza.html')

@crianza.route('/crianza/editar')
def crianza_edit_page():
    return render_template('crianza/edit_crianza.html')