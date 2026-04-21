from app import create_app
from app.models import db
from app.models.categoria import Categoria
from app.models.producto import Producto
from app.models.proveedor import Proveedor
from app.models.rol import Rol
from app.models.user import User

app = create_app()


def get_or_create_role(nombre: str) -> tuple[Rol, bool]:
    rol = db.session.execute(db.select(Rol).filter_by(nombre=nombre)).scalar_one_or_none()
    created = False
    if rol is None:
        rol = Rol(nombre=nombre)
        db.session.add(rol)
        db.session.flush()
        created = True
    return rol, created


def get_or_create_user(
    nombre: str, email: str, password: str, rol_id: int
) -> tuple[User, bool]:
    user = db.session.execute(db.select(User).filter_by(email=email)).scalar_one_or_none()
    created = False
    if user is None:
        user = User(nombre=nombre, email=email, password=password, rol_id=rol_id)
        db.session.add(user)
        created = True
    else:
        user.nombre = nombre
        user.rol_id = rol_id
    # Siempre guardar hash en lugar de texto plano
    user.generate_password_hash(password)
    return user, created


def get_or_create_categoria(nombre: str, descripcion: str) -> tuple[Categoria, bool]:
    categoria = db.session.execute(
        db.select(Categoria).filter_by(nombre=nombre)
    ).scalar_one_or_none()
    created = False

    if categoria is None:
        categoria = Categoria(nombre=nombre, descripcion=descripcion)
        db.session.add(categoria)
        db.session.flush()
        created = True
    else:
        categoria.descripcion = descripcion

    return categoria, created


def get_or_create_proveedor(
    nombre: str,
    contacto: str | None = None,
    telefono: str | None = None,
    email: str | None = None,
) -> tuple[Proveedor, bool]:
    proveedor = db.session.execute(
        db.select(Proveedor).filter_by(nombre=nombre)
    ).scalar_one_or_none()
    created = False

    if proveedor is None:
        proveedor = Proveedor(
            nombre=nombre,
            contacto=contacto,
            telefono=telefono,
            email=email,
        )
        db.session.add(proveedor)
        db.session.flush()
        created = True
    else:
        proveedor.contacto = contacto
        proveedor.telefono = telefono
        proveedor.email = email

    return proveedor, created


def get_or_create_producto(
    nombre: str,
    descripcion: str,
    precio_costo: float,
    precio_venta: float,
    stock_actual: int,
    stock_minimo: int,
    categoria_id: int,
    proveedor_id: int | None,
) -> tuple[Producto, bool]:
    producto = db.session.execute(
        db.select(Producto).filter_by(nombre=nombre)
    ).scalar_one_or_none()
    created = False

    if producto is None:
        producto = Producto(
            nombre=nombre,
            descripcion=descripcion,
            precio_costo=precio_costo,
            precio_venta=precio_venta,
            stock_actual=stock_actual,
            stock_minimo=stock_minimo,
            categoria_id=categoria_id,
            proveedor_id=proveedor_id,
        )
        db.session.add(producto)
        created = True
    else:
        producto.descripcion = descripcion
        producto.precio_costo = precio_costo
        producto.precio_venta = precio_venta
        producto.stock_actual = stock_actual
        producto.stock_minimo = stock_minimo
        producto.categoria_id = categoria_id
        producto.proveedor_id = proveedor_id

    return producto, created


def seed() -> None:
    admin_role, admin_role_created = get_or_create_role("admin")
    operador_role, operador_role_created = get_or_create_role("operador")

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

    almacen_cat, almacen_created = get_or_create_categoria(
        nombre="Almacen", descripcion="Productos secos"
    )
    limpieza_cat, limpieza_created = get_or_create_categoria(
        nombre="Limpieza", descripcion="Articulos de limpieza"
    )

    proveedor, proveedor_created = get_or_create_proveedor(
        nombre="Distribuidora Norte",
        telefono="2994001234",
    )

    harina_producto, harina_created = get_or_create_producto(
        nombre="Harina 000",
        descripcion="Harina de trigo 000",
        precio_costo=280,
        precio_venta=350,
        stock_actual=50,
        stock_minimo=10,
        categoria_id=almacen_cat.id,
        proveedor_id=proveedor.id,
    )
    lavandina_producto, lavandina_created = get_or_create_producto(
        nombre="Lavandina 1L",
        descripcion="Lavandina para limpieza de hogar",
        precio_costo=150,
        precio_venta=210,
        stock_actual=30,
        stock_minimo=5,
        categoria_id=limpieza_cat.id,
        proveedor_id=proveedor.id,
    )

    db.session.commit()

    print("Seed completado.")
    print(
        f"- Rol admin: {'creado' if admin_role_created else 'reutilizado'} | "
        f"Rol operador: {'creado' if operador_role_created else 'reutilizado'}"
    )
    print(
        f"- Usuario admin: {'creado' if admin_created else 'reutilizado/actualizado'} "
        f"({admin_user.email})"
    )
    print(
        f"- Usuario operador: {'creado' if operador_created else 'reutilizado/actualizado'} "
        f"({operador_user.email})"
    )
    print(
        f"- Categoria Almacen: {'creada' if almacen_created else 'reutilizada/actualizada'}"
    )
    print(
        f"- Categoria Limpieza: {'creada' if limpieza_created else 'reutilizada/actualizada'}"
    )
    print(
        f"- Proveedor Distribuidora Norte: {'creado' if proveedor_created else 'reutilizado/actualizado'}"
    )
    print(f"- Producto Harina 000: {'creado' if harina_created else 'reutilizado/actualizado'}")
    print(
        f"- Producto Lavandina 1L: {'creado' if lavandina_created else 'reutilizado/actualizado'}"
    )


if __name__ == "__main__":
    with app.app_context():
        seed()
