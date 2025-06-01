from models.db import db
from flask import Blueprint, jsonify, request, render_template
from models.grape_variety import GrapeVariety 
from models.vinification_process import VinificationProcess
from models.fermentation_stage import FermentationStage

import datetime

fermentation = Blueprint('fermentation', __name__, url_prefix='/fermentation')


UPLOAD_FOLDER = 'static/images' 
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@fermentation.route('/get_all_fermetations', methods=['GET'])
def get_all_fermetations():
    processes = FermentationStage.query.all()
    context = {"fermentations": processes}
    return render_template("fermentation/fermentation.html", **context)


@fermentation.route('/<uuid:process_id>/fermentation_stage', methods=['GET'])
def get_fermentation_stage(process_id):
    vinification_process = FermentationStage.query.get(str(process_id))
    if not vinification_process:
        return jsonify({"success": False, "message": "Proceso de Vinificación no encontrado."}), 404

    fermentation_stage = vinification_process.fermentation_stage
    if not fermentation_stage:
        return jsonify({"success": False, "message": "Etapa de fermentación para este proceso no encontrada."}), 404
    
    return jsonify({"success": True, "data": fermentation_stage.serialize()}), 200

from flask import redirect, url_for, flash

@fermentation.route("/add", methods=["GET", "POST"])
def add_fermentation_stage():
    if request.method == "POST":
        try:
            fermentation_start_date = datetime.datetime.strptime(request.form.get("fermentation_start_date"), "%Y-%m-%d").date()
            fermentation_end_date = datetime.datetime.strptime(request.form.get("fermentation_end_date"), "%Y-%m-%d").date()
            density = float(request.form.get("density"))
            total_acidity = float(request.form.get("total_acidity"))
            temperature_celsius = float(request.form.get("temperature_celsius"))
            observations = request.form.get("observations")
            vinification_process_id = request.form.get("vinification_process_id")

            new_fermentation = FermentationStage(
                fermentation_start_date=fermentation_start_date,
                fermentation_end_date=fermentation_end_date,
                density=density,
                total_acidity=total_acidity,
                temperature_celsius=temperature_celsius,
                observations=observations,
                vinification_process_id=vinification_process_id
            )
            db.session.add(new_fermentation)
            db.session.commit()
            flash("Fermentación registrada con éxito", "success")
            return redirect(url_for("fermentation.get_all_fermentations"))
        except Exception as e:
            db.session.rollback()
            flash(f"Error al registrar la fermentación: {str(e)}", "danger")
            return redirect(url_for("fermentation.add_fermentation_stage"))

    vinification_processes = VinificationProcess.query.all()
    return render_template("fermentation/add_fermentation.html", vinification_processes=vinification_processes)


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

@fermentation.route('/edit/<uuid:id>', methods=['GET', 'POST'])
def edit_fermentation_stage(id):
    fermentation = FermentationStage.query.get_or_404(str(id))
    vinification_processes = VinificationProcess.query.all()

    if request.method == 'POST':
        try:
            fermentation.fermentation_start_date = datetime.datetime.strptime(
                request.form['fermentation_start_date'], '%Y-%m-%d').date()

            fermentation_end_date_str = request.form.get('fermentation_end_date')
            fermentation.fermentation_end_date = (
                datetime.datetime.strptime(fermentation_end_date_str, '%Y-%m-%d').date()
                if fermentation_end_date_str else None
            )

            fermentation.density = float(request.form['density'])
            fermentation.total_acidity = float(request.form['total_acidity'])
            fermentation.temperature_celsius = float(request.form['temperature_celsius'])
            fermentation.observations = request.form.get('observations')
            fermentation.vinification_process_id = request.form['vinification_process_id']

            db.session.commit()
            return redirect(url_for('fermentation.get_all_fermetations'))

        except Exception as e:
            db.session.rollback()
            return f"Error al actualizar: {e}", 500

    return render_template(
        "fermentation/edit_fermentation.html",
        fermentation=fermentation,
        vinification_processes=vinification_processes
    )


@fermentation.route('/delete/<uuid:id>', methods=['POST'])
def delete_fermentation_stage(id):
    fermentation = FermentationStage.query.get_or_404(str(id))
    try:
        db.session.delete(fermentation)
        db.session.commit()
        return redirect(url_for('fermentation.get_all_fermetations'))  # corregido aquí
    except Exception as e:
        db.session.rollback()
        return f"Error al eliminar: {e}", 500

