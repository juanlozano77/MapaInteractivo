// Función para cambiar el color del marcador al hacer clic
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.leaflet-marker-icon').forEach(function(marker) {
        marker.addEventListener('click', function() {
            if (marker.style.backgroundColor === 'blue') {
                marker.style.backgroundColor = 'white';
            } else {
                marker.style.backgroundColor = 'blue';
            }
        });
    });
});
