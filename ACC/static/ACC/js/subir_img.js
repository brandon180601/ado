const dropzone = document.getElementById("dropzone");
const fileInput = document.getElementById("fileInput");
const preview = document.getElementById("preview");

// CLICK abre explorador
dropzone.addEventListener("click", () => {
    fileInput.click();
});

// ARCHIVOS SELECCIONADOS
fileInput.addEventListener("change", (e) => {
    handleFiles(e.target.files);
});

// DRAG & DROP
dropzone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropzone.classList.add("border-purple-600", "text-purple-700");
});

dropzone.addEventListener("dragleave", () => {
    dropzone.classList.remove("border-purple-600", "text-purple-700");
});

dropzone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropzone.classList.remove("border-purple-600", "text-purple-700");
    handleFiles(e.dataTransfer.files);
});

function handleFiles(files) {
    [...files].forEach(file => {
        if (!file.type.startsWith("image/")) return;

        const reader = new FileReader();
        reader.onload = (e) => {
            const div = document.createElement("div");
            div.className = "relative group";

            div.innerHTML = `
              <img src="${e.target.result}"
                  class="w-full h-32 object-cover rounded-lg border"/>

              <button
                class="absolute top-1 right-1 bg-red-600 text-white rounded-full w-6 h-6
                      flex items-center justify-center text-xs opacity-0 group-hover:opacity-100
                      transition"
              >
                &times;
              </button>
            `;

            // ELIMINAR IMAGEN
            div.querySelector("button").addEventListener("click", () => {
                div.remove();
            });

            preview.appendChild(div);
        };

        reader.readAsDataURL(file);
    });
}

