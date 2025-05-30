import uuid
from models.db import db

class BottlingStage(db.Model): 
    __tablename__ = "bottlingstage"

    id = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    bottling_date = db.Column(db.Date, nullable=False)
    bottles_quantity = db.Column(db.Integer, nullable=False)
    bottles_format = db.Column(db.String(50), nullable=False)
    bottling_lot_number = db.Column(db.String(50), nullable=False)
    observations = db.Column(db.Text, nullable=False)

    vinification_process_id = db.Column(db.String(50), db.ForeignKey("vinification_process.id"), nullable=False, unique=True) 
    vinification_process = db.relationship("VinificationProcess", back_populates="bottling_stage", uselist=False)

    def __init__(self, bottling_date, bottles_quantity, bottles_format, bottling_lot_number, observations, vinification_process_id):
        self.bottling_date = bottling_date
        self.bottles_quantity = bottles_quantity
        self.bottles_format = bottles_format
        self.bottling_lot_number = bottling_lot_number
        self.observations = observations
        self.vinification_process_id = vinification_process_id

    def serialize(self):
        return {
            "id": self.id,
            "bottling_date": str(self.bottling_date.isoformat() if self.bottling_date else None),
            "bottles_quantity": self.bottles_quantity,
            "bottles_format": self.bottles_format,
            "bottling_lot_number": self.bottling_lot_number,
            "observations": self.observations,
            "vinification_process_id": self.vinification_process_id
        }
