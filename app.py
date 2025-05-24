from flask import Flask
from config.config import DATABASE_CONNECTION_URI
from routes.index import index

app = Flask(__name__)
app.register_blueprint(index)

if __name__ == '__main__':
    print("Estoy ejecutando")
    app.run(debug=True)