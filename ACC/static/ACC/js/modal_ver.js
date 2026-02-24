// =========================
// VARIABLES GLOBALES
// =========================

let imagenesAccidente = []
let indiceImagen = 0


// =========================
// VER ACCIDENTE
// =========================

function verAccidente(id) {

    fetch(`/accidente/vista/${id}/`)
        .then(response => response.json())
        .then(data => {

            // =========================
            // ABRIR MODAL
            // =========================

            const modal = document.getElementById("modalVerAccidente")

            modal.classList.remove("hidden")
            modal.classList.add("flex")


            // =========================
            // DATOS GENERALES
            // =========================

            document.getElementById("ver_fecha").innerText = data.fecha

            document.getElementById("ver_unidad").innerText = data.autobus.economico

            document.getElementById("ver_placas").innerText = data.autobus.placas

            document.getElementById("ver_seams").innerText = data.autobus.seams || "-"

            document.getElementById("ver_no_obra").innerText = data.autobus.no_obra || "-"


            // =========================
            // CONDUCTOR
            // =========================

            document.getElementById("ver_conductor").innerText = data.conductor.nombre


            // =========================
            // PROVEEDOR
            // =========================

            document.getElementById("ver_proveedor").innerText = data.proveedor || "Sin asignar"


            // =========================
            // DESCRIPCIÓN
            // =========================

            document.getElementById("ver_descripcion").innerText = data.descripcion


            // =========================
            // BADGE TIPO AUTOBUS
            // =========================

            let tipo = data.autobus.tipo

            let tipoBadge = document.getElementById("ver_tipo_badge")

            tipoBadge.innerText = tipo

            tipoBadge.className = "text-white px-2 py-1 rounded-full text-xs"

            if (tipo === "GL")
                tipoBadge.classList.add("bg-purple-600")

            else if (tipo === "PL")
                tipoBadge.classList.add("bg-blue-900")

            else
                tipoBadge.classList.add("bg-gray-500")


            // =========================
            // BADGE ESTADO
            // =========================

            let estadoBadge = document.getElementById("ver_estado_badge")

            let estado = data.estado

            if (estado === "EN_PROCESO") {

                estadoBadge.innerText = "En proceso"

                estadoBadge.className =
                    "bg-yellow-100 text-yellow-700 px-3 py-1 rounded-full text-xs"

            }
            else if (estado === "EN_REPARACION") {

                estadoBadge.innerText = "En reparación"

                estadoBadge.className =
                    "bg-blue-100 text-blue-700 px-3 py-1 rounded-full text-xs"

            }
            else if (estado === "FINALIZADO") {

                estadoBadge.innerText = "Finalizado"

                estadoBadge.className =
                    "bg-green-100 text-green-700 px-3 py-1 rounded-full text-xs"

            }


            // =========================
            // IMAGENES DESDE DRIVE
            // =========================

            imagenesAccidente = data.imagenes || []

            indiceImagen = 0

            mostrarImagenActual()

        })
        .catch(error => {

            console.error("Error:", error)

            alert("Error al cargar el accidente")

        })

}



// =========================
// MOSTRAR IMAGEN ACTUAL
// =========================

function mostrarImagenActual() {

    const img = document.getElementById("ver_imagen")

    const sin = document.getElementById("sin_imagen")


    if (imagenesAccidente.length === 0) {

        img.classList.add("hidden")

        sin.classList.remove("hidden")

        return

    }

    img.src = imagenesAccidente[indiceImagen].url

    img.classList.remove("hidden")

    sin.classList.add("hidden")

}



// =========================
// SIGUIENTE IMAGEN
// =========================

function siguienteImagen() {

    if (imagenesAccidente.length === 0) return

    indiceImagen++

    if (indiceImagen >= imagenesAccidente.length)
        indiceImagen = 0

    mostrarImagenActual()

}



// =========================
// IMAGEN ANTERIOR
// =========================

function anteriorImagen() {

    if (imagenesAccidente.length === 0) return

    indiceImagen--

    if (indiceImagen < 0)
        indiceImagen = imagenesAccidente.length - 1

    mostrarImagenActual()

}



// =========================
// CERRAR MODAL
// =========================

function cerrarModalVer() {

    const modal = document.getElementById("modalVerAccidente")

    modal.classList.remove("flex")

    modal.classList.add("hidden")

}