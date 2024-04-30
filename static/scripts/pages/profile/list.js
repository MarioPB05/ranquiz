import {promiseAjax} from "/static/assets/js/ranquiz/utils.js";

function toggleVisibility(event) {
    const share_code = $(this).data('share_code');
    const parent = $(this).closest('.list_item');

    console.log(parent)

    promiseAjax(`/api/list/${share_code}/visibility`, 'GET').then((data) => {
        if (data.status === 'success') {
            const icon = $(this).find('i');

            if (icon.hasClass('bi-eye-slash-fill')) {
                icon.removeClass('bi-eye-slash-fill').addClass('bi-eye-fill');
            } else {
                icon.removeClass('bi-eye-fill').addClass('bi-eye-slash-fill');
            }

            $(this).blur();
        }
    });

    event.stopPropagation();
}

function redirectToList() {
    window.location.href = $(this).data('url');
}

function loadEvents() {
    $('#list_container')
        .on('click', '.toggle_visibility_list', toggleVisibility)
        .on('click', '.list_item', redirectToList);

}

$(document).ready(loadEvents);