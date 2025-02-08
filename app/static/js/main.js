document.addEventListener('DOMContentLoaded', function () {
    const tiles = Array.from(document.querySelectorAll('.project-tile'));
    const backToTop = document.getElementById('back-to-top');

    // Sichtbarkeit des Back-to-Top-Buttons
    backToTop.style.display = 'none';
    window.addEventListener('scroll', function () {
        if (window.scrollY > 300) {
            backToTop.style.display = 'block';
        } else {
            backToTop.style.display = 'none';
        }
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

    setTimeout(function () {
        let flashMessages = document.getElementById("flash-messages");
        if (flashMessages) {
            flashMessages.style.transition = "opacity 0.5s ease-out";
            flashMessages.style.opacity = "0";
            setTimeout(() => flashMessages.remove(), 500);
        }
    }, 3000); // 3 Sekunden warten
});
