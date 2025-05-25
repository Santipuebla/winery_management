from sqlalchemy.exc import IntegrityError
from flask import Blueprint, flash, redirect, render_template, request, url_for
from models.db import db
from models.reception_stage import ReceptionStage
from datetime import datetime

reception = Blueprint("reception", __name__, url_prefix="/reception")

UPLOAD_FOLDER = "static/images"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

def allowed_file(filename): 
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@reception.route("/new", methods=["GET", "POST"])
def add_reception_stage():
    if request.method == "POST":
        vinification_process_id = request.form['vinification_process_id']

        existing_stage = ReceptionStage.query.filter_by(vinification_process_id=vinification_process_id).first()
        if existing_stage:
            flash("Ya existe una etapa de recepción para este proceso de vinificación.", "error")
            return redirect(url_for("reception.add_reception_stage"))

        new_stage = ReceptionStage(
            reception_date=datetime.strptime(request.form["reception_date"], "%Y-%m-%d"),
            weight_kg=float(request.form["weight_kg"]),
            brix_degrees=float(request.form["brix_degrees"]),
            ph_value=float(request.form["ph_value"]),
            temperature_celcius=float(request.form["temperature_celcius"]),
            observations=request.form["observations"],
            vinification_process_id=vinification_process_id
        )

        db.session.add(new_stage)
        db.session.commit()
        flash("Se recepcionó correctamente.", "success")
        return redirect(url_for("reception.get_reception_stages"))  

    return render_template("reception/new.html")


@reception.route('/edit/<string:id>', methods=['GET', 'POST'])
def edit_reception_stage(id):
    stage = ReceptionStage.query.get_or_404(id)

    if request.method == "POST":
        vinification_process_id = request.form["vinification_process_id"]

        existing_stage = ReceptionStage.query.filter(
            ReceptionStage.vinification_process_id == vinification_process_id,
            ReceptionStage.id != id
        ).first()
        if existing_stage:
            flash("Ya existe otra etapa de recepción para este proceso de vinificación.", "error")
            return redirect(url_for("reception.edit_reception_stage", id=id))

        stage.reception_date = datetime.strptime(request.form["reception_date"], "%Y-%m-%d")
        stage.weight_kg = float(request.form["weight_kg"])
        stage.brix_degrees = float(request.form["brix_degrees"])
        stage.ph_value = float(request.form["ph_value"])
        stage.temperature_celcius = float(request.form["temperature_celcius"])
        stage.observations = request.form["observations"]
        stage.vinification_process_id = vinification_process_id

        db.session.commit()
        flash("Datos actualizados correctamente.", "success")
        return redirect(url_for("reception.get_reception_stages"))  

    return render_template("reception/edit.html", stage=stage)


@reception.route('/delete/<string:id>', methods=['POST'])
def delete_reception_stage(id):
    stage = ReceptionStage.query.get_or_404(id)

    db.session.delete(stage)
    db.session.commit()
    flash("Esta etapa de recepción se eliminó correctamente.", "success")
    return redirect(url_for("reception.get_reception_stages"))  


@reception.route('/', methods=['GET'])
def get_reception_stages():
    stages = ReceptionStage.query.all()
    return render_template('reception/list.html', stages=stages)
