import uuid
from models.db import db 

class GrapeVariety(db.Model):
    tablename = 'grape_variety' 

    id = db.Column(db.String(36), primary_key=True, unique= True, default=lambda: str(uuid.uuid4())) 
    grape_name = db.Column(db.String(50), unique=True, nullable=False) # el nombre de uva es único
    grape_origin = db.Column(db.String(50), nullable=False)
    grape_image = db.Column(db.String(300), nullable=True) # Si la imagen es opcional, nullable=True
    status = db.Column(db.Boolean, default=True, nullable=False) 
    vinification_processes = db.relationship('VinificationProcess', backref='grape_variety', lazy=True)

    # backref='grape_variety' crea un atributo 'grape_variety' en VinificationProcess

    def init(self, grape_name, grape_origin, grape_image=None, status=True):
        self.grape_name = grape_name
        self.grape_origin = grape_origin
        self.grape_image = grape_image
        self.status = status

    def serialize(self):
        return {
            'id': self.id,
            'grape_name': self.grape_name,
            'grape_origin': self.grape_origin,
            'grape_image': self.grape_image,
            'status': self.status,
            'vinification_processes_ids': [p.id for p in self.vinification_processes] # Serializamos los IDs de los procesos para evitar la recursión 
        }