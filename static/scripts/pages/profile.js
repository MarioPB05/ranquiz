import { removePageLoader, toastMessage } from "/static/assets/js/ranquiz/utils.js";

/**
 * Obtener cuando se ha hecho click en el botón de compartir cuenta
 */
function onShareAccount() {
    toastMessage('success', '¡URL copiada al portapapeles!');
}

/**
 * Obtener cuando se ha hecho click en el botón de compartir código
 */
function onShareCode() {
    toastMessage('success', '¡Código copiado al portapapeles!');
}

/**
 * Función que se ejecuta cuando la página ha cargado
 */
function pageLoaded() {
    const clipboardShareProfile = new ClipboardJS($('#share_account')[0]);  // skipcq: JS-0125
    const clipboardShareCode = new ClipboardJS($('#share_code')[0]);  // skipcq: JS-0125

    clipboardShareProfile.on('success', onShareAccount);
    clipboardShareCode.on('success', onShareCode);

    removePageLoader();
}

$(document).ready(pageLoaded);