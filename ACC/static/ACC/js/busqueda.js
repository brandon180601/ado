
const inputSearch = document.querySelector('input[name="q"]');
let timeout = null;

inputSearch.addEventListener('input', function () {
    clearTimeout(timeout);
    timeout = setTimeout(() => {
        this.form.submit();
    }, 500); // espera medio segundo después de dejar de escribir
});