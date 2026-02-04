let accidenteActual = null

function abrirModalProveedor(id, economico, conductor) {
    accidenteActual = id

    document.getElementById('provEconomico').value = economico
    document.getElementById('provConductor').value = conductor

    // 🔹 Limpia el select
    const select = document.getElementById('proveedorSelect')
    select.innerHTML = '<option value="">-- Seleccionar proveedor --</option>'

    // 🔹 CARGAR PROVEEDORES AQUÍ
    cargarProveedores()

    // 🔹 Mostrar modal
    document.getElementById('modalProveedor').classList.remove('hidden')
}

function cerrarModalProveedor() {
    document.getElementById('modalProveedor').classList.add('hidden')
}

async function guardarProveedor() {
    const proveedor = document.getElementById('proveedorSelect').value

    if (!proveedor) {
        Swal.fire('Atención', 'Selecciona un proveedor', 'warning')
        return
    }

    const response = await fetch(`/accidente/asignar-proveedor/${accidenteActual}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken(),
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ proveedor })
    })

    const data = await response.json()

    if (data.success) {
        Swal.fire({
            icon: 'success',
            title: 'Proveedor asignado',
            timer: 2000,
            showConfirmButton: false
        }).then(() => location.reload())
    } else {
        Swal.fire('Error', data.error, 'error')
    }
}
