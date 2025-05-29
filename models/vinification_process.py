import uuid
from models.db import db
# No necesitas importar las otras clases aquí si solo usas el backref/back_populates

class VinificationProcess(db.Model):
    __tablename__ = "vinification_process"

    id = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    current_stage = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True) # Agregado campo 'description' que está en el diagrama

    # FK a GrapeVariety (un proceso tiene una variedad de uva, una variedad de uva puede tener muchos procesos)
    variety_id = db.Column(db.String(50), db.ForeignKey('grape_variety.id'), nullable=False)

    # Relaciones One-to-One con las etapas (las FKs están en las tablas de las etapas)
    # Usamos back_populates para que la relación sea bidireccional y se maneje correctamente
    reception = db.relationship('ReceptionStage', back_populates='vinification_process', uselist=False)
    fermentation = db.relationship('FermentationStage', back_populates='vinification_process', uselist=False)
    bottling = db.relationship('BottlingStage', back_populates='vinification_process', uselist=False)
    aging = db.relationship('AgingStage', back_populates='vinification_process', uselist=False)

    # La relación con GrapeVariety (desde el lado "muchos")
    variety = db.relationship('GrapeVariety', backref='vinification_processes', lazy=True)


    def __init__(self, start_date, end_date, current_stage, variety_id, description=None):
        self.start_date = start_date
        self.end_date = end_date
        self.current_stage = current_stage
        self.variety_id = variety_id
        self.description = description # Inicializar el nuevo campo

    def serialize(self):
        return {
            'id': self.id,
            'start_date': str(self.start_date),
            'end_date': str(self.end_date),
            'current_stage': self.current_stage,
            'description': self.description,
            'variety_id': self.variety_id,
            # Para serializar las relaciones, puedes cargar las etapas si están presentes
            # Esto puede causar problemas de carga N+1 si no se maneja con cuidado
            'reception_stage': self.reception.serialize() if self.reception else None,
            'fermentation_stage': self.fermentation.serialize() if self.fermentation else None,
            'bottling_stage': self.bottling.serialize() if self.bottling else None,
            'aging_stage': self.aging.serialize() if self.aging else None
        }