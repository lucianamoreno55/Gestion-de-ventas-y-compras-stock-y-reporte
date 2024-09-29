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
    descuento REAL NOT NULL DEFAULT 0,
    total_con_descuento REAL NOT NULL,
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
    descuento_producto REAL NOT NULL DEFAULT 0,
    subtotal_con_descuento REAL NOT NULL,
    FOREIGN KEY (id_venta) REFERENCES ventas(id_venta),
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
)
''')

conn.commit()

# Función para registrar una nueva venta con descuentos
def registrar_venta_con_descuento(cliente, productos, forma_pago, descuento_general=0):
    # Insertar cliente (o verificar si ya existe)
    cursor.execute("INSERT INTO clientes (nombre, direccion, telefono) VALUES (?, ?, ?)", 
                   (cliente['nombre'], cliente['direccion'], cliente['telefono']))
    id_cliente = cursor.lastrowid

    # Obtener fecha actual
    fecha_venta = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Calcular el total de la venta antes de descuentos
    total = sum(p['precio'] * p['cantidad'] for p in productos)

    # Aplicar descuentos individuales a los productos
    total_con_descuento = 0
    for producto in productos:
        descuento_producto = producto.get('descuento', 0)  # Descuento individual del producto
        subtotal = producto['precio'] * producto['cantidad']
        subtotal_con_descuento = subtotal * (1 - descuento_producto / 100)
        total_con_descuento += subtotal_con_descuento
        producto['subtotal_con_descuento'] = subtotal_con_descuento

    # Aplicar descuento general a la venta si es necesario
    total_final = total_con_descuento * (1 - descuento_general / 100)

    # Insertar la venta en la tabla `ventas`
    cursor.execute("INSERT INTO ventas (id_cliente, fecha_venta, forma_pago, total, descuento, total_con_descuento) VALUES (?, ?, ?, ?, ?, ?)",
                (id_cliente, fecha_venta, forma_pago, total, descuento_general, total_final))
    id_venta = cursor.lastrowid

    # Insertar los detalles de la venta
    for producto in productos:
        cursor.execute("INSERT INTO detalles_venta (id_venta, id_producto, cantidad, subtotal, descuento_producto, subtotal_con_descuento) VALUES (?, ?, ?, ?, ?, ?)",
                    (id_venta, producto['id_producto'], producto['cantidad'], 
                        producto['precio'] * producto['cantidad'], producto.get('descuento', 0), 
                        producto['subtotal_con_descuento']))

    conn.commit()
    print("Venta con descuento registrada con éxito.")

# Ejemplo de uso
cliente_info = {
    'nombre': 'Juan Pérez',
    'direccion': 'Calle Falsa 123',
    'telefono': '555-1234'
}

productos_vendidos = [
    {'id_producto': 1, 'precio': 50.00, 'cantidad': 2, 'descuento': 10},  # 10% de descuento en este producto
    {'id_producto': 2, 'precio': 30.00, 'cantidad': 1, 'descuento': 5}    # 5% de descuento en este producto
]

forma_pago = 'Tarjeta de crédito'
descuento_general = 5  # Descuento adicional del 5% en toda la venta

registrar_venta_con_descuento(cliente_info, productos_vendidos, forma_pago, descuento_general)

# Cerrar conexión
conn.close()
