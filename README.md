# WonderChile - Turismo en Chile y el Mundo

Este es un sitio web para promocionar el turismo en Chile y destinos alrededor del mundo, construido con Flask y SQLite.

## Características

- Página de inicio con destinos turísticos populares
- Sección de actividades
- Formulario de contacto con almacenamiento en base de datos
- Diseño responsivo

## Tecnologías Utilizadas

- **Framework:** Flask (Python)
- **Base de Datos:** SQLite
- **Frontend:** HTML5, CSS3

## Instalación Local

1. Clona o descarga el proyecto
2. Instala las dependencias:
   ```
   pip install -r requirements.txt
   ```
3. Ejecuta la aplicación:
   ```
   python wonderchile.cl.py
   ```
4. Abre tu navegador en `http://localhost:5000`

## Despliegue

### Opción 1: Hosting con Soporte Python (Recomendado)

Para el hosting https://bdwihdylasiqtd.autocoder.cc/, recomendamos usar un servicio que soporte aplicaciones Python como:

- **Heroku** (gratuito para principiantes)
- **PythonAnywhere** (especializado en Python)
- **Vercel** o **Netlify** con serverless functions
- **Railway** o **Render**

### Opción 2: Convertir a PHP/MySQL (si el hosting no soporta Python)

Si el hosting solo soporta PHP, podemos convertir la aplicación a PHP con MySQL.

### Configuración para Despliegue

1. Asegúrate de que el hosting tenga Python 3.8+
2. Instala las dependencias desde requirements.txt
3. Configura la variable de entorno `FLASK_ENV=production`
4. El archivo principal es `wonderchile.cl.py`

## Estructura del Proyecto

```
wonderchile/
├── wonderchile.cl.py    # Aplicación Flask principal
├── requirements.txt     # Dependencias Python
├── templates/           # Plantillas HTML
│   ├── index.html
│   └── contacto.html
└── wonderchile.db       # Base de datos SQLite (se crea automáticamente)
```
admin_email = "admin@wonderchile.cl"
    admin_password = generate_password_hash("Admin123")

## Base de Datos

La aplicación utiliza SQLite para almacenar los mensajes de contacto. La base de datos se crea automáticamente al ejecutar la aplicación por primera vez.