from app.models.user import User
from app.models.rol import Rol
from app.models import db
from app import create_app

app = create_app()
def get_or_create_role(nombre: str) -> Rol:
    rol = db.session.execute(
        db.select(Rol).filter_by(nombre=nombre)
    ).scalar_one_or_none()
    if rol is None:
        rol = Rol(nombre=nombre)
        db.session.add(rol)
        db.session.flush()  # obtiene id sin commit intermedio
    return rol

def get_or_create_user(nombre: str, email: str, password: str, rol_id: int) -> tuple[User, bool]:
    user = db.session.execute(
        db.select(User).filter_by(email=email)
    ).scalar_one_or_none()
    created = False
    if user is None:
        user = User(nombre=nombre, email=email, password=password, rol_id=rol_id)
        db.session.add(user)
        created = True
    else:
        user.nombre = nombre
        user.rol_id = rol_id
    # Siempre guardar hash (nunca texto plano)
    user.generate_password_hash(password)
    return user, created


def seed() -> None:
    admin_role = get_or_create_role("admin")
    operador_role = get_or_create_role("operador")
    admin_user, admin_created = get_or_create_user(
        nombre="admin",
        email="admin@example.com",
        password="admin123",
        rol_id=admin_role.id,
    )
    operador_user, operador_created = get_or_create_user(
        nombre="operador",
        email="operador@example.com",
        password="operador123",
        rol_id=operador_role.id,
    )
    db.session.commit()
    print("Seed completado.")
    print(
        f"- Rol admin: {'creado' if admin_role.id else 'reutilizado'} | "
        f"Rol operador: {'creado' if operador_role.id else 'reutilizado'}"
    )
    print(
        f"- Usuario admin: {'creado' if admin_created else 'reutilizado/actualizado'} "
        f"({admin_user.email})"
    )
    print(
        f"- Usuario operador: {'creado' if operador_created else 'reutilizado/actualizado'} "
        f"({operador_user.email})"
    )
if __name__ == "__main__":
    with app.app_context():
        seed()
