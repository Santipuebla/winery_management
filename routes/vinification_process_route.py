from flask import Blueprint, request, render_template
from models.db import db
from models.vinification_process import VinificationProcess
from models.grape_variety import GrapeVariety # Importamos GrapeVariety para validar FK
import datetime # Para manejar directamente el uso de fechas

vinification_process_bp = Blueprint('vinification_process_bp', __name__)

@vinification_process_bp.route('/process', methods=['GET'])
def get_all_vinification_processes():
    vinification_process_list = VinificationProcess.query.all()
    context = { "vinification_process_list": vinification_process_list }
    return render_template('vinificacion_process/vinificacion_process.html',**context)

