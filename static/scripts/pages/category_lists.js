import { removePageLoader, promiseAjax } from "/static/assets/js/ranquiz/utils.js";
const followButton  = $("#follow_category");

/**
 * Función que cambia el botón de seguir a siguiendo y viceversa
 */
function toggleFollowButton() {

    if (followButton.hasClass("btn-primary")) {
        followButton.removeClass("btn-primary");
        followButton.addClass("btn-outline-primary");
        followButton.addClass("btn-outline");
        followButton.addClass("btn-active-primary");
        followButton.text("Seguir")
        followButton.blur();
    }else {
        followButton.addClass("btn-primary");
        followButton.removeClass("btn-outline-primary");
        followButton.removeClass("btn-outline");
        followButton.removeClass("btn-active-primary");
        followButton.text("Siguiendo")
        followButton.blur();
    }
}


/**
 * Función que se ejecuta cuando el documento está listo
 */
function onDocumentReady() {
    // Evento de cambio de botón de seguir
    followButton.on("click", toggleFollowButton);

    sendFollowCategory().then((response) => {
        if (response.following) {
            followButton.addClass("btn-primary");
            followButton.text("Siguiendo");
        } else {
            followButton.addClass("btn-outline-primary");
            followButton.text("Seguir");
        }
    });

    removePageLoader();
}

$(document).ready(onDocumentReady);
