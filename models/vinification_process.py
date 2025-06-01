import uuid
from models.db import db 
from models.reception_stage import ReceptionStage
from models.fermentation_stage import FermentationStage
from models.bottling_stage import BottlingStage
from models.aging_stage import AgingStage

class VinificationProcess(db.Model):

    __tablename__ = 'vinification_process' 

    _tablename_ = 'vinification_process' 


    id = db.Column(db.String(50), primary_key=True,unique=True, default=lambda: str(uuid.uuid4())) # UUIDs son de 36 caracteres con guiones
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=True) # Puede ser null si el proceso aún no ha terminado
    current_stage = db.Column(db.String(50), nullable=False) # Nombre de la etapa actual
    description = db.Column(db.Text, nullable=True) # Descripción del proceso
    grape_variety_id = db.Column(db.String(36), db.ForeignKey('grape_variety.id'), nullable=False) # Esto vincula cada proceso de vinificación a una variedad de uva
    # La relación inversa la definimos en GrapeVariety con backref='grape_variety'

    # Las relaciones One-to-One con las etapas (las FKs están en las tablas de las etapas)
    # Usamos uselist=False para indicar que es una relación 1:1 

    reception_stage = db.relationship('ReceptionStage', back_populates='vinification_process', uselist=False)
    reception_stage = db.relationship('ReceptionStage', back_populates='vinification_process', uselist=False)
    fermentation_stage = db.relationship('FermentationStage', back_populates='vinification_process', uselist=False)
    bottling_stage = db.relationship('BottlingStage', back_populates='vinification_process', uselist=False)
    aging_stage = db.relationship("AgingStage", back_populates="vinification_process", uselist=False)


    def _init_(self, start_date, current_stage, grape_variety_id, end_date=None, description=None):
        self.start_date = start_date
        self.end_date = end_date
        self.current_stage = current_stage
        self.description = description
        self.grape_variety_id = grape_variety_id # Ahora se pasa la FK directamente

    def serialize(self):
        reception_id = self.reception_stage.id if self.reception_stage else None
        fermentation_id = self.fermentation_stage.id if self.fermentation_stage else None
        bottling_id = self.bottling_stage.id if self.bottling_stage else None
        aging_id = self.aging_stage.id if self.aging_stage else None

        return {
            'id': self.id,
            'start_date': str(self.start_date),
            'end_date': str(self.end_date) if self.end_date else None,
            'current_stage': self.current_stage,
            'description': self.description,
            'grape_variety_id': self.grape_variety_id,
            'reception_stage_id': reception_id,
            'fermentation_stage_id': fermentation_id,
            'bottling_stage_id': bottling_id,
            'aging_stage_id': aging_id
        }