// Ocultar loader al cargar la página
window.addEventListener('load', () => {
  const loader = document.getElementById('page-loader')
  if (!loader) return

  loader.classList.add('opacity-0')
  setTimeout(() => (loader.style.display = 'none'), 300)
})

// Mostrar loader al cambiar de página
document.querySelectorAll('a[href]').forEach((link) => {
  link.addEventListener('click', () => {
    const loader = document.getElementById('page-loader')
    if (loader) loader.style.display = 'flex'
  })
})
function mostrarLoader() {
  const loader = document.getElementById('page-loader');
  if (loader) {
    loader.style.display = 'flex';
    loader.classList.remove('opacity-0');
  }
}

function ocultarLoader() {
  const loader = document.getElementById('page-loader');
  if (loader) {
    loader.classList.add('opacity-0');
    setTimeout(() => (loader.style.display = 'none'), 300);
  }
}