from app.models.base_model import BaseModel
from app.models import db


class Categoria(BaseModel):
    __tablename__ = "categorias"

    nombre = db.Column(db.String(100), nullable=False, unique=True)
    descripcion = db.Column(db.Text, nullable=True)
    productos = db.relationship("Producto", back_populates="categoria")

    def __init__(self, nombre, descripcion):
        self.nombre = nombre
        self.descripcion = descripcion

    def to_dict(self):
        data = super().to_dict()
        data.update({"nombre": self.nombre, "descripcion": self.descripcion})
        return data
