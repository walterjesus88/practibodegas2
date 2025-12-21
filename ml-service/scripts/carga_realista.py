from app.db import SessionLocal
from app.models import Producto, Venta
from datetime import date, timedelta
import random

db = SessionLocal()
db.query(Venta).delete()
db.query(Producto).delete()
db.commit()

# ============================================================
# 1. PRODUCTOS BASE (tu lista completa)
# ============================================================

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
    ("Galleta Oreo", "Snacks", 2.8),
    ("Galleta Casino", "Snacks", 2.5),
    ("Chizitos", "Snacks", 1.8),
    ("Papas Lay’s 45g", "Snacks", 3.0),
    ("Chocolate Sublime", "Dulces", 2.0),
    ("Chocolate Triángulo", "Dulces", 2.5),
    ("Chicle Trident", "Dulces", 1.5),
    ("Caramelos Halls", "Dulces", 1.2),
    ("Shampoo Sedal 350ml", "Higiene", 9.0),
    ("Jabón Dove", "Higiene", 4.5),
    ("Papel Higiénico Elite 4u", "Higiene", 8.5),
    ("Pasta Dental Colgate", "Higiene", 6.2),
    ("Desodorante Rexona", "Higiene", 10.5),
    ("Toalla Higiénica Nosotras 8u", "Higiene Femenina", 5.8),
    ("Detergente Ariel 500g", "Limpieza", 6.0),
    ("Lavavajilla Ayudín 500ml", "Limpieza", 5.0),
    ("Desinfectante Sapolio 1L", "Limpieza", 6.8),
    ("Escoba Vileda", "Limpieza", 10.0),
    ("Trapeador Flash", "Limpieza", 12.0),
    ("Pilates Energizer AA", "Varios", 4.5),
    ("Encendedor Clipper", "Varios", 3.0),
    ("Bolsa Plástica Grande", "Varios", 0.2),
    ("Huevos San Fernando x12", "Abarrotes", 8.8),
    ("Pollo Congelado 1kg", "Abarrotes", 13.5),
    ("Arvejas 500g", "Granos", 4.0),
    ("Lentejas 500g", "Granos", 4.2),
    ("Maíz Cancha 500g", "Granos", 3.5),
    ("Panetón D’onofrio 900g", "Temporada", 22.0),
    ("Vino Tabernero 750ml", "Bebidas Alcohólicas", 18.0),
    ("Cerveza Pilsen Botella", "Bebidas Alcohólicas", 6.0),
    ("Cerveza Cusqueña", "Bebidas Alcohólicas", 7.0),
    ("Ron Cartavio 750ml", "Bebidas Alcohólicas", 25.0),
    ("Pisco Quebranta 500ml", "Bebidas Alcohólicas", 28.0),
    ("Gaseosa Pepsi 1.5L", "Bebidas", 6.0),
    ("Gaseosa Coca Cola 1.5L", "Bebidas", 6.5),
    ("Helado D’onofrio Bombón", "Helados", 3.5),
    ("Helado D’onofrio Sandwich", "Helados", 3.8),
    ("Sal Rosada 1kg", "Condimentos", 6.0),
    ("Ketchup Heinz 397g", "Condimentos", 8.0),
    ("Mostaza Alacena 397g", "Condimentos", 7.5),
    ("Mayonesa Alacena 950g", "Condimentos", 10.0),
    ("Vinagre Blanco 1L", "Condimentos", 4.0),
    ("Salsa Soya 500ml", "Condimentos", 6.0),
    ("Salsa de Tomate Molitalia", "Condimentos", 5.0),
    ("Comino Molido 50g", "Condimentos", 1.5),
    ("Pimienta Negra 50g", "Condimentos", 1.5),
    ("Cereal Zucaritas 500g", "Desayuno", 8.5),
    ("Avena 3 Ositos 1kg", "Desayuno", 6.8),
    ("Gaseosa Sprite 500ml", "Bebidas", 3.5),
    ("Jugo Watts Durazno 1L", "Bebidas", 7.0),
    ("Jugo del Valle Mango 1L", "Bebidas", 7.5),
    ("Energizante Volt 500ml", "Bebidas", 6.5),
    ("Mermelada Gloria Fresa 250g", "Desayuno", 4.8),
    ("Te Hornimans Manzanilla", "Bebidas", 5.5),
    ("Café Altomayo 250g", "Desayuno", 14.0),
    ("Pan Frances x10u", "Panadería", 5.0),
    ("Té McCollins Canela", "Bebidas", 5.2),
    ("Yogurt Laive Durazno 1L", "Lácteos", 6.0),
    ("Chifles", "Snacks", 2.5),
    ("Maní Salado", "Snacks", 2.0)
]

# ============================================================
# 2. INSERTAR / ACTUALIZAR PRODUCTOS
# ============================================================

productos = []
for nombre, categoria, precio in productos_data:
    p = db.query(Producto).filter_by(nombre=nombre).first()
    if p:
        if p.precio != precio:
            p.precio = precio
        productos.append(p)
    else:
        nuevo = Producto(nombre=nombre, categoria=categoria, precio=precio)
        db.add(nuevo)
        productos.append(nuevo)

db.commit()
productos = db.query(Producto).all()

print(f"Productos totales en BD: {len(productos)}")

# ============================================================
# 3. DISTRIBUCIÓN REALISTA DE VENTAS
# ============================================================

pesos_categoria = {
    "Bebidas": 0.30,
    "Snacks": 0.15,
    "Dulces": 0.10,
    "Lácteos": 0.10,
    "Abarrotes": 0.10,
    "Conservas": 0.05,
    "Desayuno": 0.05,
    "Panadería": 0.05,
    "Higiene": 0.04,
    "Limpieza": 0.04,
    "Bebidas Alcohólicas": 0.02
}

# Asignar peso a cada producto según su categoría
pesos_productos = []
for p in productos:
    pesos_productos.append(pesos_categoria.get(p.categoria, 0.01))

# Normalizar
suma = sum(pesos_productos)
pesos_productos = [w / suma for w in pesos_productos]

# ============================================================
# 4. GENERACIÓN REALISTA DE TICKETS
# ============================================================

ventas = []
today = date.today()
ticket_id = 1

def items_por_ticket():
    r = random.random()
    if r < 0.60:
        return random.randint(1, 3)
    elif r < 0.90:
        return random.randint(4, 6)
    else:
        return random.randint(7, 10)

TOTAL_TICKETS = 90000  # entre 5000–10000 para apriori perfecto

for _ in range(TOTAL_TICKETS):

    n_items = items_por_ticket()

    # elegir productos según su peso realista
    productos_ticket = random.choices(
        productos,
        weights=pesos_productos,
        k=n_items
    )

    fecha_venta = today - timedelta(days=random.randint(0, 90))

    for prod in productos_ticket:
        cantidad = random.randint(1, 3)
        total = round(prod.precio * cantidad, 2)

        ventas.append(
            Venta(
                ticket_id=ticket_id,
                producto_id=prod.id,
                fecha=fecha_venta,
                cantidad=cantidad,
                total=total
            )
        )

    ticket_id += 1

db.add_all(ventas)
db.commit()
db.close()

print("Base de datos cargada con datos realistas 🚀")
