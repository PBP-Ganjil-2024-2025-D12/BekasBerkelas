document.addEventListener('DOMContentLoaded', () => {
    const btn = document.querySelector(".mobile-menu-button");
    const menu = document.querySelector(".mobile-menu");
    const hamburgerIcon = document.querySelector(".hamburger-icon");
    const xIcon = document.querySelector(".x-icon");

    if (btn) {
        btn.addEventListener("click", () => {
            menu.classList.toggle("hidden");
            
            if (menu.classList.contains("hidden")) {
                hamburgerIcon.classList.remove("hidden");
                xIcon.classList.add("hidden");
            } else {
                hamburgerIcon.classList.add("hidden");
                xIcon.classList.remove("hidden");
            }
        });
    }
});