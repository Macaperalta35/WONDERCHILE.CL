import sqlite3
from werkzeug.security import generate_password_hash

# Conectar a la base de datos
conn = sqlite3.connect('wonderchile.db')
cursor = conn.cursor()

# Insertar usuarios de ejemplo
usuarios = [
    ('Admin User', 'admin@wonderchile.cl', generate_password_hash('admin123'), 'admin'),
    ('Juan Pérez', 'juan@example.com', generate_password_hash('password123'), 'user'),
    ('María González', 'maria@example.com', generate_password_hash('password123'), 'user'),
    ('Carlos Rodríguez', 'carlos@example.com', generate_password_hash('password123'), 'user')
]

cursor.executemany('INSERT OR IGNORE INTO usuarios (nombre, email, password, role) VALUES (?, ?, ?, ?)', usuarios)

# Insertar viajes de ejemplo
viajes = [
    ('Tour por Santiago', 'Descubre la capital de Chile con un tour guiado por los principales atractivos históricos y culturales.', 50000, '/static/uploads/tour_santiago.jpg'),
    ('Aventura en Cajón del Maipo', 'Explora el río y las montañas en una emocionante aventura de rafting y trekking.', 75000, '/static/uploads/cajon_maipo.jpg'),
    ('Viñedos de Maipo Valley', 'Degusta los mejores vinos chilenos en una visita a los viñedos más prestigiosos del valle.', 60000, '/static/uploads/vinedos_maipo.jpg'),
    ('Puerto Varas y Lagos', 'Relájate en los hermosos lagos del sur de Chile con vistas espectaculares.', 80000, '/static/uploads/puerto_varas.jpg'),
    ('Torres del Paine', 'Vive la experiencia única del parque nacional Torres del Paine con glaciares y fauna.', 120000, '/static/uploads/torres_paine.jpg'),
    ('Desierto de Atacama', 'Admira el desierto más árido del mundo con cielos estrellados y geiseres.', 95000, '/static/uploads/atacama.jpg'),
    ('Isla de Pascua', 'Explora las misteriosas estatuas moai en la isla más remota del mundo.', 150000, '/static/uploads/isla_pascua.jpg'),
    ('Valparaíso y Viña del Mar', 'Disfruta del encanto bohemio de Valparaíso y las playas de Viña del Mar.', 55000, '/static/uploads/valparaiso.jpg')
]

cursor.executemany('INSERT OR IGNORE INTO viajes (titulo, descripcion, precio, imagen) VALUES (?, ?, ?, ?)', viajes)

# Insertar giras de estudio
giras = [
    ('Gira Educativa', 'Experiencias de aprendizaje únicas para estudiantes de todos los niveles, combinando educación con aventura.', 150000, 'https://images.unsplash.com/photo-1523050854058-8df90110c9f1?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80', 'gira'),
    ('Intercambio Cultural', 'Programas de inmersión cultural que permiten a los estudiantes vivir experiencias auténticas en diferentes países.', 200000, 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80', 'gira'),
    ('Investigación Científica', 'Giras especializadas para estudiantes de ciencias que incluyen visitas a centros de investigación y laboratorios.', 180000, 'https://images.unsplash.com/photo-1469474968028-56623f02e42e?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80', 'gira'),
    ('Arte y Cultura', 'Exploración de museos, galerías y manifestaciones culturales en destinos seleccionados.', 120000, 'https://images.unsplash.com/photo-1503676260728-1c00da094a0b?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80', 'gira'),
    ('Idiomas en el Extranjero', 'Programas intensivos de aprendizaje de idiomas con inmersión cultural completa.', 250000, 'https://images.unsplash.com/photo-1551632436-cbf8dd35adfa?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80', 'gira'),
    ('Deportes y Aventura', 'Actividades deportivas y de aventura combinadas con aprendizaje y trabajo en equipo.', 160000, 'https://images.unsplash.com/photo-1544717297-fa95b6ee9643?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80', 'gira')
]

cursor.executemany('INSERT OR IGNORE INTO viajes (titulo, descripcion, precio, imagen, tipo) VALUES (?, ?, ?, ?, ?)', giras)

# Insertar viajes solo mujeres
mujeres = [
    ('Viaje Solo Mujeres Patagonia', 'Explora la Patagonia chilena en un viaje exclusivo para mujeres, con actividades de aventura y conexión con la naturaleza.', 180000, 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80', 'mujeres'),
    ('Retiro de Yoga en Viña del Mar', 'Un retiro espiritual y relajante en la costa chilena, diseñado exclusivamente para mujeres.', 120000, 'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80', 'mujeres'),
    ('Tour Cultural Santiago', 'Descubre la historia y cultura de Santiago en un tour guiado solo para mujeres.', 80000, 'https://images.unsplash.com/photo-1488646953014-85cb44e25828?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80', 'mujeres'),
    ('Aventura en Cajón del Maipo', 'Actividades de rafting y trekking en el Cajón del Maipo, en un entorno seguro y empoderador para mujeres.', 100000, 'https://images.unsplash.com/photo-1464207687429-7505649dae38?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80', 'mujeres'),
    ('Viaje de Empoderamiento Feminino', 'Un viaje transformador que combina aventura, cultura y empoderamiento personal para mujeres.', 150000, 'https://images.unsplash.com/photo-1527631746610-bca00a040d60?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80', 'mujeres'),
    ('Exploración del Desierto de Atacama', 'Descubre la magia del desierto más árido del mundo en un viaje exclusivo para mujeres.', 200000, 'https://images.unsplash.com/photo-1469474968028-56623f02e42e?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80', 'mujeres')
]

cursor.executemany('INSERT OR IGNORE INTO viajes (titulo, descripcion, precio, imagen, tipo) VALUES (?, ?, ?, ?, ?)', mujeres)

# Insertar promociones de ejemplo
promociones = [
    ('Descuento Verano', 'Aprovecha un 20% de descuento en todos los tours de verano. ¡No te lo pierdas!', 20.0, '/static/uploads/descuento_verano.jpg'),
    ('Paquete Familiar', 'Descuento especial del 15% para familias de 4 o más personas en viajes seleccionados.', 15.0, '/static/uploads/paquete_familiar.jpg'),
    ('Early Bird', 'Reserva con anticipación y obtén un 10% de descuento en tu próximo viaje.', 10.0, '/static/uploads/early_bird.jpg'),
    ('Viaje de Luna de Miel', 'Descuento romántico del 25% para parejas en su viaje de luna de miel.', 25.0, '/static/uploads/luna_miel.jpg'),
    ('Estudiante', 'Descuento del 12% para estudiantes con credencial válida en todos los paquetes.', 12.0, '/static/uploads/estudiante.jpg')
]

cursor.executemany('INSERT OR IGNORE INTO promociones (titulo, descripcion, descuento, imagen) VALUES (?, ?, ?, ?)', promociones)

# Insertar algunos contactos de ejemplo
contactos = [
    ('Ana López', 'ana@example.com', 'Estoy interesada en el tour por Santiago. ¿Pueden darme más información?'),
    ('Pedro Martínez', 'pedro@example.com', '¿Tienen disponibilidad para el mes de diciembre en Torres del Paine?'),
    ('Sofía Ramírez', 'sofia@example.com', 'Me gustaría organizar un viaje grupal para 10 personas. ¿Es posible?')
]

cursor.executemany('INSERT OR IGNORE INTO contactos (nombre, email, mensaje) VALUES (?, ?, ?)', contactos)

# Confirmar cambios
conn.commit()

# Cerrar conexión
conn.close()

print("Base de datos poblada exitosamente con datos de ejemplo.")
