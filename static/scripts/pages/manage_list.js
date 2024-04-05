import { removePageLoader, initializeFlatpickr, promiseAjax } from "/static/assets/js/ranquiz/utils.js";

$(document).ready(function() {

    initializeFlatpickr("#range_date_highlight", 'range', moment().format('DD-MM-YYYY'));

    $('#name').maxlength({
        warningClass: "badge badge-primary",
        limitReachedClass: "badge badge-danger"
    });

    $('#type').select2({
        placeholder: 'Selecciona una opción',
        minimumResultsForSearch: -1,
        ajax: {
          url: '/api/list/types', // La URL de tu endpoint de búsqueda
          dataType: 'json',
          delay: 0,
          processResults: function (data) {
            return {
              results: data.types
            };
          }
        }
    });

    removePageLoader();
});

$("#range_date_highlight").on("change", function() {
    let dates = $(this).val().split(" hasta ");

    if (dates.length === 2) {
        promiseAjax(`/api/shop/highlight/calculator?start_date=${dates[0]}&end_date=${dates[1]}`)
        .then(response => {
            $('#highlight_price').text(response.price);
        })
        .catch(error => {
            console.error(error);
        });
    }
});
