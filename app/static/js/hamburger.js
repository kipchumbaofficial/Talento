document.getElementById('menu-toggle').addEventListener('click', function() {
    const menu = document.getElementById('popup-menu');
    if (menu.classList.contains('hidden')) {
        menu.classList.remove('hidden');
    } else {
        menu.classList.add('hidden');
    }
});

// Close the menu if clicked outside
window.addEventListener('click', function(e) {
    const menu = document.getElementById('popup-menu');
    const toggle = document.getElementById('menu-toggle');
    if (!menu.contains(e.target) && !toggle.contains(e.target)) {
        menu.classList.add('hidden');
    }
}); 