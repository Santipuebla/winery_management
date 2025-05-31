import os
import json
from datetime import datetime, timedelta
import sys
import uuid

# Asegúrate de que tu instancia de Flask 'app' esté disponible.
try:
    from app import app 
except ImportError:
    print("Error: No se pudo importar 'app' desde 'app.py'.")
    print("Asegúrate de que 'app.py' esté en la misma carpeta que 'seed.py' o ajusta la ruta de importación.")
    sys.exit(1)

# Tu instancia de SQLAlchemy
try:
    from models.db import db 
except ImportError:
    print("Error: No se pudo importar 'db' desde 'models.db'.")
    print("Asegúrate de que 'models/db.py' exista y 'db' esté definido allí.")
    sys.exit(1)

# ====================================================================
# IMPORTA TODOS TUS MODELOS DE LA CARPETA 'models/'
# Asegúrate de que los nombres de clase coincidan con tus archivos y tu esquema de base de datos.
# ====================================================================
try:
    from models.grape_variety import GrapeVariety # Nuevo
    from models.vinification_process import VinificationProcess
    from models.reception_stage import ReceptionStage
    from models.fermentation_stage import FermentationStage
    from models.aging_stage import AgingStage
    from models.bottling_stage import BottlingStage
except ImportError as e:
    print(f"Error al importar un modelo: {e}")
    print("Asegúrate de que todos tus archivos de modelo existan en la carpeta 'models/' y los nombres de las clases sean correctos.")
    sys.exit(1)


# Directorio donde se encuentran los archivos JSON de datos
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')


def load_json_data(filename):
    """Carga datos de un archivo JSON específico."""
    filepath = os.path.join(DATA_DIR, filename)
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: El archivo '{filepath}' no se encontró.")
        return []
    except json.JSONDecodeError:
        print(f"Error: El archivo '{filepath}' no es un JSON válido.")
        return []


def populate_grape_varieties(data):
    """Popula la tabla GrapeVariety y retorna un mapa de IDs."""
    created = 0
    grape_varieties_map = {}
    print("\n--- Populando GrapeVariety ---")
    for item in data:
        variety = GrapeVariety(
            grape_name=item['grape_name'],
            grape_origin=item['grape_origin'],
            grape_image=item.get('grape_image'),
            status=item.get('status', True)
        )
        # Asignar el ID del JSON después de la creación del objeto
        variety.id = uuid.UUID(item['id'])
        
        db.session.add(variety)
        grape_varieties_map[str(variety.id)] = variety
        print(f"  - Creada GrapeVariety: {item['grape_name']} (ID: {variety.id})")
        created += 1
    return created, grape_varieties_map


def populate_vinification_processes(data, grape_varieties_map):
    """Popula la tabla VinificationProcess y retorna un mapa de IDs."""
    created = 0
    vinification_processes_map = {} 
    print("\n--- Populando VinificationProcess ---")
    for item in data:
        start_date = datetime.now() - timedelta(days=item['start_date_offset_days'])
        end_date = datetime.now() - timedelta(days=item['end_date_offset_days'])
        
        variety_id = item.get('variety_id_ref') # Usar 'variety_id_ref' para el JSON
        if variety_id not in grape_varieties_map:
            print(f"  - Advertencia: GrapeVariety con ID '{variety_id}' no encontrado para VinificationProcess '{item['id']}'. Saltando.")
            continue

        process = VinificationProcess(
            start_date=start_date,
            end_date=end_date,
            current_stage=item['current_stage'], # Cambiado a 'current_stage'
            description=item.get('description'), # Añadido 'description'
            variety_id=variety_id
        )
        process.id = uuid.UUID(item['id']) 

        db.session.add(process)
        vinification_processes_map[str(process.id)] = process 
        print(f"  - Creado VinificationProcess: {item['current_stage']} (ID: {process.id})")
        created += 1
    return created, vinification_processes_map

