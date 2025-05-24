import uuid
from models.db import db

class FermentationStage(db.Model): 
    __tablename__ = 'FermentationStage'

    id = db.Column (db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    fermentation_start_date = db.Column(db.Date, nullable= False)
    fermentation_end_date = db.Column (db.Date, nullable= False)
    density = db.Column (db.Float, nullable = False)
    total_acidity = db.Column (db.Float, nullable = False)
    temperature_celsius = db.Column (db.Float, nullable = False)
    observations = db.Column (db.Text, nullable = True)
    vinification_process = db.relationship('VinificationProcess', backref = 'FermentationStage', lazy = True)

    def __init__(self,fermentation_start_date,fermentation_end_date,density,total_acidity,temperature_celsius,observations):
        self.fermentation_start_date = fermentation_start_date
        self.fermentation_end_date = fermentation_end_date
        self.density = density
        self.total_acidity = total_acidity
        self.temperature_celsius = temperature_celsius
        self.observations = observations
    
    def serialize(self):
        {
            'id': self.id,
            'fermentation_start_date': str(self.fermentation_start_date),
            'fermentation_end_date': str(self.fermentation_end_date),
            'density': self.density,
            'total_acidity': self.total_acidity,
            'temperature_celsius': self.temperature_celsius,
            'observations': self.observations,
            'vinification_process': self.vinification_process
        }
