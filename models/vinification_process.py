import uuid 
from models.db import db 
class VinificationProcess(db.Model):
    __tablename__ = 'VinificationProcess'

    id = db.Column (db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    start_date = db.Column(db.Date, nullable = False) 
    end_date = db.Column (db.Date, nullable = False)
    current_stage = db.Column(db.String(50), nullable = False)
    description = db.Column (db.Text, nullable = True)
    id_variety = db.relationship ('GrapeVariety', backref = 'VinificationProcess', lazy = True)
    id_reception = db.relationship ('ReceptionStage', backref = 'VinificationProcess', lazy = True)
    id_fermentation = db.relationship ('FermentationStage', backref = 'VinificationProcess', lazy = True)
    id_bottling = db.relationship ('BottlingStage', backref = 'VinificationProcess', lazy = True)
    id_aging = db.relationship ('AgingStage', backref = 'VinificationProcess', lazy = True)

    def __init__(self,start_date,end_date,current_stage,id_variety,id_reception,id_fermentation,id_bottling,id_aging):
        self.start_date = start_date
        self.end_date = end_date
        self.current_stage = current_stage 
        self.id_variety = id_variety
        self.id_reception = id_reception
        self.id_fermentation = id_fermentation 
        self.id_bottling = id_bottling
        self.id_aging = id_aging
    def serialize (self):
        {
            'id' :self.id,
            'start_date': str(self.start_date),
            'end_date': str(self.end_date),
            'current_stage': self.current_stage,
            'id_variety': self.id_variety,
            'id_reception': self.id_reception,
            'id_fermentation': self.id_fermentation,
            'id_bottling': self.id_bottling,
            'id_aging': self.id_aging
        }