document.addEventListener('DOMContentLoaded', function() {
    const navLinks = document.querySelectorAll('.nav-link');
    const navIndicator = document.querySelector('.nav-indicator');

    function updateNavIndicator(link) {
        navIndicator.style.width = `${link.offsetWidth}px`;
        navIndicator.style.transform = `translateX(${link.offsetLeft}px)`;
        navIndicator.style.opacity = '1';
    }

    navLinks.forEach(link => {
        if (link.classList.contains('active')) {
            updateNavIndicator(link);
        }

        link.addEventListener('mouseenter', () => {
            updateNavIndicator(link);
        });
    });

    const navLinksContainer = document.querySelector('.nav-links');
    navLinksContainer.addEventListener('mouseleave', () => {
        const activeLink = document.querySelector('.nav-link.active');
        if (activeLink) {
            updateNavIndicator(activeLink);
        } else {
            navIndicator.style.opacity = '0';
        }
    });
}); 