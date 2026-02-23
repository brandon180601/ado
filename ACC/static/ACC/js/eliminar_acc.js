function confirmarEliminar(accidenteId) {
    Swal.fire({
        title: '¿Eliminar accidente?',
        text: 'Esta acción no se puede deshacer',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#dc2626',
        cancelButtonColor: '#6b7280',
        confirmButtonText: 'Sí, eliminar',
        cancelButtonText: 'Cancelar'
    }).then((result) => {
        if (result.isConfirmed) {
            eliminarAccidente(accidenteId)
        }
    })
}

function eliminarAccidente(accidenteId) {
    if (typeof mostrarLoader === "function") {
        mostrarLoader()
    }
    fetch(`/accidente/eliminar/${accidenteId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken()
        }
    })
        .then((res) => res.json())
        .then((data) => {
            if (typeof ocultarLoader === "function") {
                ocultarLoader()
            }
            if (data.success) {
                Swal.fire({
                    icon: 'success',
                    title: 'Eliminado',
                    text: 'El accidente fue eliminado correctamente',
                    confirmButtonColor: '#6A2973',
                    showConfirmButton: false,
                    timer: 2500,
                    timerProgressBar: true
                }).then(() => {
                    location.reload()
                })
            } else {
                Swal.fire('Error', data.error, 'error')
            }
        })
}