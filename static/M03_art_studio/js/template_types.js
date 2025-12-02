document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".type-card-item").forEach(card => {
        
        card.addEventListener("click", () => {
            const url = card.dataset.detailUrl;
            if (url) {
                window.location.href = url;
            }
        });

    });
});