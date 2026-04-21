from flask import Response, jsonify
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

from app.controllers import Controller
from app.models import db
from app.models.producto import Producto

class ProductoController(Controller):
    @staticmethod
    def _producto_to_response(product: Producto) -> dict:
        return {
            "id": product.id,
            "nombre": product.nombre,
            "descripcion": product.descripcion,
            "precio_costo": str(product.precio_costo),
            "precio_venta": str(product.precio_venta),
            "stock_actual": product.stock_actual,
            "stock_minimo": product.stock_minimo,
            "categoria": {
                "id": product.categoria.id,
                "nombre": product.categoria.nombre,
            }
            if product.categoria
            else None,
            "proveedor": {
                "id": product.proveedor.id,
                "nombre": product.proveedor.nombre,
            }
            if product.proveedor
            else None,
        }

    @staticmethod
    def get_all() -> tuple[Response, int]:
        productos_list = (
            db.session.execute(
                db.select(Producto)
                .options(
                    joinedload(Producto.categoria),
                    joinedload(Producto.proveedor),
                )
                .order_by(db.desc(Producto.id))
            )
            .scalars()
            .all()
        )

        if len(productos_list) > 0:
            productos_to_dict = [
                ProductoController._producto_to_response(product)
                for product in productos_list
            ]
            return jsonify(productos_to_dict), 200
        return jsonify({"message": "datos no encontrados"}), 404

    @staticmethod
    def show(id: int) -> tuple[Response, int]:
        producto = (
            db.session.execute(
                db.select(Producto)
                .options(
                    joinedload(Producto.categoria),
                    joinedload(Producto.proveedor),
                )
                .filter_by(id=id)
                )
            .scalar_one_or_none()
            )

        if producto:
            producto_to_dict = ProductoController._producto_to_response(producto)
            return jsonify(producto_to_dict), 200
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
        
        
