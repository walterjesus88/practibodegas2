from app.db import SessionLocal
from app.models import Producto, Venta
from datetime import date, timedelta
import random

db = SessionLocal()

db.query(Venta).delete()
db.query(Producto).delete()
db.commit()

productos_data = [
    ("Coca Cola 500ml", "Bebidas", 3.5),
    ("Inka Kola 500ml", "Bebidas", 3.5),
    ("Agua San Luis 600ml", "Bebidas", 2.0),
    ("Red Bull Lata", "Bebidas", 7.0),
    ("Leche Gloria 1L", "Lácteos", 5.5),
    ("Yogurt Gloria Fresa 1L", "Lácteos", 6.0),
    ("Queso Andino 250g", "Lácteos", 8.0),
    ("Mantequilla Laive", "Lácteos", 6.5),
    ("Atún Real 170g", "Conservas", 4.5),
    ("Sardina Florida 155g", "Conservas", 3.8),
    ("Aceite Primor 1L", "Aceites", 8.9)
]

productos = [
    Producto(nombre=p[0], categoria=p[1], precio=p[2])
    for p in productos_data
]

db.add_all(productos)
db.commit()

ventas = []
today = date.today()
ticket_id = 1

for _ in range(8000):
    productos_ticket = random.sample(productos, random.randint(4, 10))
    fecha_venta = today - timedelta(days=random.randint(0, 60))

    for prod in productos_ticket:
        cantidad = random.randint(1, 5)
        total = round(prod.precio * cantidad, 2)
        ventas.append(Venta(
            ticket_id=ticket_id,
            producto_id=prod.id,
            fecha=fecha_venta,
            cantidad=cantidad,
            total=total
        ))

    ticket_id += 1

db.add_all(ventas)
db.commit()

db.close()
print("Datos insertados correctamente en PostgreSQL 🚀")
