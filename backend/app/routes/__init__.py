from flask import Blueprint

from app.routes.auth_routes import auth_bp
from app.routes.rol_routes import roles
from app.routes.user_routes import users

# Crear un Blueprint para la versión 1 de la API
api_v1 = Blueprint("api_v1", __name__, url_prefix="/api/v1")

# Registrar las rutas en el Blueprint
api_v1.register_blueprint(users)
api_v1.register_blueprint(roles)
api_v1.register_blueprint(auth_bp)
