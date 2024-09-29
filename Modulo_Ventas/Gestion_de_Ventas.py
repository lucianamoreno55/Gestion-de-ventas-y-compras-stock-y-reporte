import sqlite3
from datetime import datetime

# Conexión a la base de datos SQLite
conn = sqlite3.connect('gestion_ventas.db')
cursor = conn.cursor()

# Crear las tablas si no existen
cursor.execute('''
CREATE TABLE IF NOT EXISTS clientes (
    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    direccion TEXT,
    telefono TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS productos (
    id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_producto TEXT NOT NULL,
    precio REAL NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS ventas (
    id_venta INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cliente INTEGER,
    fecha_venta TEXT NOT NULL,
    forma_pago TEXT NOT NULL,
    total REAL NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS detalles_venta (
    id_detalle INTEGER PRIMARY KEY AUTOINCREMENT,
    id_venta INTEGER,
    id_producto INTEGER,
    cantidad INTEGER NOT NULL,
    subtotal REAL NOT NULL,
    FOREIGN KEY (id_venta) REFERENCES ventas(id_venta),
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
)
''')

conn.commit()

# Función para registrar una nueva venta
def registrar_venta(cliente, productos, forma_pago):
    # Insertar cliente (o verificar si ya existe)
    cursor.execute("INSERT INTO clientes (nombre, direccion, telefono) VALUES (?, ?, ?)", 
                (cliente['nombre'], cliente['direccion'], cliente['telefono']))
    id_cliente = cursor.lastrowid

    # Obtener fecha actual
    fecha_venta = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Calcular total
    total = sum(p['precio'] * p['cantidad'] for p in productos)

    # Insertar la venta
    cursor.execute("INSERT INTO ventas (id_cliente, fecha_venta, forma_pago, total) VALUES (?, ?, ?, ?)",
                (id_cliente, fecha_venta, forma_pago, total))
    id_venta = cursor.lastrowid

    # Insertar los detalles de la venta
    for producto in productos:
        cursor.execute("INSERT INTO detalles_venta (id_venta, id_producto, cantidad, subtotal) VALUES (?, ?, ?, ?)",
                       (id_venta, producto['id_producto'], producto['cantidad'], producto['precio'] * producto['cantidad']))

    conn.commit()
    print("Venta registrada con éxito.")

# Ejemplo de uso
cliente_info = {
    'nombre': 'Juan Pérez',
    'direccion': 'Calle Falsa 123',
    'telefono': '555-1234'
}

productos_vendidos = [
    {'id_producto': 1, 'precio': 50.00, 'cantidad': 2},
    {'id_producto': 2, 'precio': 30.00, 'cantidad': 1}
]

forma_pago = 'Tarjeta de crédito'

registrar_venta(cliente_info, productos_vendidos, forma_pago)

# Cerrar conexión
conn.close()
