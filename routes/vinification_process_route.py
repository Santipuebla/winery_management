from flask import Blueprint, request, jsonify
from models.db import db
from models.vinification_process import VinificationProcess
from models.grape_variety import GrapeVariety # Importamos GrapeVariety para validar FK
import datetime # Para manejar directamente el uso de fechas

vinification_process_bp = Blueprint('vinification_process_bp', _name_)

@vinification_process_bp.route('/', methods=['GET'])
def get_all_vinification_processes():
    """
    Obtiene todos los procesos de vinificación existentes.
    """
    processes = VinificationProcess.query.all()
    return jsonify({"success": True, "data": [p.serialize() for p in processes]}), 200

@vinification_process_bp.route('/', methods=['POST'])
def create_vinification_process():
    """
    Crea un nuevo proceso de vinificación.
    Requiere: start_date, current_stage, grape_variety_id
    Opcional: end_date, description
    """
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Datos JSON no proporcionados."}), 400

    errors = {}

    start_date_str = data.get('start_date')
    current_stage = data.get('current_stage')
    grape_variety_id = data.get('grape_variety_id')
    end_date_str = data.get('end_date')
    description = data.get('description')

    # 1. Validar start_date
    start_date = None
    if not start_date_str:
        errors['start_date'] = "La fecha de inicio es requerida."
    else:
        try:
            start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d').date()
        except ValueError:
            errors['start_date'] = "Formato de fecha de inicio inválido (YYYY-MM-DD)."
    
    # 2. Validar current_stage
    if not current_stage:
        errors['current_stage'] = "La etapa actual es requerida."
    elif not isinstance(current_stage, str):
        errors['current_stage'] = "La etapa actual debe ser una cadena de texto."
    elif len(current_stage) > 50:
        errors['current_stage'] = "La etapa actual no puede exceder los 50 caracteres."
        
    # Validamos grape_variety_id y que exista en la DB
    grape_variety = None
    if not grape_variety_id:
        errors['grape_variety_id'] = "El ID de la variedad de uva es requerido."
    else:
        # Usamos un try-except para manejar el caso de UUID inválido
        try:
            grape_variety_id_uuid = str(grape_variety_id) # Asegurarse de que sea string 
            grape_variety = GrapeVariety.query.get(grape_variety_id_uuid)
            if not grape_variety:
                errors['grape_variety_id'] = "La variedad de uva especificada no existe."
        except ValueError:
            errors['grape_variety_id'] = "Formato de ID de variedad de uva inválido (debe ser un UUID válido)."

    #Validamos el end_date
    end_date = None
    if end_date_str:
        try:
            end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d').date()
        except ValueError:
            errors['end_date'] = "Formato de fecha de fin inválido (YYYY-MM-DD)."
    
    # Validar que end_date no sea anterior a start_date
    if start_date and end_date and end_date < start_date:
        errors['end_date'] = "La fecha de fin no puede ser anterior a la fecha de inicio."

    # Validamos la descripcion
    if description is not None and not isinstance(description, str):
        errors['description'] = "La descripción debe ser texto."
    elif isinstance(description, str) and len(description) > 500: # limitamos la longitud 
        errors['description'] = "La descripción es demasiado larga."


    if errors:
        return jsonify({"success": False, "message": "Datos de entrada inválidos.", "errors": errors}), 422

    try:
        new_process = VinificationProcess(
            start_date=start_date,
            end_date=end_date,
            current_stage=current_stage,
            description=description,
            grape_variety_id=str(grape_variety_id) # Aseguramos de que se guarda como string
        )
        db.session.add(new_process)
        db.session.commit()
        return jsonify({"success": True, "data": new_process.serialize()}), 201
    except Exception as e:
        db.session.rollback()
        # Captura de errores más específicos si se desea
        return jsonify({"success": False, "message": f"Error al crear el proceso de vinificación: {str(e)}"}), 500

