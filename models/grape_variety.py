import uuid
from models.db import db

class GrapeVariety(db.Model):
    __tablename__ = "grape_variety"

    id = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    grape_name = db.Column(db.String(50), nullable=False)
    grape_origin = db.Column(db.String(50), nullable=False)
    grape_image = db.Column(db.String(300), nullable=True)
    status = db.Column(db.Boolean, default=True)

    # La relación se define desde VinificationProcess con un backref
    # No es necesario definir una relación 'vinification_process' aquí de esta manera
    # La relación 'vinification_processes' (plural) se accederá a través del backref
    # definido en VinificationProcess.

    def __init__(self, grape_name, grape_origin, grape_image=None, status=True):
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
            'status': self.status
            # No se incluye vinification_process aquí directamente ya que es una relación de uno a muchos
            # y se accedería a través de 'vinification_processes' si lo necesitas.
        }


