/*global $, share_code*/

import {toggleCategoryFollow, toggleListLike, toggleUserFollow} from "/static/assets/js/ranquiz/utils.js";

let page = 2;
let isLoadingData = false;

const kt_content_container = $('#kt_content_container')

/**
 * Verifica si el scroll está cerca del final del contenedor
 *
 * @returns {boolean}
 */
function isScrollNearEnd(element) {
    return element.scrollLeft() + element.outerWidth() >= element[0].scrollWidth - 500;
}

/**
 * Carga más datos en la sección correspondiente
 */
function loadMoreData(element) {
    if (isLoadingData) return;
    isLoadingData = true;

    let url = element.data('url');
    url += url.includes('?') ? `&page=${page}` : `?page=${page}`;

    console.log(url)

    $.ajax({
        url: url,
        type: 'GET',
        /**
         * Función que se ejecuta si la petición AJAX fue exitosa
         *
         * @param data
         * @param {Array} data.results
         */
        success(data) {
            isLoadingData = false;

            if (data.results.length === 0) return;

            page++;
            const newData = data.results;

            newData.forEach((item) => {
                const listItem = $(`<div class="${element.data('custom-class')}"></div>`).html(item);
                element.append(listItem);
            });
        }
    });
}

/**
 * Realiza un scroll infinito en la sección de listas del perfil
 *
 * @param scroll
 * @param event
 */
function infiniteScroll(scroll = false, event) {
    const element = $(event.target).closest('.position-relative').find('.scroll');

    if (isScrollNearEnd(element)) loadMoreData(element);

    if (scroll) element.animate({scrollLeft: element.scrollLeft() + 500}, 500);
}

/**
 * Carga los eventos de la página
 */
function loadEvents() {

    // Evento para dar like a una lista
    kt_content_container.on("click", ".list_like", toggleListLike);

    // Evento para seguir a un usuario
    kt_content_container.on("click", ".user_follow", (event) => {
        $(this).prop("disabled", true);
        const icon = $(event.currentTarget).find('i');

        icon.toggleClass("bi-person-plus-fill").toggleClass("bi-person-check-fill text-primary");

        toggleUserFollow(event).then(() => {
            $(this).prop("disabled", false);
        }).catch(() => {
            icon.toggleClass("bi-person-plus-fill").toggleClass("bi-person-check-fill text-primary");
            $(this).prop("disabled", false);
        });
    });

    kt_content_container.on("click", ".category_follow", (event) => {
        $(this).prop("disabled", true);
        const button = $(event.currentTarget);

        if (button.hasClass("btn-primary")) {
            button.removeClass("btn-primary").addClass("btn-outline-primary");
            button.addClass("btn-active-primary");
            button.text("Seguir");
            button.blur();
        } else {
            button.removeClass("btn-outline-primary").addClass("btn-primary");
            button.text("Siguiendo");
        }

        toggleCategoryFollow(event).then(() => {
            $(this).prop("disabled", false);
        }).catch(() => {
            const buttonFollow   = $(event.currentTarget);
            buttonFollow.toggleClass("btn-primary").toggleClass("btn-outline-primary");
            buttonFollow.toggleClass("btn-active-primary");
            buttonFollow.text("Seguir");
            buttonFollow.blur();
            $(this).prop("disabled", false);
        });
    });

    // Evento de clic en un elemento
    kt_content_container.on("click", ".list, .category_element, .user", (event) => {
        if (event.target.tagName === "A") return;


        const url = $(event.currentTarget).attr("href");
        if (url) window.location.href = url;
    });


    $('.scroll').scroll((event) => infiniteScroll(false, event));
    $('.scroll_arrow').on('click', (event) => infiniteScroll(true, event));
}

$(document).ready(loadEvents);