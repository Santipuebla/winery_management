import uuid
from models.db import db

class AgingStage(db.Model):
    __tablename__ = "aging_stage" # Cambiado a snake_case

    id = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    aging_start_date = db.Column(db.Date, nullable=False)
    aging_end_date = db.Column(db.Date, nullable=False)
    vessel_type = db.Column(db.String(50), nullable=False)
    volume_liters = db.Column(db.Float, nullable=False)
    vessel_identifier = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    observations = db.Column(db.Text, nullable=True) # Cambiado a nullable=True

    # FK a VinificationProcess (relación uno a uno)
    vinification_process_id = db.Column(
        db.String(50),
        db.ForeignKey("vinification_process.id"),
        nullable=False,
        unique=True
    )

    vinification_process = db.relationship(
        "VinificationProcess",
        back_populates="aging", # Usamos back_populates para mayor claridad y consistencia
        uselist=False
    )

    def __init__(self, aging_start_date, aging_end_date, vessel_type, volume_liters, vessel_identifier, location, observations, vinification_process_id):
        self.aging_start_date = aging_start_date
        self.aging_end_date = aging_end_date
        self.vessel_type = vessel_type
        self.volume_liters = volume_liters
        self.vessel_identifier = vessel_identifier
        self.location = location
        self.observations = observations
        self.vinification_process_id = vinification_process_id

    def serialize(self):
        return {
            "id": self.id,
            "aging_start_date": str(self.aging_start_date),
            "aging_end_date": str(self.aging_end_date),
            "vessel_type": self.vessel_type,
            "volume_liters": self.volume_liters,
            "vessel_identifier": self.vessel_identifier,
            "location": self.location,
            "observations": self.observations,
            "vinification_process_id": self.vinification_process_id
        }