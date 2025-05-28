from flask import Flask
from config.config import DATABASE_CONNECTION_URI
from routes.index import index
from routes.varieties import varieties
from routes.fermentacion import fermentacion
from routes.recepcion import recepcion

app = Flask(__name__)
app.register_blueprint(index)
app.register_blueprint(varieties)
app.register_blueprint(fermentacion)
app.register_blueprint(recepcion)

if __name__ == '__main__':
    print("Estoy ejecutando")
    app.run(debug=True)