from app.models.base_model import BaseModel
from app.models import db


class MovimientoStock(BaseModel):
    __tablename__ = "movimientos_stock"

    tipo = db.Column(db.String(20), nullable=False)  # 'entrada' o 'salida'
    cantidad = db.Column(db.Integer, nullable=False)
    motivo = db.Column(db.String(200), nullable=True)
    producto_id = db.Column(db.Integer, db.ForeignKey("productos.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # Relaciones
    producto = db.relationship("Producto", back_populates="movimientos_stock")
    user = db.relationship("User", back_populates="movimientos_stock")

    def __init__(self, tipo, cantidad, motivo, producto_id, user_id):
        self.tipo = tipo
        self.cantidad = cantidad
        self.motivo = motivo
        self.producto_id = producto_id
        self.user_id = user_id

    def to_dict(self):
        data = super().to_dict()
        data.update(
            {
                "tipo": self.tipo,
                "cantidad": self.cantidad,
                "motivo": self.motivo,
                "producto_id": self.producto_id,
                "user_id": self.user_id,
            }
        )
        return data

    def validate_tipo(self):
        if self.tipo not in ["entrada", "salida"]:
            raise ValueError("El tipo de movimiento debe ser 'entrada' o 'salida'")
        return True

    def validate_cantidad(self):
        return self.cantidad > 0
