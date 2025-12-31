document.addEventListener("DOMContentLoaded", function () {

    // ----- MODAL -----
    const openBtn = document.getElementById("openTasks");
    const modal = document.getElementById("tasksModal");
    const closeBtn = document.getElementById("closeTasks");

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

    // ----- CSRF -----
    function getCSRFToken() {
        return document.querySelector('meta[name="csrf-token"]').getAttribute("content");
    }

    // ----- FILE INPUTS -----
    document.querySelectorAll(".task-card").forEach(task => {

        const input = task.querySelector(".folderInput");
        const countText = task.querySelector(".file-count");
        const sendBtn = task.querySelector(".send-btn");

        let selectedFiles = [];

        input.addEventListener("change", function () {
            selectedFiles = [...this.files];
            countText.textContent = `${selectedFiles.length} ficheiros selecionados`;
        });

        sendBtn.addEventListener("click", function () {
            if (selectedFiles.length === 0) {
                alert("Nenhum ficheiro selecionado");
                return;
            }

            const taskId = task.dataset.taskId;
            const formData = new FormData();

            formData.append("task_id", taskId);
            selectedFiles.forEach(file => {
                formData.append("files", file);
            });

            fetch("/upload-task-files/", {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCSRFToken()
                },
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                alert(`Ficheiros enviados para a task ${taskId}`);
            });
        });
    });
});