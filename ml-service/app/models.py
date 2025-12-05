from sqlalchemy import Column, Integer, String, DateTime, Float, JSON, Text
from .db import Base

from sqlalchemy import Column, Integer, String, Float, DateTime, Date, ForeignKey, Float, JSON, Text
from sqlalchemy.orm import relationship
#from app.database import Base


class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), unique=True, nullable=False)
    categoria = Column(String(50))
    precio = Column(Float)

    ventas = relationship("Venta", back_populates="producto")


class Venta(Base):
    __tablename__ = "ventas"

    id = Column(Integer, primary_key=True)
    ticket_id = Column(Integer, index=True)
    producto_id = Column(Integer, ForeignKey("productos.id"))
    fecha = Column(Date)
    cantidad = Column(Integer)
    total = Column(Float)
    producto = relationship("Producto", back_populates="ventas")


# class Venta(Base):
#     __tablename__ = 'ventas'
#     id = Column(Integer, primary_key=True, index=True)
#     id_venta = Column(Integer, index=True)
#     producto = Column(String, index=True)
#     fecha = Column(DateTime, index=True)
#     cantidad = Column(Integer)
#     total = Column(Float)

# class ReglaApriori(Base):
#     __tablename__ = 'reglas_apriori'
#     id = Column(Integer, primary_key=True, index=True)
#     created_at = Column(DateTime)
#     params = Column(JSON)
#     rules_json = Column(JSON)

class ReglaAprioriRun(Base):
    __tablename__ = "reglas_apriori_runs"
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime)
    params = Column(JSON)

class ReglaAprioriRule(Base):
    __tablename__ = "reglas_apriori_rules"
    
    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(Integer, ForeignKey("reglas_apriori_runs.id", ondelete="CASCADE"))
    
    antecedents = Column(JSON)
    consequents = Column(JSON)
    support = Column(Float)
    confidence = Column(Float)
    lift = Column(Float)

