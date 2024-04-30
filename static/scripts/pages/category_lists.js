import { removePageLoader, promiseAjax, toastMessage } from "/static/assets/js/ranquiz/utils.js";
const followButton  = $("#follow_category");
const bellButton = $("#follow_category_bell");
const content = $("#list_container");

/**
 * Función que cambia el botón de seguir a siguiendo y viceversa
 * @param {boolean|null} state - Estado al que se quiere cambiar el botón
 */
function toggleFollowButton(state = null) {

    if (state === false || (followButton.hasClass("btn-primary") && state === null)) {
        followButton.removeClass("btn-primary").addClass("btn-outline-primary");
        followButton.addClass("btn-outline");
        followButton.addClass("btn-active-primary");
        followButton.text("Seguir");
    }else if (state === true ||(followButton.hasClass("btn-outline-primary") && state === null)) {
        followButton.addClass("btn-primary").removeClass("btn-outline-primary");
        followButton.removeClass("btn-outline");
        followButton.removeClass("btn-active-primary");
        followButton.text("Siguiendo");
    }

    followButton.blur();
}

/**
 * Función que cambia el botón de notificaciones a activado y viceversa
 * @param {boolean|null} state - Estado al que se quiere cambiar el botón
 */
function toggleBellButton(state = null) {

    if (state === false || (bellButton.hasClass("btn-primary") && state === null)) {
        bellButton.removeClass("btn-primary").addClass("btn-outline-primary");
        bellButton.addClass("btn-outline");
        bellButton.addClass("btn-active-primary");
        bellButton.find("i").removeClass("bi-bell-fill").addClass("bi-bell-slash-fill");
        bellButton.attr("title", "Activar notificaciones");
    }else if (state === true || (bellButton.hasClass("btn-outline-primary") && state === null)) {
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
 * Función que cambia los dos botones a la vez
 * @param follow
 * @param notification
 */
function toggleTwoButtons(follow, notification) {
    console.log(follow, notification)
    toggleFollowButton(follow);
    toggleBellButton(notification);

    if (follow) {
        bellButton.removeClass("d-none");
    }else {
        bellButton.addClass("d-none");
    }
}

/**
 * Función que sigue o deja de seguir una categoría
 * @param category_share_code
 * @param follow
 * @param notification
 */
function followCategory(category_share_code, follow, notification) {
    const url = "/api/category/follow?" +
          "category_share_code=" + category_share_code + "&" +
          "follow=" + follow + "&" +
          "notification=" + notification;

    followButton.prop("disabled", true);
    bellButton.prop("disabled", true);

    promiseAjax(url, "GET").then((response) => {
        if (response.status === "success") {
            toggleTwoButtons(response.followed, response.notification);
        }else {
            toastMessage("error", "Ha ocurrido un error al intentar seguir la categoría");
        }

        followButton.prop("disabled", false);
        bellButton.prop("disabled", false);

    }).catch(() => {
        toastMessage("error", "Ha ocurrido un error al intentar seguir la categoría");
        followButton.prop("disabled", false);
        bellButton.prop("disabled", false);
    });
}


/**
 * Función que se ejecuta cuando el documento está listo
 */
function onDocumentReady() {
    // Evento de cambio de botón de seguir
    followButton.on("click", () => {
        const follow = !followButton.hasClass("btn-primary");
        const notification = !bellButton.hasClass("btn-primary");

        followCategory(share_code, follow, notification);
    });

    // Evento de cambio de botón de notificaciones
    bellButton.on("click", () => {
        const follow = followButton.hasClass("btn-primary");
        const notification = !bellButton.hasClass("btn-primary");

        followCategory(share_code, follow, notification);
    });

    // Evento de click en la lista
    content.on("click", ".list", (event) => {
       if (event.target.tagName === "A") return;

        const url = $(event.currentTarget).attr("href");
        if (url) window.location.href = url;
    });

    removePageLoader();
}

$(document).ready(onDocumentReady);
