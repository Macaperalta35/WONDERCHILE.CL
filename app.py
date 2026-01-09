from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os
import logging
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

# --------------------------------------------------
# CONFIGURACIÓN GENERAL
# --------------------------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "clave_local_dev")

UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

DATABASE = "wonderchile.db"

# --------------------------------------------------
# UTILIDADES
# --------------------------------------------------
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

# --------------------------------------------------
# INICIALIZACIÓN BASE DE DATOS + ADMIN
# --------------------------------------------------
def crear_admin_por_defecto():
    db = get_db()

    admin_email = os.environ.get("ADMIN_EMAIL", "admin@wonderchile.cl")
    admin_password = os.environ.get("ADMIN_PASSWORD", "Admin123")

    existe = db.execute(
        "SELECT id FROM usuarios WHERE email = ?",
        (admin_email,)
    ).fetchone()

    if not existe:
        hashed_password = generate_password_hash(admin_password)
        db.execute("""
            INSERT INTO usuarios (nombre, email, password, role)
            VALUES (?, ?, ?, 'admin')
        """, ("Administrador", admin_email, hashed_password))
        db.commit()
        logger.info("Usuario admin creado correctamente")

def init_db():
    db = get_db()

    db.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        role TEXT DEFAULT 'user',
        fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")

    db.execute("""
    CREATE TABLE IF NOT EXISTS contactos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        email TEXT,
        mensaje TEXT,
        fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")

    db.execute("""
    CREATE TABLE IF NOT EXISTS viajes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT,
        descripcion TEXT,
        precio REAL,
        imagen TEXT
    )""")

    db.execute("""
    CREATE TABLE IF NOT EXISTS promociones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT,
        descripcion TEXT,
        descuento REAL,
        imagen TEXT
    )""")

    db.commit()
    crear_admin_por_defecto()

init_db()

# --------------------------------------------------
# RUTAS PÚBLICAS
# --------------------------------------------------
@app.route("/")
def home():
    db = get_db()
    viajes = db.execute("SELECT * FROM viajes").fetchall()
    return render_template(
        "index.html",
        user_name=session.get("user_name"),
        user_role=session.get("user_role"),
        viajes=viajes
    )

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        db = get_db()
        user = db.execute(
            "SELECT * FROM usuarios WHERE email = ?",
            (email,)
        ).fetchone()

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["user_name"] = user["nombre"]
            session["user_role"] = user["role"]
            return redirect(url_for("home"))

        return "Credenciales incorrectas"

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

@app.route("/paquetes")
def paquetes():
    db = get_db()
    viajes = db.execute("SELECT * FROM viajes").fetchall()
    return render_template("paquetes.html", viajes=viajes)

@app.route("/giras")
def giras():
    return render_template("giras.html")

@app.route("/mujeres")
def mujeres():
    return render_template("mujeres.html")

@app.route("/contacto")
def contacto():
    return render_template("contacto.html")

@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nombre = request.form["nombre"]
        email = request.form["email"]
        password = request.form["password"]

        db = get_db()
        hashed_password = generate_password_hash(password)
        try:
            db.execute(
                "INSERT INTO usuarios (nombre, email, password) VALUES (?, ?, ?)",
                (nombre, email, hashed_password)
            )
            db.commit()
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            return "Email ya registrado"

    return render_template("registro.html")

@app.route("/carrito")
def carrito():
    if not session.get("user_id"):
        return redirect(url_for("login"))
    return render_template("carrito.html")

@app.route("/paquete/<int:viaje_id>")
def detalle_paquete(viaje_id):
    db = get_db()
    viaje = db.execute("SELECT * FROM viajes WHERE id = ?", (viaje_id,)).fetchone()
    if not viaje:
        return "Paquete no encontrado", 404
    return render_template("detalle_paquete.html", viaje=viaje)

# --------------------------------------------------
# ADMIN
# --------------------------------------------------
@app.route("/admin")
def admin():
    if session.get("user_role") != "admin":
        return redirect(url_for("login"))
    return render_template("admin.html")

@app.route("/admin/viajes")
def admin_viajes():
    if session.get("user_role") != "admin":
        return redirect(url_for("login"))
    db = get_db()
    viajes = db.execute("SELECT * FROM viajes").fetchall()
    return render_template("admin_viajes.html", viajes=viajes)

@app.route("/admin/viajes/agregar", methods=["GET", "POST"])
def agregar_viaje():
    if session.get("user_role") != "admin":
        return redirect(url_for("login"))

    if request.method == "POST":
        titulo = request.form.get("titulo")
        descripcion = request.form.get("descripcion")
        precio = request.form.get("precio")
        imagen_opcion = request.form.get("imagen_opcion")

        if not titulo or not descripcion or not precio:
            return "Error: Todos los campos son obligatorios"

        imagen_path = None

        if imagen_opcion == "upload":
            if "imagen_file" not in request.files:
                return "Error: No se encontró el archivo de imagen"
            file = request.files["imagen_file"]
            if file.filename == "":
                return "Error: No se seleccionó ningún archivo"
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                file.save(file_path)
                imagen_path = f"/static/uploads/{filename}"
            else:
                return "Error: Tipo de archivo no permitido. Solo se permiten imágenes (png, jpg, jpeg, gif, webp)"
        else:
            imagen_path = request.form.get("imagen")

        db = get_db()
        db.execute(
            "INSERT INTO viajes (titulo, descripcion, precio, imagen) VALUES (?, ?, ?, ?)",
            (titulo, descripcion, precio, imagen_path)
        )
        db.commit()

        return redirect(url_for("admin_viajes"))

    return render_template("agregar_viaje.html")

@app.route("/admin/viajes/<int:viaje_id>/editar", methods=["GET", "POST"])
def editar_viaje(viaje_id):
    if session.get("user_role") != "admin":
        return redirect(url_for("login"))

    db = get_db()
    viaje = db.execute("SELECT * FROM viajes WHERE id = ?", (viaje_id,)).fetchone()

    if not viaje:
        return "Viaje no encontrado"

    if request.method == "POST":
        titulo = request.form.get("titulo")
        descripcion = request.form.get("descripcion")
        precio = request.form.get("precio")
        imagen_opcion = request.form.get("imagen_opcion")

        if not titulo or not descripcion or not precio:
            return "Error: Todos los campos son obligatorios"

        imagen_path = viaje["imagen"]

        if imagen_opcion == "upload":
            if "imagen_file" not in request.files:
                return "Error: No se encontró el archivo de imagen"
            file = request.files["imagen_file"]
            if file.filename == "":
                return "Error: No se seleccionó ningún archivo"
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                file.save(file_path)
                imagen_path = f"/static/uploads/{filename}"
            else:
                return "Error: Tipo de archivo no permitido. Solo se permiten imágenes (png, jpg, jpeg, gif, webp)"
        else:
            nueva_imagen = request.form.get("imagen")
            if nueva_imagen:
                imagen_path = nueva_imagen

        db.execute(
            "UPDATE viajes SET titulo = ?, descripcion = ?, precio = ?, imagen = ? WHERE id = ?",
            (titulo, descripcion, precio, imagen_path, viaje_id)
        )
        db.commit()

        return redirect(url_for("admin_viajes"))

    return render_template("editar_viaje.html", viaje=viaje)

@app.route("/admin/viajes/<int:viaje_id>/delete", methods=["POST"])
def eliminar_viaje(viaje_id):
    if session.get("user_role") != "admin":
        return redirect(url_for("login"))

    db = get_db()
    db.execute("DELETE FROM viajes WHERE id = ?", (viaje_id,))
    db.commit()

    return redirect(url_for("admin_viajes"))

@app.route("/admin/promociones")
def admin_promociones():
    if session.get("user_role") != "admin":
        return redirect(url_for("login"))
    db = get_db()
    promociones = db.execute("SELECT * FROM promociones").fetchall()
    return render_template("admin_promociones.html", promociones=promociones)

@app.route("/admin/promociones/agregar", methods=["GET", "POST"])
def agregar_promocion():
    if session.get("user_role") != "admin":
        return redirect(url_for("login"))

    if request.method == "POST":
        titulo = request.form.get("titulo")
        descripcion = request.form.get("descripcion")
        descuento = request.form.get("descuento")
        imagen_opcion = request.form.get("imagen_opcion")

        if not titulo or not descripcion or not descuento:
            return "Error: Todos los campos son obligatorios"

        imagen_path = None

        if imagen_opcion == "upload":
            if "imagen_file" not in request.files:
                return "Error: No se encontró el archivo de imagen"
            file = request.files["imagen_file"]
            if file.filename == "":
                return "Error: No se seleccionó ningún archivo"
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                file.save(file_path)
                imagen_path = f"/static/uploads/{filename}"
            else:
                return "Error: Tipo de archivo no permitido. Solo se permiten imágenes (png, jpg, jpeg, gif, webp)"
        else:
            imagen_path = request.form.get("imagen")

        db = get_db()
        db.execute(
            "INSERT INTO promociones (titulo, descripcion, descuento, imagen) VALUES (?, ?, ?, ?)",
            (titulo, descripcion, descuento, imagen_path)
        )
        db.commit()

        return redirect(url_for("admin_promociones"))

    return render_template("agregar_promocion.html")

@app.route("/admin/promociones/<int:promocion_id>/editar", methods=["GET", "POST"])
def editar_promocion(promocion_id):
    if session.get("user_role") != "admin":
        return redirect(url_for("login"))

    db = get_db()
    promocion = db.execute("SELECT * FROM promociones WHERE id = ?", (promocion_id,)).fetchone()

    if not promocion:
        return "Promoción no encontrada"

    if request.method == "POST":
        titulo = request.form.get("titulo")
        descripcion = request.form.get("descripcion")
        descuento = request.form.get("descuento")
        imagen_opcion = request.form.get("imagen_opcion")

        if not titulo or not descripcion or not descuento:
            return "Error: Todos los campos son obligatorios"

        imagen_path = promocion["imagen"]

        if imagen_opcion == "upload":
            if "imagen_file" not in request.files:
                return "Error: No se encontró el archivo de imagen"
            file = request.files["imagen_file"]
            if file.filename == "":
                return "Error: No se seleccionó ningún archivo"
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                file.save(file_path)
                imagen_path = f"/static/uploads/{filename}"
            else:
                return "Error: Tipo de archivo no permitido. Solo se permiten imágenes (png, jpg, jpeg, gif, webp)"
        else:
            nueva_imagen = request.form.get("imagen")
            if nueva_imagen:
                imagen_path = nueva_imagen

        db.execute(
            "UPDATE promociones SET titulo = ?, descripcion = ?, descuento = ?, imagen = ? WHERE id = ?",
            (titulo, descripcion, descuento, imagen_path, promocion_id)
        )
        db.commit()

        return redirect(url_for("admin_promociones"))

    return render_template("editar_promocion.html", promocion=promocion)

@app.route("/admin/promociones/<int:promocion_id>/delete", methods=["POST"])
def eliminar_promocion(promocion_id):
    if session.get("user_role") != "admin":
        return redirect(url_for("login"))

    db = get_db()
    db.execute("DELETE FROM promociones WHERE id = ?", (promocion_id,))
    db.commit()

    return redirect(url_for("admin_promociones"))

# --------------------------------------------------
# MAIN
# --------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
