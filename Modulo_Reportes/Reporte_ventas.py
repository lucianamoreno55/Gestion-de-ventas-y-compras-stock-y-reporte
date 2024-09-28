import sqlite3
from datetime import datetime

# Conexión a la base de datos SQLite
conn = sqlite3.connect('gestion_ventas.db')
cursor = conn.cursor()

# Función para generar reporte por producto
def reporte_por_producto(nombre_producto):
    cursor.execute('''
        SELECT p.nombre, SUM(dv.cantidad) AS cantidad_vendida, SUM(dv.subtotal) AS total_vendido
        FROM detalles_venta dv
        JOIN productos p ON dv.id_producto = p.id_producto
        WHERE p.nombre = ?
        GROUP BY p.nombre
    ''', (nombre_producto,))
    reporte = cursor.fetchone()

    if reporte:
        print(f"Reporte de ventas para el producto '{nombre_producto}':")
        print(f"Cantidad vendida: {reporte[1]}")
        print(f"Total vendido: {reporte[2]:.2f}")
    else:
        print(f"No se encontraron ventas para el producto '{nombre_producto}'.")

# Función para generar reporte por vendedor
def reporte_por_vendedor(nombre_vendedor):
    cursor.execute('''
        SELECT c.nombre, SUM(v.total) AS total_vendido
        FROM ventas v
        JOIN clientes c ON v.id_cliente = c.id_cliente
        WHERE c.nombre = ?
        GROUP BY c.nombre
    ''', (nombre_vendedor,))
    reporte = cursor.fetchone()

    if reporte:
        print(f"Reporte de ventas para el vendedor '{nombre_vendedor}':")
        print(f"Total vendido: {reporte[1]:.2f}")
    else:
        print(f"No se encontraron ventas realizadas por '{nombre_vendedor}'.")

# Función para generar reporte por período de tiempo
def reporte_por_periodo(fecha_inicio, fecha_fin):
    cursor.execute('''
        SELECT v.fecha, SUM(v.total) AS total_vendido
        FROM ventas v
        WHERE v.fecha BETWEEN ? AND ?
        GROUP BY v.fecha
    ''', (fecha_inicio, fecha_fin))
    reportes = cursor.fetchall()

    if reportes:
        print(f"Reporte de ventas desde {fecha_inicio} hasta {fecha_fin}:")
        for reporte in reportes:
            print(f"Fecha: {reporte[0]} - Total vendido: {reporte[1]:.2f}")
    else:
        print(f"No se encontraron ventas en el período desde {fecha_inicio} hasta {fecha_fin}.")

# Ejemplo de uso de las funciones

# Generar reporte por producto
reporte_por_producto("Producto1")

# Generar reporte por vendedor
reporte_por_vendedor("Juan Pérez")

# Generar reporte por período de tiempo
fecha_inicio = "2024-09-01"
fecha_fin = "2024-09-30"
reporte_por_periodo(fecha_inicio, fecha_fin)

# Cerrar la conexión
conn.close()
