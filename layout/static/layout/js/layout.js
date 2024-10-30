document.addEventListener('DOMContentLoaded', function () {
    var menuItems = document.querySelectorAll('.menu-item');

    menuItems.forEach(function (menuItem) {
        menuItem.addEventListener('click', function (e) {
            e.stopPropagation();
            var submenu = this.querySelector('.submenu');
            var isVisible = submenu.style.display === 'block';

            // Đóng tất cả các submenu khác
            document.querySelectorAll('.submenu').forEach(function (el) {
                el.style.display = 'none';
            });

            // Mở hoặc đóng submenu của mục được nhấp
            submenu.style.display = isVisible ? 'none' : 'block';
        });
    });

    // Đóng submenu khi click bên ngoài
    document.addEventListener('click', function () {
        document.querySelectorAll('.submenu').forEach(function (el) {
            el.style.display = 'none';
        });
    });
});
