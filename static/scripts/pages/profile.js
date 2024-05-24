import {removePageLoader, toastMessage, toggleUserFollow} from "/static/assets/js/ranquiz/utils.js";

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
 * Función para seguir o dejar de seguir al usuario
 */
function followUser(event) {
    $(this).prop("disabled", true);

    toggleUserFollow(event).then((isFollowed) => {
        if (isFollowed) {
            $(this).removeClass("btn-primary").addClass("btn-outline btn-outline-primary text-hover-white");
            $(this).text("Seguir");

            toastMessage("success", "Dejaste de seguir al usuario");
        }else {
            $(this).removeClass("btn-outline btn-outline-primary text-hover-white").addClass("btn-primary");
            $(this).text("Siguiendo");

            toastMessage("success", "Ahora sigues al usuario");
        }

        $(this).prop("disabled", false);
    }).catch(() => {
        toastMessage("error", "Error al seguir usuario");
        $(this).prop("disabled", false);
    });
}

/**
 * Función que se ejecuta cuando la página ha cargado
 */
function pageLoaded() {
    const clipboardShareProfile = new ClipboardJS($('#share_account')[0]);  // skipcq: JS-0125
    const clipboardShareCode = new ClipboardJS($('#share_code')[0]);  // skipcq: JS-0125

    clipboardShareProfile.on('success', onShareAccount);
    clipboardShareCode.on('success', onShareCode);

    $('.btn_toggle_follow').on('click', followUser);

    removePageLoader();
}

$(document).ready(pageLoaded);