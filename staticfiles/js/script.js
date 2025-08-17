// Sidebar toggle
const toggleBtn = document.getElementById("sidebarToggle");
const sidebar = document.getElementById("leftSidebar");

toggleBtn.addEventListener("click", () => {
    sidebar.classList.toggle("hidden");
    sidebar.classList.toggle("show");
});