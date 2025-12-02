// static/main/js/sidebar.js

document.addEventListener("DOMContentLoaded", () => {
  const toggleBtn = document.getElementById("sidebar-toggle-btn");
  if (!toggleBtn) return;

  const body = document.body;

  /* DESKTOP DAVRANIŞI (MOBİL KAPALI) */

  // Sayfa açılınca localStorage’dan collapse durumu yükle
  const stored = localStorage.getItem("sidebarCollapsed");
  if (stored === "true") {
    body.classList.add("sidebar-collapsed");
  }

  toggleBtn.addEventListener("click", () => {
    body.classList.toggle("sidebar-collapsed");

    // Yeni durumu kaydet
    const collapsed = body.classList.contains("sidebar-collapsed");
    localStorage.setItem("sidebarCollapsed", collapsed);
  });
});
