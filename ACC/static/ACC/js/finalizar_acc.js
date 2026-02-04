function validarCierreAccidente() {
    const codigo = document.getElementById("finalCodigo").value.trim();
    const costo = document.getElementById("finalCosto").value;
    const comentarios = document.getElementById("finalComentarios").value.trim();

    if (!codigo || !costo || !comentarios) {
        Swal.fire("Campos incompletos", "Todos los campos del cierre son obligatorios", "warning");
        return false;
    }

    if (parseFloat(costo) <= 0) {
        Swal.fire("Costo inválido", "El costo debe ser mayor a 0", "warning");
        return false;
    }

    if (archivosFinales.length === 0) {
        Swal.fire(
            "Evidencia requerida",
            "Debes subir al menos una imagen",
            "warning"
        );
        return false;
    }

    return true;
}

function confirmarFinalizarAccidente() {
    if (!validarCierreAccidente()) return;

    Swal.fire({
        title: "Finalizar accidente",
        text: "Una vez finalizado no podrás modificar la información",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#7e22ce",
        cancelButtonText: "Cancelar",
        confirmButtonText: "Sí, finalizar"
    }).then(result => {
        if (result.isConfirmed) {
            finalizarAccidente();
        }
    });
}

async function finalizarAccidente() {
    const formData = new FormData();

    // ==== DATOS BÁSICOS
    formData.append("economico", document.getElementById("editEconomico").value);
    formData.append("clave_conductor", document.getElementById("editClaveConductor").value);
    formData.append("tipo_dano", document.getElementById("editTipoDanio").value);
    formData.append("tipo_cargo", document.getElementById("editTipoCargo").value);
    formData.append("proveedor", document.getElementById("editProveedor").value);
    formData.append("descripcion", document.getElementById("editDescripcion").value);

    // ==== CIERRE
    formData.append(
        "codigo_acc",
        "ML-" + document.getElementById("finalCodigo").value.trim()
    );
    formData.append("costo", document.getElementById("finalCosto").value);
    formData.append("comentarios", document.getElementById("finalComentarios").value);

    // ==== IMÁGENES
    archivosFinales.forEach(file => {
        formData.append("imagenes", file);
    });

    try {
        // 🔄 MOSTRAR LOADER
        mostrarLoader();

        const response = await fetch(
            `/accidente/finalizar/${accidenteEditId}/`,
            {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken")
                },
                body: formData
            }
        );

        const data = await response.json();

        if (!response.ok || !data.success) {
            throw new Error(data.error || "Error al finalizar accidente");
        }

        Swal.fire({
            icon: "success",
            title: "Accidente finalizado",
            timer: 2000,
            showConfirmButton: false
        }).then(() => location.reload());

    } catch (error) {
        console.error(error);
        Swal.fire("Error", error.message, "error");
    } finally {
        // 🔄 OCULTAR LOADER SIEMPRE
        ocultarLoader();
    }
}
