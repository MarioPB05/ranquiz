import { removePageLoader } from "/static/assets/js/ranquiz/utils.js";

/**
 * Función que cambia la vista de los elementos de la página
 * @param selected puede ser "list", "category" o "user"
 */
function toggleNavs(selected) {
    const allNavs = $("nav button");
    const selectedNav = $(`#${selected}_nav`);

    // Remover clases de nav seleccionado a todos los botones
    allNavs.removeClass("nav_selected");
    allNavs.removeClass("text-white");
    allNavs.removeClass("btn-primary");
    allNavs.hasClass("btn-outline-primary") ? allNavs.addClass("btn-outline-primary") : "";
    allNavs.hasClass("text-secondary-dark") ? allNavs.addClass("text-secondary-dark") : "";

    // Añadir clases al nav seleccionado
    selectedNav.addClass("nav_selected");
    selectedNav.addClass("text-white");
    selectedNav.addClass("btn-primary");
    selectedNav.removeClass("btn-outline-primary");
    selectedNav.removeClass("text-secondary-dark");
}

/**
 * Función que se ejecuta cuando el documento está listo
 */
function onDocumentReady() {
    $("nav button").on("click", (event) => {
        if ($(event.target).hasClass("nav_selected")) return;
        const selected = $(event.target).attr("id").split("_")[0];
        toggleNavs(selected);
    });

    removePageLoader();
}

$(document).ready(onDocumentReady);