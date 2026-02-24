const inputSearch = document.querySelector('input[name="q"]');

inputSearch.addEventListener('keydown', function (e) {
    if (e.key === "Enter") {
        e.preventDefault(); // evita que se haga un submit doble
        this.form.submit();
    }
});

inputSearch.addEventListener('blur', function () {
    if (this.value.trim() !== "") {
        this.form.submit();
    }
});
