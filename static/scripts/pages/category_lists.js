import { removePageLoader, promiseAjax } from "/static/assets/js/ranquiz/utils.js";
const followButton  = $("#follow_category");
const bellButton = $("#follow_category_bell");
const content = $("#list_container");

/**
 * Función que cambia el botón de seguir a siguiendo y viceversa
 */
function toggleFollowButton() {

    if (followButton.hasClass("btn-primary")) {
        followButton.removeClass("btn-primary").addClass("btn-outline-primary");
        followButton.addClass("btn-outline");
        followButton.addClass("btn-active-primary");
        followButton.text("Seguir");
    }else {
        followButton.addClass("btn-primary").removeClass("btn-outline-primary");
        followButton.removeClass("btn-outline");
        followButton.removeClass("btn-active-primary");
        followButton.text("Siguiendo");
    }

    followButton.blur();
}

/**
 * Función que cambia el botón de notificaciones a activado y viceversa
 */
function toggleBellButton() {
    if (bellButton.hasClass("btn-primary")) {
        bellButton.removeClass("btn-primary").addClass("btn-outline-primary");
        bellButton.addClass("btn-outline");
        bellButton.addClass("btn-active-primary");
        bellButton.find("i").removeClass("bi-bell-fill").addClass("bi-bell-slash-fill");
        bellButton.attr("title", "Activar notificaciones");
    }else {
        bellButton.addClass("btn-primary").removeClass("btn-outline-primary");
        bellButton.removeClass("btn-outline");
        bellButton.removeClass("btn-active-primary");
        bellButton.find("i").removeClass("bi-bell-slash-fill").addClass("bi-bell-fill");
        bellButton.attr("title", "Desactivar notificaciones");
    }
    
    bellButton.tooltip('dispose').tooltip();
    bellButton.blur();
}


/**
 * Función que se ejecuta cuando el documento está listo
 */
function onDocumentReady() {
    // Evento de cambio de botón de seguir
    followButton.on("click", () => {
        toggleFollowButton();

        if (followButton.hasClass("btn-primary")) {
            bellButton.removeClass("d-none");
        }else {
            bellButton.addClass("d-none");
        }
    });

    // Evento de cambio de botón de notificaciones
    bellButton.on("click", toggleBellButton);

    // Evento de click en la lista
    content.on("click", ".list", (event) => {
       if (event.target.tagName === "A") return;

        const url = $(event.currentTarget).attr("href");
        if (url) window.location.href = url;
    });

    removePageLoader();
}

$(document).ready(onDocumentReady);
