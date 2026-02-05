document.addEventListener('DOMContentLoaded', function () {
    const tiles = Array.from(document.querySelectorAll('.project-tile'));
    const backToTop = document.getElementById('back-to-top');

    function updateViewportHeight() {
        document.documentElement.style.setProperty('--real-vh', `${window.innerHeight}px`);
    }

    // Beim Laden und bei Größenänderung aktualisieren
    window.addEventListener('resize', updateViewportHeight);
    window.addEventListener('orientationchange', updateViewportHeight);
    updateViewportHeight();

    // ===== MICROSOFT DYNAMICS INSPIRED SHAPES =====
    const shapes = document.createElement('div');
    shapes.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
        overflow: hidden;
    `;

    // Offizielle Microsoft Markenfarben (höhere Deckkraft für bessere Sichtbarkeit)
    const msColors = [
        'rgba(243, 79, 28, 0.25)',    // #F34F1C - Red/Orange (Office/Cloud)
        'rgba(127, 188, 0, 0.25)',    // #7FBC00 - Green (Xbox/Gaming)
        'rgba(1, 166, 240, 0.25)',    // #01A6F0 - Blue (Windows/Azure)
        'rgba(255, 186, 1, 0.25)',    // #FFBA01 - Yellow (Bing/Search)
        'rgba(232, 17, 35, 0.25)',    // #e81123 - Alt Red
        'rgba(0, 158, 73, 0.25)',     // #009e49 - Alt Green
        'rgba(0, 164, 239, 0.25)',    // #00a4ef - Alt Blue
        'rgba(255, 241, 0, 0.25)',    // #fff100 - Alt Yellow
        'rgba(104, 33, 122, 0.25)',   // #68217a - Purple (Ergänzung)
        'rgba(0, 188, 242, 0.25)'     // #00bcf2 - Cyan (Ergänzung)
    ];

    // Microsoft-typische Formen: Quadrate dominieren (wie Logo)
    for (let i = 0; i < 10; i++) {
        const shape = document.createElement('div');
        const isSquare = Math.random() > 0.2; // 80% Quadrate/Rechtecke (Microsoft-Logo Style)
        const width = isSquare ? Math.random() * 450 + 250 : Math.random() * 600 + 300; // Größere Formen
        const height = isSquare ? width : Math.random() * 450 + 250;

        shape.style.cssText = `
            position: absolute;
            width: ${width}px;
            height: ${height}px;
            background: ${msColors[i % msColors.length]};
            border-radius: ${isSquare ? '6px' : '50%'};
            top: ${Math.random() * 120 - 10}%;
            left: ${Math.random() * 120 - 10}%;
            transform: rotate(${Math.random() * 30 - 15}deg);
            box-shadow: 0 8px 20px ${msColors[i % msColors.length]};
        `;
        shape.setAttribute('data-speed', (Math.random() * 0.25 + 0.08).toFixed(2));
        shapes.appendChild(shape);
    }
    document.body.prepend(shapes);

    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        shapes.querySelectorAll('div').forEach(shape => {
            const speed = parseFloat(shape.getAttribute('data-speed'));
            const baseTransform = shape.style.transform.split('translateY')[0];
            shape.style.transform = `${baseTransform} translateY(${scrolled * speed}px)`;
        });
    });

    // ===== MODERNE BIDIREKTIONALE SCROLL REVEAL ANIMATIONEN =====
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -80px 0px'
    };

    // Bidirektionaler Observer für Sections mit Hysteresis
    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('revealed');
            } else if (entry.boundingClientRect.top > window.innerHeight ||
                entry.boundingClientRect.bottom < -100) {
                // Nur ausblenden wenn deutlich außerhalb des Viewports
                entry.target.classList.remove('revealed');
            }
        });
    }, observerOptions);

    // Sections mit Fade-In animieren
    const sections = document.querySelectorAll('.animate-section');
    sections.forEach(section => {
        section.classList.add('fade-in-section');
        revealObserver.observe(section);
    });

    // Bidirektionaler Stagger-Observer für Grid-Elemente
    const staggerObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            const items = entry.target.querySelectorAll('.stagger-item');

            if (entry.isIntersecting && entry.intersectionRatio > 0) {
                // Einblenden mit Stagger-Effekt
                items.forEach((item, index) => {
                    setTimeout(() => {
                        item.classList.add('revealed');
                    }, index * 60); // Schnellerer Delay
                });
            } else {
                // Ausblenden wenn nicht mehr sichtbar
                items.forEach(item => {
                    item.classList.remove('revealed');
                });
            }
        });
    }, { threshold: [0, 0.1], rootMargin: '0px 0px -50px 0px' });

    // Alle Grid-Container beobachten
    const gridContainers = document.querySelectorAll('.stagger-container');
    gridContainers.forEach(container => {
        staggerObserver.observe(container);
    });

    // ===== SECTION TITLE ANIMATIONS =====
    const titleObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            const h2 = entry.target.querySelector('h2.stagger-item');
            if (h2) {
                if (entry.isIntersecting) {
                    setTimeout(() => {
                        h2.classList.add('revealed');
                    }, 130);
                } else if (entry.boundingClientRect.top > window.innerHeight ||
                    entry.boundingClientRect.bottom < -100) {
                    // Nur ausblenden wenn deutlich außerhalb
                    h2.classList.remove('revealed');
                }
            }
        });
    }, { threshold: 0.15 });

    const sectionsWithTitles = document.querySelectorAll('.animate-section');
    sectionsWithTitles.forEach(section => {
        titleObserver.observe(section);
    });

    // ===== BACK TO TOP BUTTON =====
    backToTop.style.opacity = '0';
    backToTop.style.visibility = 'hidden';
    backToTop.style.transition = 'opacity 0.3s ease, visibility 0.3s ease, transform 0.3s ease';

    function updateBackToTopVisibility() {
        const scrolledEnough = window.scrollY > 300;
        const isModalOpen = document.body.classList.contains('overflow-hidden');

        if (scrolledEnough && !isModalOpen) {
            backToTop.style.opacity = '1';
            backToTop.style.visibility = 'visible';
        } else {
            backToTop.style.opacity = '0';
            backToTop.style.visibility = 'hidden';
        }
    }

    window.addEventListener('scroll', updateBackToTopVisibility);

    // MutationObserver für Body-Klassenänderungen (wenn Modals geöffnet/geschlossen werden)
    const bodyObserver = new MutationObserver(updateBackToTopVisibility);
    bodyObserver.observe(document.body, { attributes: true, attributeFilter: ['class'] });

    document.addEventListener('alpine:init', () => {
        Alpine.effect(() => {
            if (Alpine.store('openTile') !== null) {
                document.body.style.overflow = 'hidden';
            } else {
                document.body.style.overflow = '';
            }
        });
    });

    function updateActiveTile() {
        // Falls Desktopmodus (>=768px): entferne alle "active" und beende die Funktion
        if (window.innerWidth >= 768) {
            tiles.forEach(tile => tile.classList.remove('active'));
            return;
        }

        const viewportCenter = window.innerHeight / 2;
        let closestTile = null;
        let minDistance = Infinity;

        tiles.forEach(tile => {
            const rect = tile.getBoundingClientRect();
            const tileCenter = rect.top + rect.height / 2;
            const distance = Math.abs(tileCenter - viewportCenter);
            if (distance < minDistance) {
                minDistance = distance;
                closestTile = tile;
            }
        });

        // Setze die "active"-Klasse nur für die Kachel, die am nächsten zur Mitte liegt
        tiles.forEach(tile => tile.classList.remove('active'));
        if (closestTile) {
            closestTile.classList.add('active');
        }
    }

    // Initialer Aufruf und Aktualisierung bei Scroll und Resize
    updateActiveTile();
    window.addEventListener('scroll', updateActiveTile);
    window.addEventListener('resize', updateActiveTile);

    // ===== FLASH MESSAGES =====
    setTimeout(function () {
        let flashMessages = document.getElementById("flash-messages");
        if (flashMessages) {
            flashMessages.style.transition = "opacity 0.5s ease-out";
            flashMessages.style.opacity = "0";
            setTimeout(() => flashMessages.remove(), 500);
        }
    }, 3000); // 3 Sekunden warten
});

