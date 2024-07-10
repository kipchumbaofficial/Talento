document.getElementById('menu-toggle').addEventListener('click', function() {
    document.getElementById('popup-menu').classList.remove('hidden');
});
document.getElementById('menu-close').addEventListener('click', function() {
    document.getElementById('popup-menu').classList.add('hidden');
});

// Close the menu if clicked outside
