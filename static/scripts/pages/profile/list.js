import {initializeFlatpickr, promiseAjax, toastMessage} from "/static/assets/js/ranquiz/utils.js";

const highlight_modal = $('#highlight_modal');
const flatpickrInstance = initializeFlatpickr("#range_date_highlight", 'range', moment().format('YYYY-MM-DD')); // skipcq: JS-0125

function toggleVisibility(event) {
    const share_code = $(this).data('share_code');
    const parent = $(this).closest('.list_item');

    $(this).prop('disabled', true);

    promiseAjax(`/api/list/${share_code}/visibility`, 'GET').then((data) => {
        if (data.status === 'success') {
            const icon = $(this).find('i');
            const badge = parent.find('.list_visibility');

            if (icon.hasClass('bi-eye-slash-fill')) {
                badge.text('Privado');
                badge.removeClass('badge-success').addClass('badge-secondary');
                icon.removeClass('bi-eye-slash-fill').addClass('bi-eye-fill');

                toastMessage('success', 'Lista marcada como privada');
            } else {
                badge.text('Público');
                badge.removeClass('badge-secondary').addClass('badge-success');
                icon.removeClass('bi-eye-fill').addClass('bi-eye-slash-fill');

                toastMessage('success', 'Lista marcada como pública');
            }

            $(this).blur();
            $(this).prop('disabled', false);
        }
    });

    event.stopPropagation();
}

function highlightDays() {
    const dates = $("#range_date_highlight").val().split(" hasta ");

    if (dates.length === 2) {
        const start_date = moment(dates[0], 'YYYY-MM-DD');
        const end_date = moment(dates[1], 'YYYY-MM-DD');

        return end_date.diff(start_date, 'days');
    }

    return 0;
}

function toogleHighLightButtons() {
    const days = highlightDays();
    const buttons = $("#highlight_days_buttons button");
    const selected_button = $(`#highlight_${days}_day`);

    buttons.removeClass("btn-primary");
    buttons.addClass("btn-outline-primary");
    buttons.addClass("btn-outline");

    if (selected_button.length > 0) {
        selected_button.addClass("btn-primary");
        selected_button.removeClass("btn-outline-primary");
        selected_button.removeClass("btn-outline");
    }
}

function updateHighlightPrice() {
    const dates = $("#range_date_highlight").val().split(" hasta ");

    if (dates.length === 2) {
        promiseAjax(`/api/shop/highlight/calculator?start_date=${dates[0]}&end_date=${dates[1]}`)
            .then(response => {
                $('#highlight_price').text(response.price);
                toogleHighLightButtons();
            })
            .catch(() => {
                toastMessage('error', 'Ha ocurrido un error al calcular el precio del destacado')
            });
    }
}

function highlightList(event) {
    highlight_modal.modal('show');

    event.stopPropagation();
}

function redirectToList() {
    window.location.href = $(this).data('url');
}

function loadEvents() {
    $('#list_container')
        .on('click', '.toggle_visibility_list', toggleVisibility)
        .on('click', '.highlight_list', highlightList)
        .on('click', '.list_item', redirectToList);

    $("#range_date_highlight").on("change", updateHighlightPrice);

    $("#highlight_days_buttons button").on("click", (event) => {
        const days = parseInt($(event.target).data("days"), 10);
        const startDate = new Date();
        const endDate =  new Date();
        endDate.setDate(startDate.getDate() + days);

        flatpickrInstance.setDate([startDate, endDate]);
        updateHighlightPrice();
    });
}

$(document).ready(loadEvents);