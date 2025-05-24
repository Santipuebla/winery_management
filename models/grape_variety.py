import uuid
from models.db import db 
class GrapeVariety (db.model):
    __tablename__ : "GrapeVariety"
    
    id = db.Column (db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    grape_name = db.Column (db.String(50), nullable = False)
    grape_origin = db.Column (db.String(50), nullable = False)
    grape_image =  db.Column(db.String(300), nullable=True)
    status = db.Column(db.Boolean, default=True)
    vinification_process = db.relationship('VinificationProcess', backref = 'GrapeVariety', lazy = True)
    
    def __init__(self,grape_name,grape_origin,vinification_process,grape_image=None,status=True):
        self.grape_name = grape_name
        self.grape_origin = grape_origin
        self.grape_image = grape_image
        self.status = status
        self.vinification_process = vinification_process
    
    def serialize (self):
        return {
            'id': self.id,
            'grape_name': self.grape_name,
            'grape_origin': self.grape_origin,
            'grape_image': self.grape_image,
            'status': self.status,
            'vinification_process': self.vinification_process
        }






