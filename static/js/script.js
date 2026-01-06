// Función para agregar al carrito
function agregarAlCarrito(paquete) {
    // Verificar si el usuario está logueado haciendo una petición al servidor
    fetch('/verificar_sesion')
    .then(response => response.json())
    .then(data => {
        if (!data.logged_in) {
            alert('Debes iniciar sesión para agregar productos al carrito');
            window.location.href = '/login';
            return;
        }

        // Enviar solicitud al servidor para agregar al carrito
        return fetch('/agregar_carrito', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ paquete: paquete })
        });
    })
    .then(response => {
        if (response) {
            return response.json();
        }
    })
    .then(data => {
        if (data && data.success) {
            alert('¡Producto agregado al carrito!');
        } else if (data) {
            alert('Error al agregar al carrito: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error al procesar la solicitud');
    });
}

// Función para toggle del menú hamburguesa
function toggleMenu() {
    const navMenu = document.getElementById('nav-menu');
    navMenu.classList.toggle('show');
}

// Cerrar menú al hacer clic fuera de él
document.addEventListener('click', function(event) {
    const nav = document.querySelector('nav');
    const navMenu = document.getElementById('nav-menu');
    const menuToggle = document.querySelector('.menu-toggle');

    if (!nav.contains(event.target)) {
        navMenu.classList.remove('show');
    }
});

// Función para toggle del menú desplegable de admin
function toggleAdminDropdown() {
    const dropdownContent = document.querySelector('.dropdown-content');
    dropdownContent.classList.toggle('show');
}

// Cerrar menú desplegable al hacer clic fuera de él
document.addEventListener('click', function(event) {
    const dropdown = document.querySelector('.dropdown');
    const dropdownContent = document.querySelector('.dropdown-content');

    if (dropdown && dropdownContent && !dropdown.contains(event.target)) {
        dropdownContent.classList.remove('show');
    }
});

// Función para cargar fotos de Instagram
function cargarFotosInstagram() {
    const instagramContainer = document.getElementById('instagram-photos');

    // Fotos de ejemplo (simulando Instagram)
    const fotosEjemplo = [
        'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80',
        'https://images.unsplash.com/photo-1469474968028-56623f02e42e?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80',
        'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80',
        'https://images.unsplash.com/photo-1589904205597-7cf0143c4d86?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80',
        'https://images.unsplash.com/photo-1516483638261-f4dbaf036963?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80',
        'https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80'
    ];

    fotosEjemplo.forEach((foto, index) => {
        const card = document.createElement('div');
        card.className = 'card instagram-card';
        card.innerHTML = `
            <img src="${foto}" alt="Foto Instagram ${index + 1}" loading="lazy">
            <div class="card-content">
                <p>✨ Experiencia inolvidable</p>
            </div>
        `;
        instagramContainer.appendChild(card);
    });
}

// Cargar fotos de Instagram cuando la página se carga
document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('instagram-photos')) {
        cargarFotosInstagram();
    }
});
