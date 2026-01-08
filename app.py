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
app.secret_key = os.environ.get("SECRET_KEY", "clave_secreta_wonderchile")

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
# INICIALIZACIÓN BD + ADMIN
# --------------------------------------------------

def init_db():
    db = get_db()

    db.execute("""
    CREATE TABLE IF NOT EXISTS contactos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        email TEXT,
        mensaje TEXT,
        fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")

    db.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        email TEXT UNIQUE,
        password TEXT,
        role TEXT DEFAULT 'user',
        fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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

    db.execute("""
    CREATE TABLE IF NOT EXISTS carrito (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER,
        paquete TEXT,
        fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")

    # -------------------------
    # CREAR ADMIN AUTOMÁTICO
    # -------------------------
    admin_email = "admin@wonderchile.cl"
    admin_pass = generate_password_hash("Admin123")

    existe = db.execute(
        "SELECT id FROM usuarios WHERE email = ?", (admin_email,)
    ).fetchone()

    if not existe:
        db.execute("""
            INSERT INTO usuarios (nombre, email, password, role)
            VALUES (?, ?, ?, 'admin')
        """, ("Administrador", admin_email, admin_pass))
        logger.info("✔ Usuario ADMIN creado")

    # -------------------------
    # DATOS INICIALES VIAJES
    # -------------------------
    count = db.execute("SELECT COUNT(*) FROM viajes").fetchone()[0]
    if count == 0:
        viajes = [
            ("Tour Santiago", "City tour completo", 50000, ""),
            ("Cajón del Maipo", "Aventura en la cordillera", 75000, ""),
            ("Torres del Paine", "Experiencia Patagonia", 120000, "")
        ]
        db.executemany(
            "INSERT INTO viajes (titulo, descripcion, precio, imagen) VALUES (?, ?, ?, ?)",
            viajes
        )
        logger.info("✔ Viajes iniciales cargados")

    db.commit()
    db.close()

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
        viajes=viajes,
        user_name=session.get("user_name"),
        user_role=session.get("user_role")
    )

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        db = get_db()
        user = db.execute(
            "SELECT * FROM usuarios WHERE email = ?", (email,)
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

# --------------------------------------------------
# ADMIN
# --------------------------------------------------

def admin_required():
    return "user_id" in session and session.get("user_role") == "admin"

@app.route("/admin")
def admin():
    if not admin_required():
        return redirect(url_for("login"))
    return render_template("admin.html")

@app.route("/admin/viajes")
def admin_viajes():
    if not admin_required():
        return redirect(url_for("login"))
    db = get_db()
    viajes = db.execute("SELECT * FROM viajes").fetchall()
    return render_template("admin_viajes.html", viajes=viajes)

@app.route("/admin/viajes/agregar", methods=["GET", "POST"])
def agregar_viaje():
    if not admin_required():
        return redirect(url_for("login"))

    if request.method == "POST":
        titulo = request.form["titulo"]
        descripcion = request.form["descripcion"]
        precio = request.form["precio"]

        db = get_db()
        db.execute(
            "INSERT INTO viajes (titulo, descripcion, precio) VALUES (?, ?, ?)",
            (titulo, descripcion, precio)
        )
        db.commit()
        return redirect(url_for("admin_viajes"))

    return render_template("agregar_viaje.html")

@app.route("/admin/viajes/<int:id>/delete", methods=["POST"])
def eliminar_viaje(id):
    if not admin_required():
        return redirect(url_for("login"))

    db = get_db()
    db.execute("DELETE FROM viajes WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("admin_viajes"))

# --------------------------------------------------
# MAIN
# --------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)
