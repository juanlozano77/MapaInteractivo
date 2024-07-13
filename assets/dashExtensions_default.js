window.dashExtensions = Object.assign({}, window.dashExtensions, {
    default: {
        function0: function(btn, map) {
            if (!btn.button.options) btn.button.options = {};
            if (btn.button.options.state === 'white') {
                btn.button.style.setProperty('background-color', 'aqua', 'important'); // Cambiar a blanco con !important
                btn.button.options.state = 'aqua'; // Actualizar estado
            } else {
                btn.button.style.setProperty('background-color', 'white', 'important'); // Cambiar a azul con !important
                btn.button.options.state = 'white'; // Actualizar estado
            }
        }

    }
});