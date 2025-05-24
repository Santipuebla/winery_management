from flask import Flask
from config.config import DATABASE_CONNECTION_URI
from routes.routes_index import index
from routes.routes_embotellamiento import embotellamiento
from routes.routes_crianza import crianza

app = Flask(__name__)
app.register_blueprint(index)
app.register_blueprint(embotellamiento)
app.register_blueprint(crianza)

if __name__ == '__main__':
    print("Estoy ejecutando")
    app.run(debug=True)