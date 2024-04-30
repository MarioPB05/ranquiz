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

}

$(document).ready(loadEvents);