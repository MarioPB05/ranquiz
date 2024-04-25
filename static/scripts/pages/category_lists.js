import { removePageLoader, promiseAjax } from "/static/assets/js/ranquiz/utils.js";

/**
 * Función que se ejecuta cuando el documento está listo
 */
function onDocumentReady() {
    removePageLoader();
}

$(document).ready(onDocumentReady);
