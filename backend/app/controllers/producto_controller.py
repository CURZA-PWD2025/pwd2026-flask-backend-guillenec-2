from flask import Response, jsonify
from sqlalchemy.exc import IntegrityError

from app.controllers import Controller
from app.models import db
from app.models.producto import Producto

class ProductoController(Controller):
    @staticmethod
    def get_all() -> tuple[Response, int]:
        productos_list = (
            db.session.execute(db.select(Producto).order_by(db.desc(Producto.id)))
            .scalars()
            .all()
        )
        if len(productos_list) > 0:
            productos_to_dict = [producto.to_dict() for producto in productos_list]
            return jsonify(productos_to_dict), 200
        return jsonify({"message": "datos no encontrados"}), 404

    @staticmethod
    def show(id: int) -> tuple[Response, int]:
        producto = db.session.get(Producto, id)
        if producto:
            return jsonify(producto.to_dict()), 200

        return jsonify({"message": "producto no encontrado"}), 404
    
    @staticmethod
    def create(data: dict) -> tuple[Response, int]:
        try:
            new_producto = Producto(
                nombre=data["nombre"],
                descripcion=data.get("descripcion"),
                precio_costo=data["precio_costo"],
                precio_venta=data["precio_venta"],
                stock_actual=data["stock_actual"],
                stock_minimo=data["stock_minimo"],
                categoria_id=data["categoria_id"],
                proveedor_id=data.get("proveedor_id"),
            )
            db.session.add(new_producto)
            db.session.commit()

            return jsonify({"message": "producto creado exitosamente"}), 201

        except IntegrityError:
            db.session.rollback()
            return jsonify({"message": "error de integridad en la base de datos"}), 409

        except Exception as e:
            db.session.rollback()
            print(e)
            return jsonify({"message": "error interno del servidor"}), 500
        
    @staticmethod
    def update(id: int, data: dict) -> tuple[Response, int]:
        try:
            producto = db.session.get(Producto, id)
            if not producto:
                return jsonify({"message": "producto no encontrado"}), 404

            producto.nombre = data.get("nombre", producto.nombre)
            producto.descripcion = data.get("descripcion", producto.descripcion)
            producto.precio_costo = data.get("precio_costo", producto.precio_costo)
            producto.precio_venta = data.get("precio_venta", producto.precio_venta)
            producto.stock_actual = data.get("stock_actual", producto.stock_actual)
            producto.stock_minimo = data.get("stock_minimo", producto.stock_minimo)
            producto.categoria_id = data.get("categoria_id", producto.categoria_id)
            producto.proveedor_id = data.get("proveedor_id", producto.proveedor_id)

            db.session.commit()

            return jsonify({"message": "producto actualizado exitosamente"}), 200

        except IntegrityError:
            db.session.rollback()
            return jsonify({"message": "error de integridad en la base de datos"}), 409

        except Exception as e:
            db.session.rollback()
            print(e)
            return jsonify({"message": "error interno del servidor"}), 500
        

    @staticmethod
    def delete(id: int) -> tuple[Response, int]:
        try:
            producto = db.session.get(Producto, id)
            if not producto:
                return jsonify({"message": "producto no encontrado"}), 404
            
            db.session.delete(producto)
            db.session.commit()

            return jsonify({"message": "producto eliminado exitosamente"}), 200

        except IntegrityError:
            db.session.rollback()
            return jsonify({"message": "error de integridad en la base de datos"}), 409

        except Exception as e:
            db.session.rollback()
            print(e)
            return jsonify({"message": "error interno del servidor"}), 500
        
        
