import sqlite3
from datetime import datetime

# Conexión a la base de datos SQLite
conn = sqlite3.connect('gestion_compras.db')
cursor = conn.cursor()

# Crear tablas si no existen
cursor.execute('''
    CREATE TABLE IF NOT EXISTS proveedores (
        id_proveedor INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        contacto TEXT NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS compras (
        id_compra INTEGER PRIMARY KEY AUTOINCREMENT,
        id_proveedor INTEGER,
        fecha TEXT NOT NULL,
        total REAL NOT NULL,
        FOREIGN KEY(id_proveedor) REFERENCES proveedores(id_proveedor)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS detalles_compra (
        id_detalle INTEGER PRIMARY KEY AUTOINCREMENT,
        id_compra INTEGER,
        producto TEXT NOT NULL,
        cantidad INTEGER NOT NULL,
        precio_unitario REAL NOT NULL,
        subtotal REAL NOT NULL,
        FOREIGN KEY(id_compra) REFERENCES compras(id_compra)
    )
''')

# Función para generar reporte de compras por proveedor
def reporte_por_proveedor(nombre_proveedor):
    cursor.execute('''
        SELECT p.nombre, SUM(c.total) AS total_comprado
        FROM compras c
        JOIN proveedores p ON c.id_proveedor = p.id_proveedor
        WHERE p.nombre = ?
        GROUP BY p.nombre
    ''', (nombre_proveedor,))
    reporte = cursor.fetchone()

    if reporte:
        print(f"Reporte de compras para el proveedor '{nombre_proveedor}':")
        print(f"Total comprado: {reporte[1]:.2f}")
    else:
        print(f"No se encontraron compras para el proveedor '{nombre_proveedor}'.")

# Función para generar reporte de compras por período de tiempo
def reporte_por_fecha(fecha_inicio, fecha_fin):
    cursor.execute('''
        SELECT c.fecha, p.nombre, SUM(c.total) AS total_comprado
        FROM compras c
        JOIN proveedores p ON c.id_proveedor = p.id_proveedor
        WHERE c.fecha BETWEEN ? AND ?
        GROUP BY c.fecha, p.nombre
    ''', (fecha_inicio, fecha_fin))
    reportes = cursor.fetchall()

    if reportes:
        print(f"Reporte de compras desde {fecha_inicio} hasta {fecha_fin}:")
        for reporte in reportes:
            print(f"Fecha: {reporte[0]} - Proveedor: {reporte[1]} - Total comprado: {reporte[2]:.2f}")
    else:
        print(f"No se encontraron compras en el período desde {fecha_inicio} hasta {fecha_fin}.")

# Ejemplo de uso de las funciones

# Generar reporte por proveedor
reporte_por_proveedor("Proveedor1")

# Generar reporte por fecha
fecha_inicio = "2024-09-01"
fecha_fin = "2024-09-30"
reporte_por_fecha(fecha_inicio, fecha_fin)

# Cerrar la conexión
conn.close()