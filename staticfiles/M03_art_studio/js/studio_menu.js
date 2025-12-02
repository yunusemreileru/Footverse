// studio_menu.js
document.addEventListener("DOMContentLoaded", function () {

    // Tüm menü item'lerini seçiyoruz
    const menuItems = document.querySelectorAll(".studio-menu-item-wrapper");

    let openMenu = null;

    menuItems.forEach(wrapper => {
        const button = wrapper.querySelector(".studio-menu-item");
        const submenu = wrapper.querySelector(".studio-submenu");

        // Aç-kapa işlemi
        button.addEventListener("click", function (event) {
            event.stopPropagation(); // sayfaya yayılmasın

            // Eğer aynı menü açıksa kapat
            if (openMenu === submenu) {
                submenu.classList.remove("open");
                openMenu = null;
                return;
            }

            // Başka açık menüyü kapat
            if (openMenu) {
                openMenu.classList.remove("open");
            }

            // Yeni menüyü aç
            submenu.classList.add("open");
            openMenu = submenu;
        });
    });

    // Menü dışına tıklayınca kapat
    document.addEventListener("click", function () {
        if (openMenu) {
            openMenu.classList.remove("open");
            openMenu = null;
        }
    });
});
