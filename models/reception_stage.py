import uuid
from models.db import db

class ReceptionStage(db.Model):
    __tablename__ = "receptionstage"

    id = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    reception_date = db.Column(db.Date, nullable=False)
    weight_kg = db.Column(db.Float, nullable=False)
    brix_degrees = db.Column(db.Float, nullable=False)
    ph_value = db.Column(db.Float, nullable=False)
    temperature_celcius = db.Column(db.Float, nullable=False)
    observations = db.Column(db.Text, nullable=False)

    vinification_process_id = db.Column(db.String(50), db.ForeignKey("vinification_process.id"), nullable=False, unique=True)
    vinification_process = db.relationship("VinificationProcess", back_populates="receptionstage", uselist=False)

    def __init__(self, reception_date, weight_kg, brix_degrees, ph_value, temperature_celcius, observations, vinification_process_id):
        self.reception_date = reception_date
        self.weight_kg = weight_kg
        self.brix_degrees = brix_degrees
        self.ph_value = ph_value
        self.temperature_celcius = temperature_celcius
        self.observations = observations
        self.vinification_process_id = vinification_process_id

    def serialize(self):
        return {
            "id": self.id,
            "reception_date": str(self.reception_date),
            "weight_kg": self.weight_kg,
            "brix_degrees": self.brix_degrees,
            "ph_value": self.ph_value,
            "temperature_celcius": self.temperature_celcius,
            "observations": self.observations,
            "vinification_process_id": self.vinification_process_id
        }

