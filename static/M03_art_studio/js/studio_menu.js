// studio_menu.js — Theme Engine v3 (Stable Menu Controller)

document.addEventListener("DOMContentLoaded", () => {

    const menuItems = document.querySelectorAll(".studio-menu-item-wrapper");
    let openMenu = null;

    menuItems.forEach(wrapper => {
        const button = wrapper.querySelector(".studio-menu-item");
        const submenu = wrapper.querySelector(".studio-submenu");

        if (!button || !submenu) return;

        // Toggle submenu
        button.addEventListener("click", event => {
            event.stopPropagation();

            // Eğer aynı menü açıksa kapat
            if (openMenu === submenu) {
                submenu.classList.remove("open");
                openMenu = null;
                return;
            }

            // Başka açık menü varsa kapat
            if (openMenu && openMenu !== submenu) {
                openMenu.classList.remove("open");
            }

            // Yeni menüyü aç
            submenu.classList.add("open");
            openMenu = submenu;
        });

        // Submenu içindeki tıklamalar menüyü kapatmamalı
        submenu.addEventListener("click", event => {
            event.stopPropagation();
        });
    });

    // Herhangi bir yere tıklayınca kapat
    document.addEventListener("click", () => {
        if (openMenu) {
            openMenu.classList.remove("open");
            openMenu = null;
        }
    });

    // ESC ile kapat
    document.addEventListener("keydown", e => {
        if (e.key === "Escape" && openMenu) {
            openMenu.classList.remove("open");
            openMenu = null;
        }
    });
});
