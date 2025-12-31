const openBtn = document.getElementById("openProfile");
const modal = document.getElementById("profileModal");
const closeBtn = document.getElementById("closeProfile");

openBtn.addEventListener("click", function (e) {
    e.preventDefault();
    modal.style.display = "block";
});

closeBtn.addEventListener("click", function () {
    modal.style.display = "none";
});

window.addEventListener("click", function (e) {
    if (e.target === modal) {
    modal.style.display = "none";
    }
});