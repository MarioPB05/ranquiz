import {removePageLoader, initializeFlatpickr} from "/static/assets/js/ranquiz/utils.js";

/**
 * Esta función se encarga de cargar la lista de países en el select2
 */
function loadCountries() {
    $.ajax({
        type: 'GET',
        url: 'https://cdn.jsdelivr.net/npm/world_countries_lists@latest/data/es/countries.json',
        dataType: 'json',
        success: (response) => {
            $('#id_country').select2({
                data: response.map(e => ({
                    id: e.name,
                    text: e.name
                })),
                dropdownAutoWidth: true
            });
        }
    });
}

$(document).ready(() => {

    const element = document.querySelector("#register_stepper");
    const stepper = new KTStepper(element);  // skipcq: JS-0125

    stepper.on("kt.stepper.next", (s) => s.goNext());

    stepper.on("kt.stepper.previous", (s) => s.goPrevious());

    initializeFlatpickr('#id_birthdate');
    loadCountries();

    removePageLoader();
});