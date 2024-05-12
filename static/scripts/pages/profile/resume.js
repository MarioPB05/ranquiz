/*global $, share_code*/

import { toggleListLike } from "/static/assets/js/ranquiz/utils.js";

let page = 2;
let isLoadingData = false;

/**
 * Redirige a la lista seleccionada
 *
 * @param event
 */
function redirectToList(event) {
    if (event.target.tagName === "A") return;

    const url = $(event.currentTarget).attr("href");
    if (url) window.location.href = url;
}

/**
 * Verifica si el scroll está cerca del final del contenedor
 *
 * @returns {boolean}
 */
function isScrollNearEnd() {
    const element = $('.scroll');
    return element.scrollLeft() + element.outerWidth() >= element[0].scrollWidth - 100;
}

/**
 * Carga más datos en la sección de listas del perfil
 */
function loadMoreData() {
    if (isLoadingData) return;
    isLoadingData = true;

    $.ajax({
        url: `/api/user/${share_code}/lists?page=${page}`,
        type: 'GET',
        /**
         * Función que se ejecuta si la petición AJAX fue exitosa
         *
         * @param data
         * @param {Array} data.lists
         */
        success(data) {
            if (data.lists.length === 0) return;

            page++;
            isLoadingData = false;
            const newData = data.lists;

            newData.forEach(function(item) {
                const listItem = $('<div class="min-w-375px"></div>').html(item);
                $('.scroll').append(listItem);
            });
        }
    });


}

/**
 * Realiza un scroll infinito en la sección de listas del perfil
 *
 * @param scroll
 */
function infiniteScroll(scroll = false) {
    if (isScrollNearEnd()) loadMoreData();

    if (scroll) {
        const element = $('.scroll');
        element.animate({scrollLeft: element.scrollLeft() + 500}, 500);
    }
}

/**
 * Carga los eventos de la página
 */
function loadEvents() {
    $('.list').on('click', redirectToList);
    $('.list_like').on('click', toggleListLike);

    $('.scroll').scroll(() => infiniteScroll());
    $('#list_arrow_right').on('click', () => infiniteScroll(true));
}

$(document).ready(loadEvents);