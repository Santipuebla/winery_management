from sqlalchemy.exc import IntegrityError
from flask import Blueprint, flash, redirect, render_template, request, url_for
from models.db import db
from models.aging_stage import AgingStage  
from datetime import datetime

aging = Blueprint("aging", _name_, url_prefix="/aging")


@aging.route("/new", methods=["GET", "POST"])
def add_aging_stage():
    if request.method == "POST":
        vinification_process_id = request.form["vinification_process_id"]

        existing_stage = AgingStage.query.filter_by(vinification_process_id=vinification_process_id).first()
        if existing_stage:
            flash("Ya existe una etapa de crianza para este proceso de vinificación.", "error")
            return redirect(url_for("aging.add_aging_stage"))

        new_stage = AgingStage(
            aging_start_date=datetime.strptime(request.form["aging_start_date"], "%Y-%m-%d"),
            aging_end_date=datetime.strptime(request.form["aging_end_date"], "%Y-%m-%d"),
            vessel_type=request.form["vessel_type"],
            volume_liters=float(request.form["volume_liters"]),
            vessel_identifier=request.form["vessel_identifier"],
            location=request.form["location"],
            observations=request.form["observations"],
            vinification_process_id=vinification_process_id
        )

        db.session.add(new_stage)
        db.session.commit()
        flash("Etapa de crianza agregada correctamente.", "success")
        return redirect(url_for("aging.get_aging_stages"))

    return render_template("aging/new.html")


@aging.route("/edit/<string:id>", methods=["GET", "POST"])
def edit_aging_stage(id):
    stage = AgingStage.query.get_or_404(id)

    if request.method == "POST":
        vinification_process_id = request.form["vinification_process_id"]

        existing_stage = AgingStage.query.filter(
            AgingStage.vinification_process_id == vinification_process_id,
            AgingStage.id != id
        ).first()

        if existing_stage:
            flash("Ya existe otra etapa de crianza para este proceso de vinificación.", "error")
            return redirect(url_for("aging.edit_aging_stage", id=id))

        stage.aging_start_date = datetime.strptime(request.form["aging_start_date"], "%Y-%m-%d")
        stage.aging_end_date = datetime.strptime(request.form["aging_end_date"], "%Y-%m-%d")
        stage.vessel_type = request.form["vessel_type"]
        stage.volume_liters = float(request.form["volume_liters"])
        stage.vessel_identifier = request.form["vessel_identifier"]
        stage.location = request.form["location"]
        stage.observations = request.form["observations"]
        stage.vinification_process_id = vinification_process_id

        db.session.commit()
        flash("Etapa de crianza actualizada correctamente.", "success")
        return redirect(url_for("aging.get_aging_stages"))

    return render_template("aging/edit.html", stage=stage)


@aging.route("/delete/<string:id>", methods=["POST"])
def delete_aging_stage(id):
    stage = AgingStage.query.get_or_404(id)

    db.session.delete(stage)
    db.session.commit()
    flash("Etapa de crianza eliminada correctamente.", "success")
    return redirect(url_for("aging.get_aging_stages"))


@aging.route("/", methods=["GET"])
def get_aging_stages():
    filter_vessel = request.args.get("vessel_type")
    filter_location = request.args.get("location")

    query = AgingStage.query

    if filter_vessel:
        query = query.filter(AgingStage.vessel_type == filter_vessel)
    if filter_location:
        query = query.filter(AgingStage.location == filter_location)

    stages = query.all()

    return render_template("aging/list.html", stages=stages,
                        current_filter_vessel=filter_vessel,
                        current_filter_location=filter_location)