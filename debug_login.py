import sqlite3
from werkzeug.security import check_password_hash

# Conectar a la base de datos
conn = sqlite3.connect('wonderchile.db')
cursor = conn.cursor()

# Obtener el usuario admin
cursor.execute('SELECT * FROM usuarios WHERE email = ?', ('admin@wonderchile.cl',))
user = cursor.fetchone()

if user:
    print(f"Usuario encontrado: {user}")
    # Verificar la contraseña
    if check_password_hash(user[3], 'admin123'):
        print("Contraseña correcta")
    else:
        print("Contraseña incorrecta")
else:
    print("Usuario no encontrado")

# Cerrar conexión
conn.close()
