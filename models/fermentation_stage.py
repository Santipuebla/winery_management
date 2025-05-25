import uuid
from models.db import db

class FermentationStage(db.Model):
    __tablename__ = 'fermentation_stage' 

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4())) 
    fermentation_start_date = db.Column(db.Date, nullable=False)
    fermentation_end_date = db.Column(db.Date, nullable=True) 
    density = db.Column(db.Float, nullable=False)
    total_acidity = db.Column(db.Float, nullable=False)
    temperature_celsius = db.Column(db.Float, nullable=False)
    observations = db.Column(db.Text, nullable=True) # Texto largo, puede ser opcional

    # Esta es la columna que apunta al proceso de vinificación
    vinification_process_id = db.Column(db.String(36), db.ForeignKey('vinification_process.id'), unique=True, nullable=True)
    # unique=True para asegurar que un proceso solo tenga UNA etapa de fermentación
    # nullable=True si la etapa puede existir sin un proceso asociado inicialmente, o si se añade después.
    # Si siempre debe estar ligada a un proceso desde su creación, usa nullable=False y pásala en el __init__.

    # Relación inversa: FermentationStage tiene un VinificationProcess
    # El backref 'vinification_process' crea un atributo de relación en VinificationProcess
    # 'uselist=False' indica que es una relación 1:1 
    vinification_process = db.relationship('VinificationProcess', backref=db.backref('fermentation_stage', uselist=False), lazy=True)


    def __init__(self, fermentation_start_date, density, total_acidity, temperature_celsius,fermentation_end_date=None, observations=None, vinification_process_id=None): 
        self.fermentation_start_date = fermentation_start_date
        self.fermentation_end_date = fermentation_end_date
        self.density = density
        self.total_acidity = total_acidity
        self.temperature_celsius = temperature_celsius
        self.observations = observations
        self.vinification_process_id = vinification_process_id # Asignar la FK aquí

    def serialize(self):
        return {
            'id': self.id,
            'fermentation_start_date': str(self.fermentation_start_date),
            'fermentation_end_date': str(self.fermentation_end_date) if self.fermentation_end_date else None, # Manejar None
            'density': self.density,
            'total_acidity': self.total_acidity,
            'temperature_celsius': self.temperature_celsius,
            'observations': self.observations,
            'vinification_process_id': self.vinification_process_id
            # Serializamos el ID del proceso de vinificación, no el objeto completo
        }