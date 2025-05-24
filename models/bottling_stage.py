import uuid
from models.db import db

class BottlingStage:
    __tablename__: "BottlingStage"

    id = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    bottling_date = db.Column (db.Date, nullable=False)
    bottles_quantity = db.Column(db.Int, nullable=False)
    bottles_format = db.Column(db.String(50), nullable=False) 
    bottling_lot_number = db.Column(db.String, nullable=False)  
    observations = db.Column(db.Text, nullable=False) 
    
    def __init__(self, bottling_date, bottles_quantity, bottles_format, bottling_lot_number, observations ):
        
        self.bottling_date = bottling_date
        self.bottles_quantity = bottles_quantity
        self.bottles_format = bottles_format
        self.bottling_lot_number = bottling_lot_number
        self.observations = observations

    def serialize(self):
        return {
            "id": self.id,
            "bottling_date" : self.bottling_date,
            "bottles_quantity" : self.bottles_quantity,
            "bottles_format" : self.bottles_format,
            "bottling_lot_number" : self.bottling_lot_number,
            "observations" : self.observations,

        }