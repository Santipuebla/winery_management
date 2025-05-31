from flask import Flask
from config.config import DATABASE_CONNECTION_URI
from models.db import db #importamos db que nos va a permitir definir los modelos, tablas, etc.
from routes.routes_index import index
from routes.bottling_stage_route import bottling
from routes.aging_stage_route import aging

app = Flask(__name__)
app.secret_key = 'clave_secreta'
app.register_blueprint(index)
app.register_blueprint(bottling)
app.register_blueprint(aging)

app.config["SQLALCHEMY_DATABASE_URI"]= DATABASE_CONNECTION_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    from models.grape_variety import GrapeVariety
    from models.vinification_process import VinificationProcess
    from models.reception_stage import ReceptionStage
    from models.fermentation_stage import FermentationStage
    from models.bottling_stage import BottlingStage
    from models.aging_stage import AgingStage
    db.drop_all()
    db.create_all()


if __name__ == '__main__':
    print("Estoy ejecutando")
    app.run(debug=True)

