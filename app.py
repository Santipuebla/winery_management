from flask import Flask
from config.config import DATABASE_CONNECTION_URI
from models.db import db
from routes.fermentation_stage_route import fermentation
from routes.grape_variety_route import grape_varieties



def create_app():
    app = Flask(__name__)
    app.secret_key = 'clave_super_secreta'
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_CONNECTION_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Registro de todos los blueprints
    app.register_blueprint(fermentation)
    app.register_blueprint(grape_varieties)




    @app.route('/')
    def index():
        return "Winery App corriendo 🍇"

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