def populate_reception_stages(data, vinification_processes_map):
    """Popula la tabla ReceptionStage."""
    created = 0
    print("\n--- Populando ReceptionStage ---")
    for item in data:
        reception_date = datetime.now() - timedelta(days=item['reception_date_offset_days'])
        
        process_id = item.get('vinification_process_id_ref')
        if process_id not in vinification_processes_map:
            print(f"  - Advertencia: VinificationProcess con ID '{process_id}' no encontrado para ReceptionStage '{item['id']}'. Saltando.")
            continue

        stage = ReceptionStage(
            reception_date=reception_date,
            weight_kg=item['weight_kg'], # Cambiado
            brix_degrees=item['brix_degrees'], # Nuevo
            ph_value=item['ph_value'], # Nuevo
            temperature_celcius=item['temperature_celcius'], # Nuevo
            observations=item.get('observations'),
            vinification_process_id=process_id 
        )
        stage.id = uuid.UUID(item['id'])

        db.session.add(stage)
        print(f"  - Creada ReceptionStage (ID: {stage.id}) para {vinification_processes_map[process_id].current_stage}")
        created += 1
    return created

def populate_fermentation_stages(data, vinification_processes_map):
    """Popula la tabla FermentationStage."""
    created = 0
    print("\n--- Populando FermentationStage ---")
    for item in data:
        fermentation_start_date = datetime.now() - timedelta(days=item['fermentation_start_date_offset_days']) # Cambiado
        fermentation_end_date = datetime.now() - timedelta(days=item['fermentation_end_date_offset_days']) # Cambiado
        
        process_id = item.get('vinification_process_id_ref')
        if process_id not in vinification_processes_map:
            print(f"  - Advertencia: VinificationProcess con ID '{process_id}' no encontrado para FermentationStage '{item['id']}'. Saltando.")
            continue

        stage = FermentationStage(
            fermentation_start_date=fermentation_start_date,
            fermentation_end_date=fermentation_end_date,
            density=item['density'], # Nuevo
            total_acidity=item['total_acidity'], # Nuevo
            temperature_celsius=item['temperature_celsius'],
            observations=item.get('observations'),
            vinification_process_id=process_id
        )
        stage.id = uuid.UUID(item['id'])

        db.session.add(stage)
        print(f"  - Creada FermentationStage (ID: {stage.id}) para {vinification_processes_map[process_id].current_stage}")
        created += 1
    return created

def populate_aging_stages(data, vinification_processes_map):
    """Popula la tabla AgingStage."""
    created = 0
    print("\n--- Populando AgingStage ---")
    for item in data:
        aging_start_date = datetime.now() - timedelta(days=item['aging_start_date_offset_days']) # Cambiado
        aging_end_date = datetime.now() - timedelta(days=item['aging_end_date_offset_days']) # Cambiado
        
        process_id = item.get('vinification_process_id_ref')
        if process_id not in vinification_processes_map:
            print(f"  - Advertencia: VinificationProcess con ID '{process_id}' no encontrado para AgingStage '{item['id']}'. Saltando.")
            continue

        stage = AgingStage(
            aging_start_date=aging_start_date,
            aging_end_date=aging_end_date,
            vessel_type=item['vessel_type'], # Cambiado
            volume_liters=item['volume_liters'], # Nuevo
            vessel_identifier=item['vessel_identifier'], # Nuevo
            location=item['location'], # Nuevo
            observations=item.get('observations'),
            vinification_process_id=process_id
        )
        stage.id = uuid.UUID(item['id'])

        db.session.add(stage)
        print(f"  - Creada AgingStage (ID: {stage.id}) para {vinification_processes_map[process_id].current_stage}")
        created += 1
    return created

def populate_bottling_stages(data, vinification_processes_map):
    """Popula la tabla BottlingStage."""
    created = 0
    print("\n--- Populando BottlingStage ---")
    for item in data:
        bottling_date = datetime.now() - timedelta(days=item['bottling_date_offset_days'])
        
        process_id = item.get('vinification_process_id_ref')
        if process_id not in vinification_processes_map:
            print(f"  - Advertencia: VinificationProcess con ID '{process_id}' no encontrado para BottlingStage '{item['id']}'. Saltando.")
            continue

        stage = BottlingStage(
            bottling_date=bottling_date,
            bottles_quantity=item['bottles_quantity'],
            bottles_format=item['bottles_format'],
            bottling_lot_number=item['bottling_lot_number'],
            observations=item.get('observations'),
            vinification_process_id=process_id
        )
        stage.id = uuid.UUID(item['id'])

        db.session.add(stage)
        print(f"  - Creada BottlingStage (ID: {stage.id}) para {vinification_processes_map[process_id].current_stage}")
        created += 1
    return created


