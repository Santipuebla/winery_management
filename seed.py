import os
import json
from datetime import datetime, timedelta
import sys
import uuid

# Asegura que Flask y SQLAlchemy estén disponibles
try:
    from app import app
    from models.db import db
    from models.grape_variety import GrapeVariety
    from models.vinification_process import VinificationProcess
    from models.reception_stage import ReceptionStage
    from models.fermentation_stage import FermentationStage
    from models.aging_stage import AgingStage
    from models.bottling_stage import BottlingStage
except ImportError as e:
    print(f"ImportError: {e}")
    sys.exit(1)

# Datos de ejemplo generados directamente sin archivos JSON
data_grape_varieties = [
    {
        "id": str(uuid.uuid4()),
        "grape_name": "Cabernet Sauvignon",
        "grape_origin": "Francia",
        "grape_image": None,
        "status": True
    },
    {
        "id": str(uuid.uuid4()),
        "grape_name": "Malbec",
        "grape_origin": "Argentina",
        "grape_image": None,
        "status": True
    },
    {
        "id": str(uuid.uuid4()),
        "grape_name": "Merlot",
        "grape_origin": "Italia",
        "grape_image": None,
        "status": True
    },
]

data_vinification_processes = [
    {
        "id": str(uuid.uuid4()),
        "start_date_offset_days": 30,
        "end_date_offset_days": 10,
        "current_stage": "Fermentación",
        "description": "Proceso inicial",
        "variety_id_ref": None  # Asignado luego
    },
    {
        "id": str(uuid.uuid4()),
        "start_date_offset_days": 60,
        "end_date_offset_days": 30,
        "current_stage": "Crianza",
        "description": "Proceso de maduración",
        "variety_id_ref": None
    },
    {
        "id": str(uuid.uuid4()),
        "start_date_offset_days": 90,
        "end_date_offset_days": 60,
        "current_stage": "Embotellado",
        "description": "Proceso general de embotellado de varios vinos.",
        "variety_id_ref": None
    },
]

# Asignar variety_id_ref desde data_grape_varieties
for i, process in enumerate(data_vinification_processes):
    process["variety_id_ref"] = data_grape_varieties[i % len(data_grape_varieties)]["id"]


def populate_all():
    with app.app_context():
        db.create_all()
        print("Base de datos inicializada.")

        db.session.query(BottlingStage).delete()
        db.session.query(AgingStage).delete()
        db.session.query(FermentationStage).delete()
        db.session.query(ReceptionStage).delete()
        db.session.query(VinificationProcess).delete()
        db.session.query(GrapeVariety).delete()
        db.session.commit()

        grape_varieties_map = {}
        for item in data_grape_varieties:
            variety = GrapeVariety(
                id=uuid.UUID(item["id"]),
                grape_name=item["grape_name"],
                grape_origin=item["grape_origin"],
                grape_image=item["grape_image"],
                status=item["status"]
            )
            db.session.add(variety)
            grape_varieties_map[item["id"]] = variety

        db.session.commit()
        print("Variedades de uva cargadas.")

        for item in data_vinification_processes:
            start_date = datetime.now() - timedelta(days=item['start_date_offset_days'])
            end_date = datetime.now() - timedelta(days=item['end_date_offset_days'])
            process = VinificationProcess(
                id=uuid.UUID(item["id"]),
                start_date=start_date,
                end_date=end_date,
                current_stage=item["current_stage"],
                description=item["description"],
                variety_id=item["variety_id_ref"]
            )
            db.session.add(process)

        db.session.commit()
        print("Procesos de vinificación cargados.")

        print("\n¡Seeding completado exitosamente!")

        for p in data_vinification_processes:
            if p['current_stage'] == "Embotellado" and p['description'] == "Proceso general de embotellado de varios vinos.":
                print("----------------------------------------------------------------------------------")
                print(f"UUID de proceso embotellado general: {p['id']}")
                print("----------------------------------------------------------------------------------")

if __name__ == '__main__':
    populate_all()
