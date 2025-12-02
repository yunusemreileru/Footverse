// sidebar.js — V3 Stable Sidebar Controller

document.addEventListener("DOMContentLoaded", () => {

    const toggleBtn = document.getElementById("sidebar-toggle-btn");
    const body = document.body;

    if (!toggleBtn) return;

    /* ============================================================
       DESKTOP DAVRANIŞI — localStorage ile kalıcı sidebar state
    ============================================================ */

    const stored = localStorage.getItem("sidebarCollapsed");
    if (stored === "true") {
        body.classList.add("sidebar-collapsed");
    }

    toggleBtn.addEventListener("click", event => {
        event.stopPropagation();

        // Masaüstü toggle
        const isCollapsed = body.classList.toggle("sidebar-collapsed");
        localStorage.setItem("sidebarCollapsed", isCollapsed);

        // Mobilde aç-kapa davranışı (class: sidebar-open)
        body.classList.toggle("sidebar-open");
    });

    /* ============================================================
       MOBİL DAVRANIŞI — overlay tıklayınca kapat
    ============================================================ */

    document.addEventListener("click", () => {
        if (body.classList.contains("sidebar-open")) {
            body.classList.remove("sidebar-open");
        }
    });

    // Sidebar içinde tıklama propagation kapat
    const sidebar = document.getElementById("sidebar");
    if (sidebar) {
        sidebar.addEventListener("click", e => {
            e.stopPropagation();
        });
    }

    /* ============================================================
       ESC ile kapatma
    ============================================================ */
    document.addEventListener("keydown", e => {
        if (e.key === "Escape" && body.classList.contains("sidebar-open")) {
            body.classList.remove("sidebar-open");
        }
    });

    /* ============================================================
       Responsive davranış — geniş ekrana geçince mobil state reset
    ============================================================ */
    const mq = window.matchMedia("(min-width: 992px)");

    mq.addEventListener("change", e => {
        if (e.matches) {
            // Mobil açık sidebar desktop'ta kapanır
            body.classList.remove("sidebar-open");
        }
    });

});
