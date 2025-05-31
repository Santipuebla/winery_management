from app import create_app
from models.db import db

app = create_app()

with app.app_context():
    db.create_all()
    print("✅ Tablas creadas correctamente.")
