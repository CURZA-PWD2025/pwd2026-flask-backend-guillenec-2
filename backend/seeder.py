from app.models.user import User
from app.models.rol import Rol
from app.models import db
from app import create_app

app = create_app()


def seed():
    # Crear roles
    admin_role = Rol(nombre='admin')
    operador_role = Rol(nombre='operador')
    db.session.add_all([admin_role, operador_role])
    db.session.commit()

    # Crear usuarios
    admin_user = User(nombre='admin', password='admin123', rol_id=admin_role.id, email='admin@example.com')
    regular_user = User(nombre='operador', password='operador123', rol_id=operador_role.id, email='operador@example.com')
    db.session.add_all([admin_user, regular_user])
    db.session.commit()
    
if __name__ == '__main__':
    with app.app_context():
        seed()