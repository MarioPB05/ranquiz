/*global $, share_code*/

import { toggleListLike } from "/static/assets/js/ranquiz/utils.js";

let page = 2;
let isLoadingData = false;

function redirectToList(event) {
    if (event.target.tagName === "A") return;

    const url = $(event.currentTarget).attr("href");
    if (url) window.location.href = url;
}

function isScrollNearEnd() {
    const element = $('.scroll');
    return element.scrollLeft() + element.outerWidth() >= element[0].scrollWidth - 100;
}

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

function infiniteScroll(scroll = false) {
    if (isScrollNearEnd()) loadMoreData();

    if (scroll) {
        const element = $('.scroll');
        element.animate({scrollLeft: element.scrollLeft() + 500}, 500);
    }
}

function loadEvents() {
    $('.list').on('click', redirectToList);
    $('.list_like').on('click', toggleListLike);

    $('.scroll').scroll(() => infiniteScroll());
    $('#list_arrow_right').on('click', () => infiniteScroll(true));
}

$(document).ready(loadEvents);