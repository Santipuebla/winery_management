import uuid
from app import app
from models.db import db
from models.grape_variety import GrapeVariety
from models.vinification_process import VinificationProcess
from models.reception_stage import ReceptionStage
from models.fermentation_stage import FermentationStage
from models.bottling_stage import BottlingStage
from models.aging_stage import AgingStage

def populate_all():
    with app.app_context():
        print("Reiniciando tablas...")
        db.drop_all()
        db.create_all()

        # ---------- GRAPE VARIETIES ----------
        print(" Cargando variedades de uva...")
        v1 = GrapeVariety(id="aa7ac020-7dd8-4b43-acd0-b6312b62ef78", grape_name="Variedad 1", grape_origin="Origen 1", grape_image="imagen1.jpg", status=True)
        v2 = GrapeVariety(id="b465a22b-29f2-4a42-b0f9-4e12da14be2c", grape_name="Variedad 2", grape_origin="Origen 2", grape_image="imagen2.jpg", status=True)
        v3 = GrapeVariety(id="5c7f680b-c04a-4b8e-b6b8-61bb34943fc5", grape_name="Variedad 3", grape_origin="Origen 3", grape_image="imagen3.jpg", status=True)
        db.session.add_all([v1, v2, v3])

        # ---------- VINIFICATION PROCESSES ----------
        print(" Cargando procesos de vinificación...")
        p1 = VinificationProcess(id="0591318f-2628-4aaf-ba42-5b50a860885b", start_date="2024-04-01", end_date="2024-06-01", current_stage="aging", description="Proceso completo de prueba 1", grape_variety_id=v1.id)
        p2 = VinificationProcess(id="59a2a1d9-3431-4600-95fe-e796f29c045d", start_date="2024-04-02", end_date="2024-06-02", current_stage="aging", description="Proceso completo de prueba 2", grape_variety_id=v2.id)
        p3 = VinificationProcess(id="8bbd432c-e2da-4c8b-88c7-d0f111703bc6", start_date="2024-04-03", end_date="2024-06-03", current_stage="aging", description="Proceso completo de prueba 3", grape_variety_id=v3.id)
        db.session.add_all([p1, p2, p3])

        # ---------- RECEPTION STAGE ----------
        print(" Cargando recepciones...")
        db.session.add_all([
            ReceptionStage(id="b67faa08-ac5c-48e6-a907-ed0a2e5652f0", reception_date="2024-04-01", weight_kg=1100, brix_degrees=22.0, ph_value=3.2, temperature_celcius=17.5, observations="Recepción 1", vinification_process_id=p1.id),
            ReceptionStage(id="bbb63371-0497-4567-a8ac-5ffe95944199", reception_date="2024-04-02", weight_kg=1150, brix_degrees=23.0, ph_value=3.3, temperature_celcius=18.5, observations="Recepción 2", vinification_process_id=p2.id),
            ReceptionStage(id="b37556f0-c5d0-4dba-a93b-e203b9e20da7", reception_date="2024-04-03", weight_kg=1200, brix_degrees=24.0, ph_value=3.4, temperature_celcius=19.5, observations="Recepción 3", vinification_process_id=p3.id),
        ])

        # ---------- FERMENTATION STAGE ----------
        print("🧪 Cargando fermentaciones...")
        db.session.add_all([
            FermentationStage(id="80f521b3-c6dd-4752-a82f-dfda5f84eefd", fermentation_start_date="2024-04-02", fermentation_end_date="2024-04-11", density=1.01, total_acidity=6.0, temperature_celsius=21.0, observations="Fermentación 1", vinification_process_id=p1.id),
            FermentationStage(id="beed5738-3cfd-47a9-882a-28f20d98acf9", fermentation_start_date="2024-04-03", fermentation_end_date="2024-04-12", density=1.02, total_acidity=6.2, temperature_celsius=22.0, observations="Fermentación 2", vinification_process_id=p2.id),
            FermentationStage(id="5c18c8b4-4511-4283-9e07-9a26302ae81e", fermentation_start_date="2024-04-04", fermentation_end_date="2024-04-13", density=1.03, total_acidity=6.4, temperature_celsius=23.0, observations="Fermentación 3", vinification_process_id=p3.id),
        ])

        # ---------- BOTTLING STAGE ----------
        print("🍾 Cargando embotellados...")
        db.session.add_all([
            BottlingStage(id="b4b92ff1-484b-4b16-816f-8b527da5aaf8", bottling_date="2024-05-11", bottles_quantity=900, bottles_format="750ml", bottling_lot_number="LoteB1", observations="Embotellado 1", vinification_process_id=p1.id),
            BottlingStage(id="3b459560-53a1-4ea2-8268-8dbd0d3f5571", bottling_date="2024-05-12", bottles_quantity=950, bottles_format="750ml", bottling_lot_number="LoteB2", observations="Embotellado 2", vinification_process_id=p2.id),
            BottlingStage(id="820a106d-df68-455c-9da0-87f9c03d5782", bottling_date="2024-05-13", bottles_quantity=1000, bottles_format="750ml", bottling_lot_number="LoteB3", observations="Embotellado 3", vinification_process_id=p3.id),
        ])

        # ---------- AGING STAGE ----------
        print(" Cargando crianza...")
        db.session.add_all([
            AgingStage(id="8475e1b6-d942-4361-94c4-6c98746a6e17", aging_start_date="2024-05-11", aging_end_date="2024-06-01", vessel_type="Barrica 1", volume_liters=200.0, vessel_identifier="AG-001", location="Sala 1", observations="Notas 1", vinification_process_id=p1.id),
            AgingStage(id="45471353-ca31-4a02-b5d5-9cb956d06e26", aging_start_date="2024-05-12", aging_end_date="2024-06-02", vessel_type="Barrica 2", volume_liters=225.0, vessel_identifier="AG-002", location="Sala 2", observations="Notas 2", vinification_process_id=p2.id),
            AgingStage(id="c58c21d0-220e-4453-9e1c-f5bb3f4e825e", aging_start_date="2024-05-13", aging_end_date="2024-06-03", vessel_type="Barrica 3", volume_liters=250.0, vessel_identifier="AG-003", location="Sala 3", observations="Notas 3", vinification_process_id=p3.id),
        ])

        # ---------- COMMIT ----------
        db.session.commit()
        print(" ¡Base de datos inicializada con éxito!")

if __name__ == '__main__':
    populate_all()