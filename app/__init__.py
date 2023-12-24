from flask_restful import Api
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_login import LoginManager
app=Flask(__name__)
api = Api(app)
login = LoginManager(app)
login.login_view = 'login'

app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
CORS(app)
from app import route, model

if __name__ == "__name__":
    app.run(host='0.0.0.0', port=5000)
    app.run(debug=True)

