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

# --------------------------------------------------
# MAIN
# --------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
