from sqlalchemy.exc import InternalError
from flask import Blueprint, flash, redirect, render_template, request, url_for
from models.db import db
from models.bottling_stage import BottlingStage
from datetime import datetime
from models.vinification_process import VinificationProcess

bottling = Blueprint("bottling", __name__, url_prefix="/bottling")

UPLOAD_FOLDER = "static/images"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS 

@bottling.route("/test")
def test_bottlings():
    count = BottlingStage.query.count()
    return f"Hay {count} embotellamientos en la base."

@bottling.route("/", methods=["GET"])
def embotellamiento_page():
    # Esta ruta solo lista los embotellamientos para la tabla.
    embotellamientos = BottlingStage.query.all()
    return render_template("embotellamiento/embotellamiento.html", 
                           embotellamientos=embotellamientos)

@bottling.route("/new", methods=["GET", "POST"])
def add_bottling_stage():
    # Diccionario para almacenar errores de validación (manuales)
    errors = {}
    
    # Necesitamos todos los procesos de vinificación para el select en el formulario
    vinification_processes = VinificationProcess.query.all()

    if request.method == "POST":
        # Recolectar datos directamente de request.form
        bottling_date_str = request.form.get("bottling_date")
        bottles_quantity_str = request.form.get("bottles_quantity")
        bottles_format = request.form.get("bottles_format")
        bottling_lot_number = request.form.get("bottling_lot_number")
        observations = request.form.get("observations")
        vinification_process_id = request.form.get("vinification_process_id")

        # --- VALIDACIÓN MANUAL ---
        if not bottling_date_str:
            errors['bottling_date'] = "La fecha de embotellado es requerida."
        else:
            try:
                bottling_date = datetime.strptime(bottling_date_str, "%Y-%m-%d")
            except ValueError:
                errors['bottling_date'] = "Formato de fecha inválido. Use AAAA-MM-DD."

        if not bottles_quantity_str:
            errors['bottles_quantity'] = "La cantidad de botellas es requerida."
        else:
            try:
                bottles_quantity = int(bottles_quantity_str)
                if bottles_quantity <= 0:
                    errors['bottles_quantity'] = "La cantidad de botellas debe ser un número positivo."
            except ValueError:
                errors['bottles_quantity'] = "La cantidad de botellas debe ser un número entero."

        if not bottles_format:
            errors['bottles_format'] = "El formato de botellas es requerido."
        
        if not bottling_lot_number:
            errors['bottling_lot_number'] = "El número de lote es requerido."

        if not vinification_process_id:
            errors['vinification_process_id'] = "El proceso de vinificación es requerido."
        else:
            # Verificar si el vinification_process_id existe
            process_exists = VinificationProcess.query.get(vinification_process_id)
            if not process_exists:
                errors['vinification_process_id'] = "El proceso de vinificación seleccionado no es válido."
            else:
                # Verificar si ya existe una etapa para ese proceso (Lógica que ya tenías)
                existing_stage = BottlingStage.query.filter_by(vinification_process_id=vinification_process_id).first()
                if existing_stage:
                    errors['vinification_process_id'] = "Ya existe una etapa de embotellado para este proceso de vinificación."

        # Si no hay errores, proceder a guardar
        if not errors:
            try:
                new_stage = BottlingStage(
                    bottling_date=bottling_date, # Usar la fecha ya convertida
                    bottles_quantity=bottles_quantity, # Usar la cantidad ya convertida
                    bottles_format=bottles_format,
                    bottling_lot_number=bottling_lot_number,
                    observations=observations,
                    vinification_process_id=vinification_process_id
                )

                db.session.add(new_stage)
                db.session.commit()
                flash("Etapa de embotellado agregada correctamente.", "success")
                return redirect(url_for("bottling.embotellamiento_page"))
            except InternalError as e:
                db.session.rollback()
                flash(f"Error interno al agregar la etapa: {e}", "error")
            except Exception as e:
                db.session.rollback()
                flash(f"Ocurrió un error inesperado: {e}", "error")
        else:
            # Si hay errores, flash un mensaje general y se re-renderizará el formulario con los errores específicos
            flash("Por favor, corrige los errores en el formulario.", "error")

    # Para GET o si hay errores en POST, renderizar el formulario
    return render_template("embotellamiento/add_embotellamiento.html", 
                           vinification_processes=vinification_processes,
                           errors=errors, # Pasamos los errores a la plantilla
                           # Para precargar los valores si hubo errores en el POST
                           # Es crucial devolver los valores del POST para que el usuario no pierda lo que escribió
                           data=request.form if request.method == "POST" else {}
                          )


