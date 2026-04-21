import os
from dotenv import load_dotenv
from flask import Flask
from app.config import config
from app.models import db

from app.routes.__init__ import api_v1

from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

load_dotenv(override = True)
migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)

    env = os.getenv('FLASK_ENV', 'development')
    app.config.from_object(config[env])

    db.init_app(app)
    migrate.init_app(app=app, db=db)
    jwt.init_app(app)

    app.register_blueprint(api_v1)

    @app.get("/")
    def health():
        return {"message": "API TP1 activa"}, 200 
    
    return app
    