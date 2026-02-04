const dropzoneFinal = document.getElementById("dropzoneFinal");
const fileInputFinal = document.getElementById("fileInputFinal");
const previewFinal = document.getElementById("previewFinal");
let archivosFinales = [];


// CLICK abre explorador
dropzoneFinal.addEventListener("click", () => {
  fileInputFinal.click();
});

// ARCHIVOS SELECCIONADOS
fileInputFinal.addEventListener("change", (e) => {
  handleFilesFinal(e.target.files);
  fileInputFinal.value = ""; // permite volver a subir el mismo archivo
});

// DRAG & DROP
dropzoneFinal.addEventListener("dragover", (e) => {
  e.preventDefault();
  dropzoneFinal.classList.add("border-purple-600", "text-purple-700");
});

dropzoneFinal.addEventListener("dragleave", () => {
  dropzoneFinal.classList.remove("border-purple-600", "text-purple-700");
});

dropzoneFinal.addEventListener("drop", (e) => {
  e.preventDefault();
  dropzoneFinal.classList.remove("border-purple-600", "text-purple-700");
  handleFilesFinal(e.dataTransfer.files);
});

// ===============================
// MANEJO DE ARCHIVOS (FINAL)
// ===============================
function handleFilesFinal(files) {
  [...files].forEach(file => {

    if (!file.type.startsWith("image/")) return;

    // 🔴 GUARDA EL ARCHIVO REAL
    archivosFinales.push(file);

    const reader = new FileReader();

    reader.onload = (e) => {
      const index = archivosFinales.length - 1;

      const div = document.createElement("div");
      div.className = "relative group";

      div.innerHTML = `
        <img src="${e.target.result}"
             class="w-full h-32 object-cover rounded-lg border"/>

        <button type="button"
          class="absolute top-1 right-1 bg-red-600 text-white rounded-full
                 w-6 h-6 flex items-center justify-center text-xs
                 opacity-0 group-hover:opacity-100 transition">
          &times;
        </button>
      `;

      // ELIMINAR IMAGEN (DOM + ARRAY)
      div.querySelector("button").addEventListener("click", () => {
        archivosFinales.splice(index, 1);
        div.remove();
      });

      previewFinal.appendChild(div);
    };

    reader.readAsDataURL(file);
  });
}
