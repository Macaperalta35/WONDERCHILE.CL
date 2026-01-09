# Mejoras en el Backend TODO

## Mejoras de Seguridad
- [x] Implementar hash de contraseñas usando Werkzeug
- [x] Actualizar ruta de registro para hashear contraseñas
- [x] Actualizar ruta de login para verificar contraseñas hasheadas
- [x] Hashear la contraseña por defecto del admin

## Validación de Entrada y Manejo de Errores
- [x] Agregar validación de entrada para formularios (email, campos requeridos)
- [x] Agregar bloques try-except para operaciones de base de datos
- [x] Retornar respuestas de error apropiadas

## Logging
- [x] Agregar logging básico para solicitudes y errores

## Mejoras en la Base de Datos
- [x] Usar administradores de contexto para conexiones DB
- [x] Agregar nuevas tablas para viajes y promociones

## Características de Visualización de Usuario
- [x] Pasar nombre de usuario logueado a las plantillas
- [x] Actualizar plantillas para mostrar nombre de usuario si está logueado

## Gestión de Contenido (Viajes y Promociones)
- [x] Agregar rutas para admin para CRUD de viajes
- [x] Agregar rutas para admin para CRUD de promociones
- [x] Actualizar plantilla de admin para incluir secciones de gestión

## Organización del Código
- [x] Refactorizar código repetitivo
- [x] Agregar comentarios al código

## Dependencias
- [x] Actualizar requirements.txt con Werkzeug

## Mejoras en la Interfaz de Usuario
- [x] Agregar sección dedicada "Viajes Solo Mujeres" en la página principal
- [x] Agregar sección de términos y condiciones en la página de detalle de paquete
- [x] Agregar estilos CSS para la sección de términos y condiciones
- [x] Actualizar JavaScript para verificar aceptación de términos antes de agregar al carrito

## Pruebas
- [ ] Probar login, registro, carrito, funciones de admin
- [ ] Verificar que las nuevas características funcionen
