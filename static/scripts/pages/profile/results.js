/*global $, baseURL*/

/**
 * Obtiene la URL actual
 *
 * @returns {URL}
 */
function getCurrentURL() {
    return new URL(baseURL);
}

/**
 * Redirige a la lista seleccionada
 */
function redirectToResult() {
    window.location.href = $(this).data('url');
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

    url.searchParams.delete('page')
    url.searchParams.set('search', search);
    window.location.href = `${url.toString()}`;
}

/**
 * Función que se ejecuta cuando el documento está listo
 */
function onDocumentReady() {
    $('.list_result').on('click', redirectToResult);
    $('#search_input').on('keypress', searchList);
    $('#search_btn').on('click', searchList);
}

$(document).ready(onDocumentReady);