import sqlite3
import matplotlib.pyplot as plt

# Conexión a la base de datos SQLite
conn = sqlite3.connect('gestion_negocio.db')
cursor = conn.cursor()

# Crear tablas si no existen
cursor.execute('''
    CREATE TABLE IF NOT EXISTS ventas (
        id_venta INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TEXT NOT NULL,
        total REAL NOT NULL,
        id_cliente INTEGER,
        id_producto INTEGER,
        FOREIGN KEY(id_cliente) REFERENCES clientes(id_cliente),
        FOREIGN KEY(id_producto) REFERENCES productos(id_producto)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS clientes (
        id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS productos (
        id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        precio REAL NOT NULL,
        stock INTEGER NOT NULL
    )
''')

# Función para generar reportes personalizados con filtros
def generar_reporte(filtro_producto=None, filtro_cliente=None, filtro_fecha=None):
    query = '''
        SELECT v.fecha, p.nombre AS producto, c.nombre AS cliente, v.total
        FROM ventas v
        JOIN productos p ON v.id_producto = p.id_producto
        JOIN clientes c ON v.id_cliente = c.id_cliente
        WHERE 1=1
    '''
    params = []

    # Aplicar filtros personalizados
    if filtro_producto:
        query += " AND p.nombre = ?"
        params.append(filtro_producto)
    if filtro_cliente:
        query += " AND c.nombre = ?"
        params.append(filtro_cliente)
    if filtro_fecha:
        query += " AND v.fecha = ?"
        params.append(filtro_fecha)

    cursor.execute(query, params)
    resultados = cursor.fetchall()

    # Mostrar reporte en consola
    if resultados:
        print(f"Reporte personalizado:")
        for resultado in resultados:
            print(f"Fecha: {resultado[0]}, Producto: {resultado[1]}, Cliente: {resultado[2]}, Total: {resultado[3]:.2f}")
    else:
        print("No se encontraron resultados para los filtros aplicados.")

    return resultados

# Función para generar gráficos de ventas
def generar_grafico(resultados):
    if not resultados:
        print("No hay datos para generar un gráfico.")
        return

    fechas = [resultado[0] for resultado in resultados]
    totales = [resultado[3] for resultado in resultados]

    plt.figure(figsize=(10, 6))
    plt.bar(fechas, totales, color='skyblue')
    plt.xlabel('Fecha')
    plt.ylabel('Total Vendido')
    plt.title('Total de Ventas por Fecha')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Ejemplo de uso de las funciones

# Generar reporte personalizado
filtros = generar_reporte(filtro_producto="Producto1", filtro_cliente="Juan Pérez")

# Generar gráfico a partir de los resultados del reporte
generar_grafico(filtros)

# Cerrar la conexión
conn.close()
