// mobile-menu.js - Funcionalidad para menú móvil

document.addEventListener('DOMContentLoaded', () => {
    // Crear botón de menú móvil si no existe
    if (!document.getElementById('mobile-menu-btn')) {
        const header = document.querySelector('.page-header');
        if (header) {
            const mobileBtn = document.createElement('button');
            mobileBtn.id = 'mobile-menu-btn';
            mobileBtn.className = 'btn btn-secondary mobile-only';
            mobileBtn.innerHTML = '☰ Menú';
            mobileBtn.setAttribute('aria-label', 'Abrir menú de navegación');
            mobileBtn.setAttribute('aria-expanded', 'false');

            const controls = header.querySelector('.controls');
            if (controls) {
                controls.insertBefore(mobileBtn, controls.firstChild);
            } else {
                header.appendChild(mobileBtn);
            }

            // Toggle del menú móvil
            mobileBtn.addEventListener('click', () => {
                const sidebar = document.querySelector('.sidebar');
                if (sidebar) {
                    sidebar.classList.toggle('open');
                    const isOpen = sidebar.classList.contains('open');
                    mobileBtn.innerHTML = isOpen ? '✕ Cerrar' : '☰ Menú';
                    mobileBtn.setAttribute('aria-expanded', isOpen);
                }
            });

            // Cerrar menú al hacer clic fuera
            document.addEventListener('click', (e) => {
                const sidebar = document.querySelector('.sidebar');
                const mobileBtn = document.getElementById('mobile-menu-btn');

                if (sidebar && mobileBtn &&
                    !sidebar.contains(e.target) &&
                    !mobileBtn.contains(e.target) &&
                    sidebar.classList.contains('open')) {
                    sidebar.classList.remove('open');
                    mobileBtn.innerHTML = '☰ Menú';
                    mobileBtn.setAttribute('aria-expanded', 'false');
                }
            });
        }
    }

    // Agregar estilos para el botón móvil
    const style = document.createElement('style');
    style.textContent = `
        .mobile-only {
            display: none;
        }

        @media (max-width: 768px) {
            .mobile-only {
                display: inline-flex;
            }

            #mobile-menu-btn {
                position: fixed;
                bottom: 20px;
                right: 20px;
                z-index: 1000;
                border-radius: 50px;
                padding: 12px 20px;
                box-shadow: var(--shadow-lg);
                font-size: 14px;
                font-weight: 600;
            }

            .sidebar.open {
                transform: translateX(0);
            }
        }
    `;
    document.head.appendChild(style);

    // Mejorar accesibilidad de enlaces
    const links = document.querySelectorAll('a[href]');
    links.forEach(link => {
        if (!link.hasAttribute('aria-label') && link.textContent.trim()) {
            link.setAttribute('aria-label', link.textContent.trim());
        }
    });

    // Animación de entrada para cards
    const cards = document.querySelectorAll('.card');
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    cards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        observer.observe(card);
    });
});
