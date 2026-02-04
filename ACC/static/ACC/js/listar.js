const economicoInput = document.getElementById("economicoInput");
economicoInput.addEventListener("blur", function () {
    const economico = this.value.trim();

    if (!economico) return;

    fetch(`/buscar-autobus/?economico=${economico}`)
        .then(response => response.json())
        .then(data => {
            if (data.existe) {
                document.getElementById("tipoUnidad").value = data.tipo_unidad;
                document.getElementById("noObra").value = data.no_obra;
                document.getElementById("serie").value = data.serie;
                document.getElementById("seams").value = data.seams;
                document.getElementById("placas").value = data.placas;
            } else {
                document.getElementById("tipoUnidad").value = "";
                document.getElementById("noObra").value = "";
                document.getElementById("serie").value = "";
                document.getElementById("seams").value = "";
                document.getElementById("placas").value = "";
            }
        });
});

const claveInput = document.getElementById("claveConductor");

claveInput.addEventListener("blur", function () {
    const clave = this.value.trim();

    if (!clave) return;

    fetch(`/buscar-conductor/?clave=${clave}`)
        .then(response => response.json())
        .then(data => {
            if (data.existe) {
                document.getElementById("nombreConductor").value = data.nombre_completo;
            } else {
                document.getElementById("nombreConductor").value = "";
            }
        });
});

document.addEventListener("DOMContentLoaded", function () {
    fetch("/listar-tipo-cargo/")
        .then(response => response.json())
        .then(data => {
            const select = document.getElementById("tipoCargo");

            data.cargos.forEach(cargo => {
                const option = document.createElement("option");
                option.value = cargo.id_tipo_cargo;
                option.textContent = cargo.descripcion;
                select.appendChild(option);
            });
        });
    // ---- Cargar Tipo de Daño ----
    fetch("/listar-tipo-danio/")
        .then(response => response.json())
        .then(data => {
            const selectDanio = document.getElementById("tipoDanio");

            data.danios.forEach(danio => {
                const option = document.createElement("option");
                option.value = danio.id_tipo_dano;
                option.textContent = danio.descripcion;
                selectDanio.appendChild(option);
            });
        });
});

async function cargarProveedores() {
    const response = await fetch('/listar-proveedores/')
    const data = await response.json()

    const select = document.getElementById('proveedorSelect')
    select.innerHTML = '<option value="">-- Seleccionar proveedor --</option>'

    data.proveedores.forEach(p => {
        const option = document.createElement('option')
        option.value = p.id_proveedor
        option.textContent = p.nombre
        select.appendChild(option)
    })
}