def populate_all():
    with app.app_context():
        print("Iniciando el proceso de seeding de la base de datos...")

        # --- Eliminar datos existentes (Orden inverso a la creación por FKs) ---
        print("\n--- Limpiando datos existentes (tablas hijo a padre) ---")
        try:
            db.session.query(BottlingStage).delete()
            db.session.query(AgingStage).delete()
            db.session.query(FermentationStage).delete()
            db.session.query(ReceptionStage).delete()
            db.session.query(VinificationProcess).delete() 
            db.session.query(GrapeVariety).delete() # Nuevo: Eliminar GrapeVariety primero
            db.session.commit()
            print("Datos existentes limpiados.")
        except Exception as e:
            db.session.rollback()
            print(f"Advertencia: Error al limpiar datos existentes: {e}")
            print("Continuando de todas formas. Podría haber conflictos de datos.")

        # --- Cargar datos de los archivos JSON ---
        print("\n--- Cargando datos desde archivos JSON ---")
        grape_varieties_data = load_json_data('grape_variety.json') # Nuevo
        vinification_processes_data = load_json_data('vinification_processes.json')
        reception_stages_data = load_json_data('reception_stages.json')
        fermentation_stages_data = load_json_data('fermentation_stages.json')
        aging_stages_data = load_json_data('aging_stages.json')
        bottling_stages_data = load_json_data('bottling_stages.json')

        # --- Población de tablas en el ORDEN CORRECTO (padre a hijo) ---
        total_created = 0

        # 0. GrapeVariety (Ahora es el padre principal)
        count, grape_varieties_map = populate_grape_varieties(grape_varieties_data)
        total_created += count
        db.session.commit()
        print(f'{count} variedades de uva cargadas y mapeadas.')

        # 1. VinificationProcess (Ahora depende de GrapeVariety)
        count, vinification_processes_map = populate_vinification_processes(vinification_processes_data, grape_varieties_map)
        total_created += count
        db.session.commit()
        print(f'{count} procesos de vinificación cargados y mapeados.')

        # 2. ReceptionStage
        count = populate_reception_stages(reception_stages_data, vinification_processes_map)
        total_created += count
        db.session.commit()
        print(f'{count} etapas de recepción cargadas.')

        # 3. FermentationStage
        count = populate_fermentation_stages(fermentation_stages_data, vinification_processes_map)
        total_created += count
        db.session.commit()
        print(f'{count} etapas de fermentación cargadas.')

        # 4. AgingStage
        count = populate_aging_stages(aging_stages_data, vinification_processes_map)
        total_created += count
        db.session.commit()
        print(f'{count} etapas de guarda/crianza cargadas.')

        # 5. BottlingStage
        count = populate_bottling_stages(bottling_stages_data, vinification_processes_map)
        total_created += count
        db.session.commit()
        print(f'{count} etapas de embotellado cargadas.')

        print(f"\n¡Seeding completado con éxito! Total de registros creados: {total_created}")
        
        # Imprime el ID del proceso de embotellado general para que lo copies
        general_bottling_process_id = None
        for p in vinification_processes_data:
            if p['current_stage'] == "Embotellado" and p.get('description') == "Proceso general de embotellado de varios vinos.": # Basarse en la nueva data
                general_bottling_process_id = p['id']
                break
        
        if general_bottling_process_id:
            print("----------------------------------------------------------------------------------")
            print(f"Recuerda usar este UUID para FIXED_VINIFICATION_PROCESS_UUID en bottling_routes.py:")
            print(f"   -> {general_bottling_process_id}")
            print("----------------------------------------------------------------------------------")
        else:
            print("Advertencia: No se encontró 'Proceso Embotellado General' (basado en la descripción) en tus datos de vinification_processes.json.")


if __name__ == '__main__':
    with app.app_context():
        # Asegura que las tablas de la base de datos existan antes de intentar poblar.
        db.create_all()
        print("Tablas de la base de datos aseguradas/creadas.")
    populate_all()