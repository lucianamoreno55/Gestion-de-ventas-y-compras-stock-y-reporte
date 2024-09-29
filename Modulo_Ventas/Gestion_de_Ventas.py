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

# Función para agregar productos a la tabla productos
def agregar_producto(nombre_producto, precio):
    cursor.execute("INSERT INTO productos (nombre_producto, precio) VALUES (?, ?)", (nombre_producto, precio))
    conn.commit()
    print(f"Producto '{nombre_producto}' agregado con éxito.")

# Función para registrar una nueva venta
def registrar_venta(cliente, productos, forma_pago):
    try:
        # Insertar cliente (o verificar si ya existe)
        cursor.execute("INSERT INTO clientes (nombre, direccion, telefono) VALUES (?, ?, ?)", 
                        (cliente['nombre'], cliente['direccion'], cliente['telefono']))
        id_cliente = cursor.lastrowid
        print(f"Cliente registrado con ID: {id_cliente}")

        # Obtener fecha actual
        fecha_venta = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Calcular total
        total = sum(p['precio'] * p['cantidad'] for p in productos)

        # Insertar la venta
        cursor.execute("INSERT INTO ventas (id_cliente, fecha_venta, forma_pago, total) VALUES (?, ?, ?, ?)",
                        (id_cliente, fecha_venta, forma_pago, total))
        id_venta = cursor.lastrowid
        print(f"Venta registrada con ID: {id_venta}")

        # Insertar los detalles de la venta
        for producto in productos:
            cursor.execute("INSERT INTO detalles_venta (id_venta, id_producto, cantidad, subtotal) VALUES (?, ?, ?, ?)",
                           (id_venta, producto['id_producto'], producto['cantidad'], producto['precio'] * producto['cantidad']))
        conn.commit()
        print("Venta registrada con éxito.")

    except sqlite3.Error as e:
        print(f"Error en la base de datos: {e}")
        conn.rollback()

# Agregar productos a la tabla de productos
agregar_producto('Producto 1', 50.00)
agregar_producto('Producto 2', 30.00)

# Ejemplo de uso para registrar una venta
cliente_info = {
    'nombre': 'Juan Pérez',
    'direccion': 'Calle Falsa 123',
    'telefono': '555-1234'
}

# Los productos vendidos deben tener ID de productos válidos que existan en la tabla 'productos'
productos_vendidos = [
    {'id_producto': 1, 'precio': 50.00, 'cantidad': 2},  # Producto 1 con cantidad 2
    {'id_producto': 2, 'precio': 30.00, 'cantidad': 1}   # Producto 2 con cantidad 1
]

forma_pago = 'Tarjeta de crédito'

# Registrar la venta
registrar_venta(cliente_info, productos_vendidos, forma_pago)

# Cerrar conexión
conn.close()
