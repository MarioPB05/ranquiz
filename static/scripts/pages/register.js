import {removePageLoader, initializeFlatpickr} from "/static/assets/js/ranquiz/utils.js";

/**
 * Esta función se encarga de cargar la lista de países en el select2
 */
function loadCountries() {
    $.ajax({
        type: 'GET',
        url: 'https://cdn.jsdelivr.net/npm/world_countries_lists@latest/data/es/countries.json',
        dataType: 'json',
        success: function (response) {
            $('#id_country').select2({
                data: response.map(e => ({
                    id: e.name,
                    text: e.name
                })),
                dropdownAutoWidth: true
            });
        },
        error: function () {
        },
        complete: function () {
        }
    });
}

$(document).ready(() => {

    const element = document.querySelector("#register_stepper");
    const stepper = new KTStepper(element);

    stepper.on("kt.stepper.next", function (stepper) {
        stepper.goNext();
    });

    stepper.on("kt.stepper.previous", function (stepper) {
        stepper.goPrevious();
    });

    initializeFlatpickr('#id_birthdate');
    loadCountries();

    removePageLoader();
});