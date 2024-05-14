/*global $, baseURL, moment*/

import {initializeFlatpickr, promiseAjax, toastMessage} from "/static/assets/js/ranquiz/utils.js";

const highlight_modal = $('#highlight_modal');
const highlight_submit = $('#highlight_submit');
const flatpickrInstance = initializeFlatpickr("#range_date_highlight", 'range', moment().format('YYYY-MM-DD')); // skipcq: JS-0125

/**
 * Cambia la visibilidad de una lista
 *
 * @param event
 */
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

/**
 * Calcula la cantidad de días entre las fechas seleccionadas
 *
 * @returns {number|*}
 */
function highlightDays() {
    const dates = $("#range_date_highlight").val().split(" hasta ");

    if (dates.length === 2) {
        const start_date = moment(dates[0], 'YYYY-MM-DD');
        const end_date = moment(dates[1], 'YYYY-MM-DD');

        return end_date.diff(start_date, 'days');
    }

    return 0;
}

/**
 * Cambia el estilo de los botones para el destacado de listas
 */
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

/**
 * Actualiza el precio del destacado de listas
 */
function updateHighlightPrice() {
    const dates = $("#range_date_highlight").val().split(" hasta ");

    if (dates.length === 2) {
        promiseAjax(`/api/shop/highlight/calculator?start_date=${dates[0]}&end_date=${dates[1]}`)
            .then(response => {
                $('#highlight_price').text(response.price);
                toogleHighLightButtons();
                highlight_submit.prop('disabled', false);
            })
            .catch(() => {
                toastMessage('error', 'Ha ocurrido un error al calcular el precio del destacado')
            });
    }
}

/**
 * Muestra el modal para destacar una lista
 *
 * @param event
 */
function showHighlightModal(event) {
    $("#highlight_list_name").text($(this).data('name'));
    highlight_submit.data('share_code', $(this).data('share_code'));
    highlight_submit.prop('disabled', true);
    flatpickrInstance.clear();
    $('#highlight_price').text('0');
    toogleHighLightButtons();

    const share_code = highlight_submit.data('share_code');

    promiseAjax(`/api/shop/highlight/${share_code}/check`, 'GET').then(response => {
        if (response.highlighted) {
            toastMessage('warning', 'Esta lista ya está destacada');
        }else {
            highlight_modal.modal('show');
        }
    });

    event.stopPropagation();
}

/**
 * Elimina una lista
 *
 * @param event
 */
function deleteList(event) {
    const share_code = $(this).data('share_code');

    $(this).prop('disabled', true);

    promiseAjax(`/api/list/${share_code}/delete`, 'GET').then((data) => {
        if (data.status === 'success') {
            window.location.reload();
        }

        $(this).prop('disabled', false);
    });

    event.stopPropagation();
}

/**
 * Recupera una lista eliminada
 *
 * @param event
 */
function recoverList(event) {
    const share_code = $(this).data('share_code');

    $(this).prop('disabled', true);

    promiseAjax(`/api/list/${share_code}/recover`, 'GET').then((data) => {
        if (data.status === 'success') {
            window.location.reload();
        }

        $(this).prop('disabled', false);
    });

    event.stopPropagation();

}

/**
 * Redirige a la lista seleccionada
 */
function redirectToList() {
    window.location.href = $(this).data('url');
}

/**
 * Obtiene la URL actual
 *
 * @returns {URL}
 */
function getCurrentURL() {
    return new URL(baseURL);
}

/**
 * Busca listas por el nombre de la lista sin quitar los filtros actuales
 *
 * @param event
 */
function searchList(event) {
    const url = getCurrentURL();
    const search = $('#search_input').val();

    if (event.key && event.key !== 'Enter') return; // Si se presionó una tecla y no fue Enter, no se hace nada

    if (!search) {
        url.searchParams.delete('search');

        window.location.href = url.toString();
        return;
    }

    url.searchParams.set('search', search);
    window.location.href = `${url.toString()}`;
}

/**
 * Filtra las listas por visibilidad y si se muestran las eliminadas
 */
function filterLists() {
    const url = getCurrentURL();
    const visibility = $('#visibility_filter').val();
    const show_deleted = $('#show_deleted_filter').is(':checked');

    if (visibility === 'all') {
        url.searchParams.delete('visibility');
    }else {
        url.searchParams.set('visibility', visibility);
    }

    if (!show_deleted) {
        url.searchParams.delete('show_deleted');
    }else {
        url.searchParams.set('show_deleted', show_deleted);
    }

    window.location.href = url.toString();
}

/**
 * Función que permite cambiar de página sin perder los filtros actuales
 *
 * @param event
 */
function changePage(event) {
    event.preventDefault();

    const page = $(this).data('page');
    const url = getCurrentURL();

    url.searchParams.set('page', page);

    window.location.href = url.toString();
}

/**
 * Carga los eventos de la página
 */
function loadEvents() {
    $('#list_container')
        .on('click', '.toggle_visibility_list', toggleVisibility)
        .on('click', '.highlight_list', showHighlightModal)
        .on('click', '.delete_list', deleteList)
        .on('click', '.restore_list', recoverList)
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

    highlight_submit.on("click", () => {
        const dates = $("#range_date_highlight").val().split(" hasta ");
        const share_code = highlight_submit.data('share_code');

        if (dates.length === 2) {
            highlight_submit.prop('disabled', true);

            promiseAjax(`/api/shop/highlight/${share_code}?start_date=${dates[0]}&end_date=${dates[1]}`, 'GET')
                .then((response) => {
                    if (response.status === 'success') {
                        toastMessage('success', response.message);
                        highlight_modal.modal('hide');
                    } else {
                        toastMessage('error', response.message);
                    }
                    highlight_submit.prop('disabled', false);
                })
                .catch(() => {
                    toastMessage('error', 'Ha ocurrido un error al destacar la lista');
                    highlight_submit.prop('disabled', false);
                });
        }
    });

    $('#search_input').on('keypress', searchList);
    $('#search_btn').on('click', searchList);
    $('#apply_filters_btn').on('click', filterLists);
    $('.page-link').on('click', changePage);

    const auto_redirect = $('#auto_redirect');

    if (auto_redirect.length > 0) {
        auto_redirect.trigger('click');
    }
}

$(document).ready(loadEvents);