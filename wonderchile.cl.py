from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3
import os
import logging
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'tu_clave_secreta_aqui')

# Configuración de uploads
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Crear directorio de uploads si no existe
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Configuración de la base de datos
DATABASE = 'wonderchile.db'

def get_db():
    """Get a database connection."""
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def get_db_connection():
    """Context manager for database connections."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    with app.app_context():
        db = get_db()
        db.execute('''CREATE TABLE IF NOT EXISTS contactos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT NOT NULL,
            mensaje TEXT NOT NULL,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        db.execute('''CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        db.execute('''CREATE TABLE IF NOT EXISTS carrito (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            paquete TEXT NOT NULL,
            fecha_agregado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
        )''')
        db.execute('''CREATE TABLE IF NOT EXISTS viajes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descripcion TEXT NOT NULL,
            precio REAL NOT NULL,
            imagen TEXT,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        db.execute('''CREATE TABLE IF NOT EXISTS promociones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descripcion TEXT NOT NULL,
            descuento REAL NOT NULL,
            imagen TEXT,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        db.commit()

@app.route('/')
def home():
    user_name = session.get('user_name') if 'user_id' in session else None
    user_role = session.get('user_role') if 'user_id' in session else None
    db = get_db()
    viajes = db.execute('SELECT * FROM viajes').fetchall()
    return render_template('index.html', user_name=user_name, user_role=user_role, viajes=viajes)

@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        mensaje = request.form['mensaje']

        if not nombre or not email or not mensaje:
            return "Error: Todos los campos son obligatorios"

        db = get_db()
        db.execute('INSERT INTO contactos (nombre, email, mensaje) VALUES (?, ?, ?)',
                   (nombre, email, mensaje))
        db.commit()
        return redirect(url_for('home'))

    return render_template('contacto.html')

@app.route('/paquetes')
def paquetes():
    db = get_db()
    viajes = db.execute('SELECT * FROM viajes').fetchall()
    return render_template('paquetes.html', viajes=viajes)

@app.route('/paquete/<int:viaje_id>')
def detalle_paquete(viaje_id):
    db = get_db()
    viaje = db.execute('SELECT * FROM viajes WHERE id = ?', (viaje_id,)).fetchone()
    if not viaje:
        return "Paquete no encontrado", 404
    return render_template('detalle_paquete.html', viaje=viaje)

@app.route('/giras')
def giras():
    return render_template('giras.html')

@app.route('/mujeres')
def mujeres():
    return render_template('mujeres.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password = request.form['password']

        if not nombre or not email or not password:
            return "Error: Todos los campos son obligatorios"

        hashed_password = generate_password_hash(password)

        db = get_db()
        try:
            db.execute('INSERT INTO usuarios (nombre, email, password) VALUES (?, ?, ?)',
                       (nombre, email, hashed_password))
            db.commit()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            return "Error: El email ya está registrado"

    return render_template('registro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if not email or not password:
            return "Error: Todos los campos son obligatorios"

        db = get_db()
        user = db.execute('SELECT * FROM usuarios WHERE email = ?', (email,)).fetchone()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['user_name'] = user['nombre']
            session['user_role'] = user['role']
            return redirect(url_for('home'))
        else:
            return "Error: Credenciales incorrectas"

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/carrito')
def carrito():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    db = get_db()
    items = db.execute('SELECT * FROM carrito WHERE usuario_id = ?', (session['user_id'],)).fetchall()
    return render_template('carrito.html', items=items)

@app.route('/admin')
def admin():
    if 'user_id' not in session or session.get('user_role') != 'admin':
        return redirect(url_for('login'))
    return render_template('admin.html')

@app.route('/admin/viajes')
def admin_viajes():
    if 'user_id' not in session or session.get('user_role') != 'admin':
        return redirect(url_for('login'))

    db = get_db()
    viajes = db.execute('SELECT * FROM viajes').fetchall()
    return render_template('admin_viajes.html', viajes=viajes)

@app.route('/admin/promociones')
def admin_promociones():
    if 'user_id' not in session or session.get('user_role') != 'admin':
        return redirect(url_for('login'))

    db = get_db()
    promociones = db.execute('SELECT * FROM promociones').fetchall()
    return render_template('admin_promociones.html', promociones=promociones)

@app.route('/admin/viajes/agregar', methods=['GET', 'POST'])
def agregar_viaje():
    if 'user_id' not in session or session.get('user_role') != 'admin':
        return redirect(url_for('login'))

    if request.method == 'POST':
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        imagen_opcion = request.form.get('imagen_opcion')

        if not titulo or not descripcion or not precio:
            return "Error: Todos los campos son obligatorios"

        imagen_path = None

        if imagen_opcion == 'upload':
            # Manejar subida de archivo
            if 'imagen_file' not in request.files:
                return "Error: No se encontró el archivo de imagen"
            file = request.files['imagen_file']
            if file.filename == '':
                return "Error: No se seleccionó ningún archivo"
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                imagen_path = f'/static/uploads/{filename}'
            else:
                return "Error: Tipo de archivo no permitido. Solo se permiten imágenes (png, jpg, jpeg, gif, webp)"
        else:
            # Usar URL
            imagen_path = request.form.get('imagen')

        db = get_db()
        db.execute('INSERT INTO viajes (titulo, descripcion, precio, imagen) VALUES (?, ?, ?, ?)',
                   (titulo, descripcion, precio, imagen_path))
        db.commit()
        return redirect(url_for('admin_viajes'))

    return render_template('agregar_viaje.html')

@app.route('/admin/promociones/agregar', methods=['GET', 'POST'])
def agregar_promocion():
    if 'user_id' not in session or session.get('user_role') != 'admin':
        return redirect(url_for('login'))

    if request.method == 'POST':
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']
        descuento = request.form['descuento']
        imagen_opcion = request.form.get('imagen_opcion')

        if not titulo or not descripcion or not descuento:
            return "Error: Todos los campos son obligatorios"

        imagen_path = None

        if imagen_opcion == 'upload':
            # Manejar subida de archivo
            if 'imagen_file' not in request.files:
                return "Error: No se encontró el archivo de imagen"
            file = request.files['imagen_file']
            if file.filename == '':
                return "Error: No se seleccionó ningún archivo"
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                imagen_path = f'/static/uploads/{filename}'
            else:
                return "Error: Tipo de archivo no permitido. Solo se permiten imágenes (png, jpg, jpeg, gif, webp)"
        else:
            # Usar URL
            imagen_path = request.form.get('imagen')

        db = get_db()
        db.execute('INSERT INTO promociones (titulo, descripcion, descuento, imagen) VALUES (?, ?, ?, ?)',
                   (titulo, descripcion, descuento, imagen_path))
        db.commit()
        return redirect(url_for('admin_promociones'))

    return render_template('agregar_promocion.html')

@app.route('/admin/viajes/<int:viaje_id>/editar', methods=['GET', 'POST'])
def editar_viaje(viaje_id):
    if 'user_id' not in session or session.get('user_role') != 'admin':
        return redirect(url_for('login'))

    db = get_db()
    viaje = db.execute('SELECT * FROM viajes WHERE id = ?', (viaje_id,)).fetchone()
    if not viaje:
        return "Viaje no encontrado"

    if request.method == 'POST':
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        imagen_opcion = request.form.get('imagen_opcion')

        if not titulo or not descripcion or not precio:
            return "Error: Todos los campos son obligatorios"

        imagen_path = viaje['imagen']  # Mantener imagen actual por defecto

        if imagen_opcion == 'upload':
            # Manejar subida de archivo
            if 'imagen_file' not in request.files:
                return "Error: No se encontró el archivo de imagen"
            file = request.files['imagen_file']
            if file.filename == '':
                return "Error: No se seleccionó ningún archivo"
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                imagen_path = f'/static/uploads/{filename}'
            else:
                return "Error: Tipo de archivo no permitido. Solo se permiten imágenes (png, jpg, jpeg, gif, webp)"
        else:
            # Usar URL
            nueva_imagen = request.form.get('imagen')
            if nueva_imagen:
                imagen_path = nueva_imagen

        db.execute('UPDATE viajes SET titulo = ?, descripcion = ?, precio = ?, imagen = ? WHERE id = ?',
                   (titulo, descripcion, precio, imagen_path, viaje_id))
        db.commit()
        return redirect(url_for('admin_viajes'))

    return render_template('editar_viaje.html', viaje=viaje)

@app.route('/admin/promociones/<int:promocion_id>/editar', methods=['GET', 'POST'])
def editar_promocion(promocion_id):
    if 'user_id' not in session or session.get('user_role') != 'admin':
        return redirect(url_for('login'))

    db = get_db()
    promocion = db.execute('SELECT * FROM promociones WHERE id = ?', (promocion_id,)).fetchone()
    if not promocion:
        return "Promoción no encontrada"

    if request.method == 'POST':
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']
        descuento = request.form['descuento']
        imagen_opcion = request.form.get('imagen_opcion')

        if not titulo or not descripcion or not descuento:
            return "Error: Todos los campos son obligatorios"

        imagen_path = promocion['imagen']  # Mantener imagen actual por defecto

        if imagen_opcion == 'upload':
            # Manejar subida de archivo
            if 'imagen_file' not in request.files:
                return "Error: No se encontró el archivo de imagen"
            file = request.files['imagen_file']
            if file.filename == '':
                return "Error: No se seleccionó ningún archivo"
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                imagen_path = f'/static/uploads/{filename}'
            else:
                return "Error: Tipo de archivo no permitido. Solo se permiten imágenes (png, jpg, jpeg, gif, webp)"
        else:
            # Usar URL
            nueva_imagen = request.form.get('imagen')
            if nueva_imagen:
                imagen_path = nueva_imagen

        db.execute('UPDATE promociones SET titulo = ?, descripcion = ?, descuento = ?, imagen = ? WHERE id = ?',
                   (titulo, descripcion, descuento, imagen_path, promocion_id))
        db.commit()
        return redirect(url_for('admin_promociones'))

    return render_template('editar_promocion.html', promocion=promocion)

@app.route('/admin/viajes/<int:viaje_id>/delete', methods=['POST'])
def eliminar_viaje(viaje_id):
    if 'user_id' not in session or session.get('user_role') != 'admin':
        return redirect(url_for('login'))

    db = get_db()
    db.execute('DELETE FROM viajes WHERE id = ?', (viaje_id,))
    db.commit()

    return redirect(url_for('admin_viajes'))

@app.route('/admin/promociones/<int:promocion_id>/delete', methods=['POST'])
def eliminar_promocion(promocion_id):
    if 'user_id' not in session or session.get('user_role') != 'admin':
        return redirect(url_for('login'))

    db = get_db()
    db.execute('DELETE FROM promociones WHERE id = ?', (promocion_id,))
    db.commit()

    return redirect(url_for('admin_promociones'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
