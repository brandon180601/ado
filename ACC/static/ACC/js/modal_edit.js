let accidenteEditId = null
let estadoInicialEditar = null
let bloqueandoEventosEditar = false


document.addEventListener('click', function (e) {
  const btn = e.target.closest('.btn-editar')
  if (!btn) return

  const id = btn.dataset.id

  abrirModalEditar(id)
})


// ABRIR MODAL
async function abrirModalEditar(id) {
  accidenteEditId = id
  bloqueandoEventosEditar = true

  try {
    const res = await fetch(`/accidente/detalle/${id}/`)
    if (!res.ok) throw 'Error al cargar accidente'

    const data = await res.json()

    // ===== UNIDAD =====
    document.getElementById('editEconomico').value = data.autobus.economico
    document.getElementById('editTipoUnidad').value = data.autobus.tipo
    document.getElementById('editSeams').value = data.autobus.seams
    document.getElementById('editNoObra').value = data.autobus.no_obra
    document.getElementById('editSerie').value = data.autobus.serie
    document.getElementById('editPlacas').value = data.autobus.placas

    // ===== CONDUCTOR =====
    document.getElementById('editClaveConductor').value = data.conductor.clave
    document.getElementById('editNombreConductor').value = data.conductor.nombre

    // ===== DESCRIPCIÓN =====
    document.getElementById('editDescripcion').value = data.descripcion

    // ===== SELECTS =====
    await cargarSelect('/listar-tipo-danio/', 'editTipoDanio', data.tipo_dano_id)
    await cargarSelect('/listar-tipo-cargo/', 'editTipoCargo', data.tipo_cargo_id)
    await cargarSelect('/listar-proveedores/', 'editProveedor', data.proveedor_id)

    // Guardar estado inicial DESPUÉS de cargar todo
    estadoInicialEditar = obtenerEstadoEditar()
    deshabilitarGuardarEditar()

    bloqueandoEventosEditar = false

    document.getElementById('modalEditarAccidente').classList.remove('hidden')

  } catch (error) {
    bloqueandoEventosEditar = false
    Swal.fire('Error', 'No se pudo cargar el accidente', 'error')
  }
}

// CERRAR MODAL
function cerrarModalEditar() {
  document.getElementById('modalEditarAccidente').classList.add('hidden')
  accidenteEditId = null
  estadoInicialEditar = null
}

async function cargarSelect(url, selectId, seleccionado) {
  const res = await fetch(url)
  const data = await res.json()

  const select = document.getElementById(selectId)
  select.innerHTML = '<option value="">-- Seleccionar --</option>'

  const lista = data.danios || data.cargos || data.proveedores

  lista.forEach(item => {
    // detectar id dinámicamente
    const id =
      item.id ||
      item.id_tipo_dano ||
      item.id_tipo_cargo ||
      item.id_proveedor

    const texto = item.descripcion || item.nombre

    const option = document.createElement('option')
    option.value = String(id)
    option.textContent = texto

    select.appendChild(option)
  })

  // seleccionar después de cargar todo
  if (seleccionado !== null && seleccionado !== undefined) {
    select.value = String(seleccionado)
  }
}


document.addEventListener("DOMContentLoaded", () => {

  const economicoEdit = document.getElementById("editEconomico")
  const claveConductorEdit = document.getElementById("editClaveConductor")

  // ===============================
  // BUSCAR AUTOBÚS (EDITAR)
  // ===============================
  economicoEdit.addEventListener("blur", function () {
    const economico = this.value.trim()
    if (!economico) return

    fetch(`/buscar-autobus/?economico=${economico}`)
      .then(res => res.json())
      .then(data => {
        if (data.existe) {
          document.getElementById("editTipoUnidad").value = data.tipo_unidad
          document.getElementById("editNoObra").value = data.no_obra
          document.getElementById("editSerie").value = data.serie
          document.getElementById("editSeams").value = data.seams
          document.getElementById("editPlacas").value = data.placas
        } else {
          limpiarAutobusEditar()
        }
        verificarCambiosEditar()
      })
  })

  function limpiarAutobusEditar() {
    document.getElementById("editTipoUnidad").value = ""
    document.getElementById("editNoObra").value = ""
    document.getElementById("editSerie").value = ""
    document.getElementById("editSeams").value = ""
    document.getElementById("editPlacas").value = ""
  }

  // ===============================
  // BUSCAR CONDUCTOR (EDITAR)
  // ===============================
  claveConductorEdit.addEventListener("blur", function () {
    const clave = this.value.trim()
    if (!clave) return

    fetch(`/buscar-conductor/?clave=${clave}`)
      .then(res => res.json())
      .then(data => {
        document.getElementById("editNombreConductor").value =
          data.existe ? data.nombre_completo : ""
        verificarCambiosEditar()
      })
  })
  document.querySelectorAll(
    "#modalEditarAccidente input, #modalEditarAccidente textarea, #modalEditarAccidente select"
  ).forEach(el => {
    el.addEventListener("input", verificarCambiosEditar)
    el.addEventListener("change", verificarCambiosEditar)
  })

})

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
      cookie = cookie.trim();
      if (cookie.startsWith(name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function actualizarAccidente() {
  fetch(`/accidente/actualizar/${accidenteEditId}/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken")
    },
    body: JSON.stringify({
      economico: document.getElementById("editEconomico").value.trim(),
      clave_conductor: document.getElementById("editClaveConductor").value.trim(),
      tipo_dano: document.getElementById("editTipoDanio").value,
      tipo_cargo: document.getElementById("editTipoCargo").value,
      proveedor: document.getElementById("editProveedor").value,
      descripcion: document.getElementById("editDescripcion").value
    })
  })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        Swal.fire({
          icon: 'success',
          title: 'Accidente actualizado',
          timer: 2000,
          showConfirmButton: false
        }).then(() => location.reload())
      } else {
        Swal.fire("Error", data.error, "error")
      }
    })
}

function obtenerEstadoEditar() {
  return {
    economico: document.getElementById("editEconomico").value.trim(),
    clave_conductor: document.getElementById("editClaveConductor").value.trim(),
    tipo_dano: document.getElementById("editTipoDanio").value,
    tipo_cargo: document.getElementById("editTipoCargo").value,
    proveedor: document.getElementById("editProveedor").value,
    descripcion: document.getElementById("editDescripcion").value.trim(),
  }
}

function deshabilitarGuardarEditar() {
  const btn = document.getElementById("btnGuardarEditar")
  btn.disabled = true
  btn.classList.add("opacity-50", "cursor-not-allowed")
}

function habilitarGuardarEditar() {
  const btn = document.getElementById("btnGuardarEditar")
  btn.disabled = false
  btn.classList.remove("opacity-50", "cursor-not-allowed")
}

function verificarCambiosEditar() {
  if (bloqueandoEventosEditar || !estadoInicialEditar) return

  const actual = obtenerEstadoEditar()
  const huboCambios =
    JSON.stringify(actual) !== JSON.stringify(estadoInicialEditar)

  if (huboCambios) {
    habilitarGuardarEditar()
  } else {
    deshabilitarGuardarEditar()
  }
}

