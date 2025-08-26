document.addEventListener("DOMContentLoaded", function () {
    const root = document.documentElement;
    const toggleBtn = document.getElementById("themeToggle");
    const themeIcon = document.getElementById("themeIcon");
    const themeText = document.getElementById("themeText");

    let theme = localStorage.getItem("theme") || "light";
    setTheme(theme);

    toggleBtn.addEventListener("click", () => {
        theme = theme === "light" ? "dark" : "light";
        setTheme(theme);
        localStorage.setItem("theme", theme);
    });

    function setTheme(theme) {
        root.setAttribute("data-theme", theme);
        if (theme === "dark") {
            themeIcon.className = "bi bi-sun";
            themeText.textContent = "Світла";
        } else {
            themeIcon.className = "bi bi-moon";
            themeText.textContent = "Темна";
        }
    }
});
