from flask import Flask
from flask_cors import CORS, cross_origin
from flask_restful import Api,Resource
from flask_sqlalchemy import SQLAlchemy
from blue.api.routes import mod 

from blue.api.routes import db

app = Flask(__name__)
CORS(app)

db.init_app(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

with app.app_context():
    # Imports
    from blue.api import routes
    db.create_all()

app.register_blueprint(api.routes.mod,url_prefix = '/api')
