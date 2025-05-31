from models.db import db
from flask import Blueprint, jsonify, request, render_template
from models.grape_variety import GrapeVariety 
from models.vinification_process import VinificationProcess
from models.fermentation_stage import FermentationStage

import datetime

fermentation = Blueprint('fermentation', _name_, url_prefix='/fermentation')


UPLOAD_FOLDER = 'static/images' 
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@fermentation.route('/get_all_fermetations', methods=['GET'])
def get_all_fermetations():
    processes = FermentationStage.query.all()
    context = {"fermentations": processes}
    return render_template("fermentation/fermentacion.html", **context)


@fermentation.route('/<uuid:process_id>/fermentation_stage', methods=['GET'])
def get_fermentation_stage(process_id):
    vinification_process = FermentationStage.query.get(str(process_id))
    if not vinification_process:
        return jsonify({"success": False, "message": "Proceso de Vinificación no encontrado."}), 404

    fermentation_stage = vinification_process.fermentation_stage
    if not fermentation_stage:
        return jsonify({"success": False, "message": "Etapa de fermentación para este proceso no encontrada."}), 404
    
    return jsonify({"success": True, "data": fermentation_stage.serialize()}), 200

@fermentation.route('/<uuid:process_id>/fermentation_stage', methods=['POST'])
def create_fermentation_stage(process_id):
    vinification_process = FermentationStage.query.get(str(process_id))
    if not vinification_process:
        return jsonify({"success": False, "message": "Proceso de Vinificación no encontrado."}), 404

    # Validar si ya existe una etapa de fermentación para este proceso (debido a unique=True)
    if vinification_process.fermentation_stage:
        return jsonify({"success": False, "message": "Este proceso de vinificación ya tiene una etapa de fermentación asociada."}), 409 #  Conflict

    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Datos JSON no proporcionados."}), 400

    errors = {}

    fermentation_start_date_str = data.get('fermentation_start_date')
    density = data.get('density')
    total_acidity = data.get('total_acidity')
    temperature_celsius = data.get('temperature_celsius')
    fermentation_end_date_str = data.get('fermentation_end_date')
    observations = data.get('observations')

    # ConvertiMOS y validaMOS LAS fechas
    fermentation_start_date = None
    if not fermentation_start_date_str:
        errors['fermentation_start_date'] = "La fecha de inicio de fermentación es requerida."
    else:
        try:
            fermentation_start_date = datetime.datetime.strptime(fermentation_start_date_str, '%Y-%m-%d').date()
        except ValueError:
            errors['fermentation_start_date'] = "Formato de fecha de inicio inválido (YYYY-MM-DD)."
    
    fermentation_end_date = None
    if fermentation_end_date_str:
        try:
            fermentation_end_date = datetime.datetime.strptime(fermentation_end_date_str, '%Y-%m-%d').date()
        except ValueError:
            errors['fermentation_end_date'] = "Formato de fecha de fin inválido (YYYY-MM-DD)."
    
    # Validamos si la fecha de fin es anterior a la de inicio
    if fermentation_start_date and fermentation_end_date and fermentation_end_date < fermentation_start_date:
        errors['fermentation_end_date'] = "La fecha de fin no puede ser anterior a la fecha de inicio."

    # Validar números (densidad, acidez, temperatura)
    if not isinstance(density, (int, float)):
        errors['density'] = "La densidad es requerida y debe ser un número."
    if not isinstance(total_acidity, (int, float)):
        errors['total_acidity'] = "La acidez total es requerida y debe ser un número."
    if not isinstance(temperature_celsius, (int, float)):
        errors['temperature_celsius'] = "La temperatura es requerida y debe ser un número."

    # Validar observaciones (opcional pero puede tener límite de longitud si es Text)
    if observations is not None and not isinstance(observations, str):
        errors['observations'] = "Las observaciones deben ser texto."

    if errors:
        return jsonify({"success": False, "message": "Datos de entrada inválidos.", "errors": errors}), 422

    try:
        new_fermentation_stage = FermentationStage(
            fermentation_start_date=fermentation_start_date,
            fermentation_end_date=fermentation_end_date,
            density=density,
            total_acidity=total_acidity,
            temperature_celsius=temperature_celsius,
            observations=observations,
            vinification_process_id=str(process_id)
        )
        db.session.add(new_fermentation_stage)
        db.session.commit()
        return jsonify({"success": True, "data": new_fermentation_stage.serialize()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": f"Error al crear la etapa de fermentación: {str(e)}"}), 500

@fermentation.route('/<uuid:process_id>/fermentation_stage', methods=['PUT'])
def update_fermentation_stage(process_id):
    vinification_process = FermentationStage.query.get(str(process_id))
    if not vinification_process:
        return jsonify({"success": False, "message": "Proceso de Vinificación no encontrado."}), 404

    fermentation_stage = vinification_process.fermentation_stage
    if not fermentation_stage:
        return jsonify({"success": False, "message": "Etapa de fermentación para este proceso no encontrada."}), 404

    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Datos JSON no proporcionados."}), 400

    errors = {}

    if 'fermentation_start_date' in data:
        try:
            fermentation_stage.fermentation_start_date = datetime.datetime.strptime(data['fermentation_start_date'], '%Y-%m-%d').date()
        except ValueError:
            errors['fermentation_start_date'] = "Formato de fecha de inicio inválido (YYYY-MM-DD)."
    
    if 'fermentation_end_date' in data:
        if data['fermentation_end_date'] is None:
            fermentation_stage.fermentation_end_date = None
        else:
            try:
                fermentation_stage.fermentation_end_date = datetime.datetime.strptime(data['fermentation_end_date'], '%Y-%m-%d').date()
            except ValueError:
                errors['fermentation_end_date'] = "Formato de fecha de fin inválido (YYYY-MM-DD)."
    
    # Validar si la fecha de fin es anterior a la de inicio después de las actualizaciones
    if fermentation_stage.fermentation_start_date and fermentation_stage.fermentation_end_date and \
        fermentation_stage.fermentation_end_date < fermentation_stage.fermentation_start_date:
        errors['fermentation_end_date'] = "La fecha de fin no puede ser anterior a la fecha de inicio."


    if 'density' in data:
        if not isinstance(data['density'], (int, float)):
            errors['density'] = "La densidad debe ser un número."
        else:
            fermentation_stage.density = data['density']

    if 'total_acidity' in data:
        if not isinstance(data['total_acidity'], (int, float)):
            errors['total_acidity'] = "La acidez total debe ser un número."
        else:
            fermentation_stage.total_acidity = data['total_acidity']

    if 'temperature_celsius' in data:
        if not isinstance(data['temperature_celsius'], (int, float)):
            errors['temperature_celsius'] = "La temperatura debe ser un número."
        else:
            fermentation_stage.temperature_celsius = data['temperature_celsius']

    if 'observations' in data:
        if data['observations'] is not None and not isinstance(data['observations'], str):
            errors['observations'] = "Las observaciones deben ser texto."
        else:
            fermentation_stage.observations = data['observations']

    if errors:
        return jsonify({"success": False, "message": "Datos de entrada inválidos.", "errors": errors}), 422

    try:
        db.session.commit()
        return jsonify({"success": True, "data": fermentation_stage.serialize()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": f"Error al actualizar la etapa de fermentación: {str(e)}"}), 500


@fermentation.route('/<uuid:process_id>/fermentation_stage', methods=['DELETE'])
def delete_fermentation_stage(process_id):
    vinification_process = FermentationStage.query.get(str(process_id))
    if not vinification_process:
        return jsonify({"success": False, "message": "Proceso de Vinificación no encontrado."}), 404

    fermentation_stage = vinification_process.fermentation_stage
    if not fermentation_stage:
        return jsonify({"success": False, "message": "Etapa de fermentación para este proceso no encontrada."}), 404

    try:
        db.session.delete(fermentation_stage)
        db.session.commit()
        return jsonify({"success": True, "message": "Etapa de fermentación eliminada correctamente."}), 204 # 204 No Content
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": f"Error al eliminar la etapa de fermentación: {str(e)}"}), 500