import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect('wonderchile.db')
cursor = conn.cursor()

# Contar registros en cada tabla
tables = ['usuarios', 'viajes', 'promociones', 'contactos']
for table in tables:
    cursor.execute(f'SELECT COUNT(*) FROM {table}')
    count = cursor.fetchone()[0]
    print(f'{table.capitalize()}: {count} registros')

# Cerrar conexión
conn.close()
