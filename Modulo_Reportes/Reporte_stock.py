import sqlite3

# Conexión a la base de datos SQLite
conn = sqlite3.connect('gestion_inventario.db')
cursor = conn.cursor()

# Crear tablas si no existen
cursor.execute('''
    CREATE TABLE IF NOT EXISTS categorias (
        id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS almacenes (
        id_almacen INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        ubicacion TEXT NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS productos (
        id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        stock INTEGER NOT NULL,
        id_categoria INTEGER,
        id_almacen INTEGER,
        FOREIGN KEY(id_categoria) REFERENCES categorias(id_categoria),
        FOREIGN KEY(id_almacen) REFERENCES almacenes(id_almacen)
    )
''')

# Función para generar reporte de stock por categoría
def reporte_por_categoria(nombre_categoria):
    cursor.execute('''
        SELECT c.nombre, p.nombre, p.stock
        FROM productos p
        JOIN categorias c ON p.id_categoria = c.id_categoria
        WHERE c.nombre = ?
    ''', (nombre_categoria,))
    productos = cursor.fetchall()

    if productos:
        print(f"Reporte de stock para la categoría '{nombre_categoria}':")
        for producto in productos:
            print(f"Producto: {producto[1]} - Stock: {producto[2]}")
    else:
        print(f"No se encontraron productos en la categoría '{nombre_categoria}'.")

# Función para generar reporte de stock por almacén
def reporte_por_almacen(nombre_almacen):
    cursor.execute('''
        SELECT a.nombre, p.nombre, p.stock
        FROM productos p
        JOIN almacenes a ON p.id_almacen = a.id_almacen
        WHERE a.nombre = ?
    ''', (nombre_almacen,))
    productos = cursor.fetchall()

    if productos:
        print(f"Reporte de stock para el almacén '{nombre_almacen}':")
        for producto in productos:
            print(f"Producto: {producto[1]} - Stock: {producto[2]}")
    else:
        print(f"No se encontraron productos en el almacén '{nombre_almacen}'.")

# Ejemplo de uso de las funciones

# Generar reporte por categoría
reporte_por_categoria("Electrónica")

# Generar reporte por almacén
reporte_por_almacen("Almacén Central")

# Cerrar la conexión
conn.close()