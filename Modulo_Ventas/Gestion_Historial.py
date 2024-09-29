import sqlite3
from datetime import datetime

# Conexión a la base de datos SQLite
conn = sqlite3.connect('gestion_ventas.db')
cursor = conn.cursor()

# Crear las tablas si no existen
cursor.execute('''
CREATE TABLE IF NOT EXISTS vendedores (
    id_vendedor INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_vendedor TEXT NOT NULL
)
''')

cursor.execute('''
ALTER TABLE ventas ADD COLUMN id_vendedor INTEGER DEFAULT NULL
''')

conn.commit()

# Función para registrar una nueva venta (incluyendo vendedor)
def registrar_venta_con_vendedor(cliente, productos, forma_pago, id_vendedor, descuento_general=0):
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
    cursor.execute("INSERT INTO ventas (id_cliente, fecha_venta, forma_pago, total, descuento, total_con_descuento, id_vendedor) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (id_cliente, fecha_venta, forma_pago, total, descuento_general, total_final, id_vendedor))
    id_venta = cursor.lastrowid

    # Insertar los detalles de la venta
    for producto in productos:
        cursor.execute("INSERT INTO detalles_venta (id_venta, id_producto, cantidad, subtotal, descuento_producto, subtotal_con_descuento) VALUES (?, ?, ?, ?, ?, ?)",
                    (id_venta, producto['id_producto'], producto['cantidad'], 
                        producto['precio'] * producto['cantidad'], producto.get('descuento', 0), 
                        producto['subtotal_con_descuento']))

    conn.commit()
    print("Venta registrada con éxito por el vendedor ID:", id_vendedor)

# Función para consultar el historial de ventas por vendedor y por período
def consultar_historial_vendedor(id_vendedor, fecha_inicio, fecha_fin):
    cursor.execute('''
    SELECT v.id_venta, v.fecha_venta, c.nombre, v.total_con_descuento
    FROM ventas v
    JOIN clientes c ON v.id_cliente = c.id_cliente
    WHERE v.id_vendedor = ? AND v.fecha_venta BETWEEN ? AND ?
    ''', (id_vendedor, fecha_inicio, fecha_fin))

    ventas = cursor.fetchall()

    if ventas:
        print(f"Historial de ventas del vendedor {id_vendedor} entre {fecha_inicio} y {fecha_fin}:")
        for venta in ventas:
            print(f"Venta ID: {venta[0]}, Fecha: {venta[1]}, Cliente: {venta[2]}, Total con descuento: {venta[3]}")
    else:
        print(f"No se encontraron ventas para el vendedor {id_vendedor} en el período especificado.")

# Función para agregar un nuevo vendedor
def agregar_vendedor(nombre_vendedor):
    cursor.execute("INSERT INTO vendedores (nombre_vendedor) VALUES (?)", (nombre_vendedor,))
    conn.commit()
    print(f"Vendedor '{nombre_vendedor}' agregado con éxito.")

# Ejemplo de uso
# Agregar un nuevo vendedor
agregar_vendedor('Carlos Gómez')

# Registrar una venta
cliente_info = {
    'nombre': 'Ana Torres',
    'direccion': 'Calle Real 456',
    'telefono': '555-9876'
}

productos_vendidos = [
    {'id_producto': 1, 'precio': 50.00, 'cantidad': 2, 'descuento': 10},  # 10% de descuento en este producto
    {'id_producto': 2, 'precio': 30.00, 'cantidad': 1, 'descuento': 5}    # 5% de descuento en este producto
]

forma_pago = 'Tarjeta de débito'
id_vendedor = 1  # ID del vendedor Carlos Gómez

registrar_venta_con_vendedor(cliente_info, productos_vendidos, forma_pago, id_vendedor)

# Consultar historial de ventas del vendedor
fecha_inicio = '2023-01-01'
fecha_fin = '2023-12-31'
consultar_historial_vendedor(id_vendedor, fecha_inicio, fecha_fin)

# Cerrar conexión
conn.close()
