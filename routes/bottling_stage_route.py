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

@bottling.route('/', methods=['GET'])
def get_bottling_stages():
    bottling_list = BottlingStage.query.all()
    context = {"bottlings": bottling_list}  # Cambié 'receptions' por 'bottlings'
    return render_template('embotellamiento/embotellamiento.html', **context)



@bottling.route("/new", methods=["GET", "POST"])
@bottling.route("/new", methods=["GET", "POST"])
def add_bottling_stage():
    vinification_process_id = request.args.get("vinification_process_id")

    # Traer todos los procesos para el select
    vinification_processes = VinificationProcess.query.all()

    if request.method == "POST":
        vinification_process_id = request.form.get("vinification_process_id")
        if not vinification_process_id:
            flash("No se recibió el ID del proceso de vinificación.", "error")
            return redirect(request.url)

        existing_stage = BottlingStage.query.filter_by(vinification_process_id=vinification_process_id).first()
        if existing_stage:
            flash("Ya existe una etapa de embotellado para este proceso de vinificación.", "error")
            return redirect(url_for("bottling.add_bottling_stage") + f"?vinification_process_id={vinification_process_id}")

        new_stage = BottlingStage(
            bottling_date=datetime.strptime(request.form["bottling_date"], "%Y-%m-%d"),
            bottles_quantity=int(request.form["bottles_quantity"]),
            bottles_format=request.form["bottles_format"],
            bottling_lot_number=request.form["bottling_lot_number"],
            observations=request.form["observations"],
            vinification_process_id=vinification_process_id
        )

        db.session.add(new_stage)
        db.session.commit()
        flash("Etapa de embotellado agregada correctamente.", "success")
        return redirect(url_for("bottling.get_bottling_stages"))

    return render_template(
        "embotellamiento/add_embotellamiento.html",
        vinification_process_id=vinification_process_id,
        vinification_processes=vinification_processes  # <-- PASAR lista de procesos aquí
    )

    



@bottling.route("/edit/<string:id>", methods=["GET", "POST"])
def edit_bottling_stage(id):
    stage = BottlingStage.query.get_or_404(id)

    if request.method == "POST":
        vinification_process_id = request.form["vinification_process_id"]

        existing_stage = BottlingStage.query.filter(
            BottlingStage.vinification_process_id == vinification_process_id,
            BottlingStage.id != id
        ).first()
        if existing_stage:
            flash("Ya existe otra etapa de embotellado para este proceso de vinificación.", "error")
            return redirect(url_for("bottling.edit_bottling_stage", id=id))

        stage.bottling_date = datetime.strptime(request.form["bottling_date"], "%Y-%m-%d")
        stage.bottles_quantity = int(request.form["bottles_quantity"])
        stage.bottles_format = request.form["bottles_format"]
        stage.bottling_lot_number = request.form["bottling_lot_number"]
        stage.observations = request.form["observations"]
        stage.vinification_process_id = vinification_process_id

        db.session.commit()
        flash("Etapa de embotellado actualizada exitosamente.", "success")
        return redirect(url_for("bottling.get_bottling_stages"))

    return render_template("embotellamiento/edit_embotellamiento.html", stage=stage)


@bottling.route("/delete/<string:id>", methods=["POST"])
def delete_bottling_stage(id):
    stage = BottlingStage.query.get_or_404(id)

    db.session.delete(stage)
    db.session.commit()

    flash("Etapa de embotellado eliminada del sistema.", "success")
    return redirect(url_for("bottling.get_bottling_stages"))