@bottling.route("/edit/<string:id>", methods=["GET", "POST"])
def edit_bottling_stage(id):
    stage = BottlingStage.query.get_or_404(id)
    errors = {}
    vinification_processes = VinificationProcess.query.all()

    if request.method == "POST":
        bottling_date_str = request.form.get("bottling_date")
        bottles_quantity_str = request.form.get("bottles_quantity")
        bottles_format = request.form.get("bottles_format")
        bottling_lot_number = request.form.get("bottling_lot_number")
        observations = request.form.get("observations")
        vinification_process_id = request.form.get("vinification_process_id")

        # --- VALIDACIÓN MANUAL ---
        if not bottling_date_str:
            errors['bottling_date'] = "La fecha de embotellado es requerida."
        else:
            try:
                bottling_date = datetime.strptime(bottling_date_str, "%Y-%m-%d")
            except ValueError:
                errors['bottling_date'] = "Formato de fecha inválido. Use AAAA-MM-DD."

        if not bottles_quantity_str:
            errors['bottles_quantity'] = "La cantidad de botellas es requerida."
        else:
            try:
                bottles_quantity = int(bottles_quantity_str)
                if bottles_quantity <= 0:
                    errors['bottles_quantity'] = "La cantidad de botellas debe ser un número positivo."
            except ValueError:
                errors['bottles_quantity'] = "La cantidad de botellas debe ser un número entero."

        if not bottles_format:
            errors['bottles_format'] = "El formato de botellas es requerido."
        
        if not bottling_lot_number:
            errors['bottling_lot_number'] = "El número de lote es requerido."

        if not vinification_process_id:
            errors['vinification_process_id'] = "El proceso de vinificación es requerido."
        else:
            process_exists = VinificationProcess.query.get(vinification_process_id)
            if not process_exists:
                errors['vinification_process_id'] = "El proceso de vinificación seleccionado no es válido."
            else:
                existing_stage = BottlingStage.query.filter(
                    BottlingStage.vinification_process_id == vinification_process_id,
                    BottlingStage.id != id # Excluir la etapa actual al verificar unicidad
                ).first()
                if existing_stage:
                    errors['vinification_process_id'] = "Ya existe otra etapa de embotellado para este proceso de vinificación."
        
        if not errors:
            try:
                stage.bottling_date = bottling_date
                stage.bottles_quantity = bottles_quantity
                stage.bottles_format = bottles_format
                stage.bottling_lot_number = bottling_lot_number
                stage.observations = observations
                stage.vinification_process_id = vinification_process_id

                db.session.commit()
                flash("Etapa de embotellado actualizada exitosamente.", "success")
                return redirect(url_for("bottling.embotellamiento_page")) # Redirige a la página de lista
            except InternalError as e:
                db.session.rollback()
                flash(f"Error interno al actualizar la etapa: {e}", "error")
            except Exception as e:
                db.session.rollback()
                flash(f"Ocurrió un error inesperado al actualizar: {e}", "error")
        else:
            flash("Por favor, corrige los errores en el formulario.", "error")

    # Para GET o si hay errores en POST
    # Si es GET, precargamos el formulario con los datos de 'stage'.
    # Si es POST con errores, precargamos con los datos enviados en 'request.form'.
    return render_template("embotellamiento/edit_embotellamiento.html", 
                           stage=stage,
                           vinification_processes=vinification_processes,
                           errors=errors, # Pasamos los errores a la plantilla
                           # Si es GET, los datos serán los de 'stage'. Si es POST con errores, serán los de request.form
                           data=request.form if request.method == "POST" else {
                               'bottling_date': stage.bottling_date.strftime('%Y-%m-%d') if stage.bottling_date else '',
                               'bottles_quantity': stage.bottles_quantity,
                               'bottles_format': stage.bottles_format,
                               'bottling_lot_number': stage.bottling_lot_number,
                               'observations': stage.observations,
                               'vinification_process_id': str(stage.vinification_process_id) # Convertir a string para el select
                           }
                          )


@bottling.route("/delete/<string:id>", methods=["POST"])
def delete_bottling_stage(id):
    stage = BottlingStage.query.get_or_404(id)
    try:
        db.session.delete(stage)
        db.session.commit()
        flash("Etapa de embotellado eliminada del sistema.", "success")
    except InternalError as e:
        db.session.rollback()
        flash(f"Error interno al eliminar la etapa: {e}", "error")
    except Exception as e:
        db.session.rollback()
        flash(f"Ocurrió un error inesperado al eliminar: {e}", "error")
    return redirect(url_for("bottling.embotellamiento_page"))



