from flask import Flask   #importamos flask
from config.config import DATABASE_CONNECTION_URI #importamos la variable de conexion a la bd
from models.db import db #importamos db que nos va a permitir definir los modelos, tablas, etc.