@vinification_process_bp.route('/<uuid:process_id>', methods=['GET'])
def get_vinification_process_by_id(process_id):
    """
    Obtiene un proceso de vinificación específico por su ID.
    """
    process = VinificationProcess.query.get(str(process_id))
    if not process:
        return jsonify({"success": False, "message": "Proceso de Vinificación no encontrado."}), 404
    
    return jsonify({"success": True, "data": process.serialize()}), 200

@vinification_process_bp.route('/<uuid:process_id>', methods=['PUT'])
def update_vinification_process(process_id):
    """
    Actualiza completamente un proceso de vinificación existente por su ID.
    Requiere todos los campos aunque solo se modifique uno (PUT).
    """
    process = VinificationProcess.query.get(str(process_id))
    if not process:
        return jsonify({"success": False, "message": "Proceso de Vinificación no encontrado."}), 404

    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Datos JSON no proporcionados."}), 400

    errors = {}

    if 'start_date' in data:
        try:
            new_start_date = datetime.datetime.strptime(data['start_date'], '%Y-%m-%d').date()
            process.start_date = new_start_date
        except ValueError:
            errors['start_date'] = "Formato de fecha de inicio inválido (YYYY-MM-DD)."
    else:
        errors['start_date'] = "La fecha de inicio es requerida para la actualización."

    if 'end_date' in data:
        if data['end_date'] is None:
            process.end_date = None
        else:
            try:
                new_end_date = datetime.datetime.strptime(data['end_date'], '%Y-%m-%d').date()
                process.end_date = new_end_date
            except ValueError:
                errors['end_date'] = "Formato de fecha de fin inválido (YYYY-MM-DD)."
    # Si 'end_date' no está en data, su valor actual se mantiene.
    
    # Validamos que end_date no sea anterior a start_date (después de posibles actualizaciones)
    if process.start_date and process.end_date and process.end_date < process.start_date:
        errors['end_date'] = "La fecha de fin no puede ser anterior a la fecha de inicio."

    if 'current_stage' in data:
        if not isinstance(data['current_stage'], str):
            errors['current_stage'] = "La etapa actual debe ser una cadena de texto."
        elif len(data['current_stage']) > 50:
            errors['current_stage'] = "La etapa actual no puede exceder los 50 caracteres."
        else:
            process.current_stage = data['current_stage']
    else:
        errors['current_stage'] = "La etapa actual es requerida para la actualización (PUT)."

    if 'description' in data:
        if data['description'] is not None and not isinstance(data['description'], str):
            errors['description'] = "La descripción debe ser texto."
        elif isinstance(data['description'], str) and len(data['description']) > 500:
            errors['description'] = "La descripción es demasiado larga."
        else:
            process.description = data['description']
    # Si 'description' no está en data, su valor actual se mantiene.

    if 'grape_variety_id' in data:
        try:
            new_grape_variety_id = str(data['grape_variety_id'])
            grape_variety = GrapeVariety.query.get(new_grape_variety_id)
            if not grape_variety:
                errors['grape_variety_id'] = "La variedad de uva especificada no existe."
            else:
                process.grape_variety_id = new_grape_variety_id
        except ValueError:
            errors['grape_variety_id'] = "Formato de ID de variedad de uva inválido (debe ser un UUID válido)."
    else:
        errors['grape_variety_id'] = "El ID de la variedad de uva es requerido para la actualización (PUT)."

    if errors:
        return jsonify({"success": False, "message": "Datos de entrada inválidos.", "errors": errors}), 422

    try:
        db.session.commit()
        return jsonify({"success": True, "data": process.serialize()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": f"Error al actualizar el proceso de vinificación: {str(e)}"}), 500

@vinification_process_bp.route('/<uuid:process_id>', methods=['DELETE'])
def delete_vinification_process(process_id):
    """
    Elimina un proceso de vinificación específico por su ID.
    """
    process = VinificationProcess.query.get(str(process_id))
    if not process:
        return jsonify({"success": False, "message": "Proceso de Vinificación no encontrado."}), 404

    try:

        db.session.delete(process)
        db.session.commit()
        return jsonify({"success": True, "message": "Proceso de vinificación eliminado correctamente."}), 204 # 204 No Content
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": f"Error al eliminar el proceso de vinificación: {str(e)}"}), 500