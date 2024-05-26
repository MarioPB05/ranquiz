import {
    removePageLoader,
    formatElapsedTime,
    toastMessage,
    promiseAjax,
    secondsToTime,
    reloadUserData
} from "/static/assets/js/ranquiz/utils.js";

const commentsContainer = $("#comments_container");
const blockUI = new KTBlockUI(commentsContainer.parent()[0], {  // skipcq: JS-0125
    message: '<div class="blockui-message"><span class="spinner-border text-primary"></span>Cargando comentarios...</div>',
});
const blockLikeBtn = new KTBlockUI($("#heart-btn")[0]);  // skipcq: JS-0125
const blockFavoriteBtn = new KTBlockUI($("#star-btn")[0]);  // skipcq: JS-0125
const templateComment = $("#template_comment");
const templateAward = $("#template_award");
const templateBuyableAward = $("#template_buyable_award");
const commentAlert = $("#comment_alert");

let comments = [];
let awards = [];


/**
 * Obtiene los premios de la base de datos y los añade a la lista de premios en el comentario plantilla
 */
function getAwards() {
    promiseAjax("/api/social/awards").then(response => {
        awards = response.awards;

        $.each(awards, (index, award) => {
            const award_element = templateBuyableAward.clone();
            award_element.removeAttr("id");
            award_element.removeClass("d-none").addClass("d-flex");

            award_element.find(".award_name").text(award.title);
            award_element.find(".award_icon").addClass(award.icon);
            award_element.find("div").css("background-color", award.color);
            award_element.find(".award_price").text(award.price);

            award_element.attr("data-award-id", award.id);

            award_element.appendTo(templateComment.find(".menu"));
        });

    }).catch(() => {
        toastMessage("error", "Error al obtener los premios");
    });
}

/**
 * Añade un premio a un comentario
 * @param award_id
 * @param comment
 */
function addAwardToComment(award_id, comment, amount=1) {
    const found_award = awards.find(award => award.id === award_id);

    if (comment.find(`div.award[data-award-id=${award_id}]`).length > 0) {
        comment.find(`div.award[data-award-id=${award_id}]`).find(".award_amount").text(parseInt(comment.find(`div.award[data-award-id=${award_id}]`).find(".award_amount").text()) + 1);

    } else {
        const award_element = templateAward.clone();
        award_element.removeAttr("id");
        award_element.removeClass("d-none").addClass("d-flex");
        award_element.attr("title", found_award.title);

        const tooltip = new bootstrap.Tooltip(award_element); // skipcq: JS-0125, JS-0128

        award_element.find(".award_icon").addClass(found_award.icon);
        award_element.find(".award_amount").text(amount);
        award_element.css("background-color", found_award.color);

        award_element.attr("data-award-id", award_id);
        award_element.removeClass("d-none").addClass("d-flex");

        award_element.appendTo(comment.find(".award_container"));
    }
}

/**
 * Sube un premio a la base de datos
 * @param award_id
 * @param comment
 */
function uploadAward(award_id, comment) {
    const id_comment = comment.attr("data-comment-id");
    const token = $('input[name=csrfmiddlewaretoken]').val();
    const comment_add_award = comment.find(".add_award");
    comment_add_award.attr("disabled", "disabled");
    comment_add_award.addClass("opacity-75");

    promiseAjax(`/api/list/${share_code}/comment/${id_comment}/add_award`, "POST", {  // skipcq: JS-0125
        "id_award": award_id,
        "csrfmiddlewaretoken": token
    }).then(response => {
        if (response.status === "Success") {
            addAwardToComment(award_id, comment);
            toastMessage("success", "Premio otorgado");
            reloadUserData();
        }else if (response.status === "Error") {
            toastMessage("error", response.message);
        }
        comment_add_award.removeAttr("disabled");
        comment_add_award.removeClass("opacity-75");
    }).catch(() => {
        toastMessage("error", "Error al subir el premio");
        comment_add_award.removeClass("opacity-75");
    });
}

/**
 * Añade un comentario a la lista de comentarios
 * @param comment
 */
function addComment(comment, new_comment = false) {
    const content = comment.content;
    const author_name = comment.author.name;
    const author_avatar = comment.author.avatar;
    const author_url = comment.author.url;
    const date = new Date(comment.date);
    const comment_awards = comment.awards;
    const id = comment.id;
    const user_is_athor = comment.user_is_author;
    const user_is_list_author = comment.user_is_list_author;

    const element = templateComment.clone();

    element.removeAttr("id");
    element.removeClass("d-none").addClass("d-flex");
    element.attr("data-comment-id", id);

    if (user_is_athor === true) {
        element.find(".add_award").parent().remove();
        element.find(".own_comment_badge").removeClass("d-none");
    }else if (user_is_list_author === true) {
        element.find(".creator_comment_badge").removeClass("d-none");
    }

    element.find(".comment_content").text(content);
    element.find(".author_name").text(author_name);
    element.find(".author_avatar").attr("src", author_avatar);
    element.find(".author_group").attr("href", author_url);
    element.find(".comment_date").text(formatElapsedTime(date));

    element.find('[data-kt-menu]').each(function () {
        new KTMenu($(this)[0]);  // skipcq: JS-0125, JS-R1002
    });

    if (comment_awards) {
        $.each(comment_awards, (index, award) => {
            addAwardToComment(award.id_award, element, award.amount);
        });
    }

    if (new_comment) {
        element.prependTo("#comments_container");
    }else {
        element.appendTo("#comments_container");
    }

    actualizeCommentCounter();
}

/**
 * Obtiene los comentarios de la base de datos y los añade
 * @param mode
 */
function getComments(mode = "recent") {
    commentsContainer.empty();
    comments = [];

    blockUI.block();

    promiseAjax(`/api/list/${share_code}/comments?mode=${mode}`).then(response => {  // skipcq: JS-0125
        comments = response.comments;

        $.each(comments, (index, comment) => {
            addComment(comment);
        });

        if (comments.length === 0) {
            commentAlert.appendTo("#comments_container");
        }

        blockUI.release();

        actualizeCommentCounter();

    }).catch(() => {
        toastMessage("error", "Error al obtener los comentarios");
        blockUI.release();
    });
}

/**
 * Sube un comentario a la base de datos
 * @param comment
 * @returns {*}
 */
function uploadComment(comment) {
    comment.csrfmiddlewaretoken = $('input[name=csrfmiddlewaretoken]').val();

    promiseAjax(`/api/list/${share_code}/comment/create`, "POST", comment).then(response => {  // skipcq: JS-0125
        addComment(response.comment, true);
        comments.push(response.comment);
        actualizeCommentCounter();

        if (comments.length === 1) {
            commentAlert.remove();
        }

        // Animación de scroll
        commentsContainer.animate({ scrollTop: 0 }, "slow");

        // Animación de resaltado
        commentsContainer.children().first().css("background-color", "lightyellow").delay(1000).queue(function(next) {
            $(this).css("background-color", ""); // Restaurar el color original
            next();
        });

    }).catch(() => {
        toastMessage("error", "Error al subir el comentario");
    });
}

/**
 * Actualiza el contador de comentarios
 */
function actualizeCommentCounter() {
    $("#comment_counter").text(comments.length);
}

/**
 * Añade el comentario que se ha escrito en la base de datos y a los comentarios
 */
function writeComment() {
    const content = $("#comment_input").val();

    if (content.length > $("#comment_input").attr("maxlength")) {
        toastMessage("error", "El comentario es demasiado largo");
        return;
    }

    if (!content.trim()) {
        return;
    }

    const comment = { content };

    $("#comment_input").val("");
    autosize.update($("#comment_input"));  // skipcq: JS-0125

    uploadComment(comment);
}

/**
 * Cambia entre comentarios recientes y destacados
 */
function toggleSort(event) {
    const all = $(".sort_button");
    const element = $(event.currentTarget);

    if (element.hasClass("badge-outline-primary-selected")) {
        element.removeClass("badge-outline-primary-selected");
    } else {
        all.removeClass("badge-outline-primary-selected");
       element.addClass("badge-outline-primary-selected");
    }

    if (!all.hasClass("badge-outline-primary-selected")) {
        getComments("recent");
    }else if (element.data("mode") === "featured") {
        getComments("featured");
    }else if (element.data("mode") === "own") {
        getComments("own");
    }

}

/**
 * Maneja el clic en los elementos de corazones y estrellas
 */
function handleIconClick() {
    // Función para manejar el clic en los elementos de corazones y estrellas
    const countLabel = $(this).next('label');
    const icon = $(this).find('i');

    // Obtener el número actual
    let count = parseInt(countLabel.text());

    // Incrementar o disminuir según la clase del icono
    if (icon.hasClass("heart-selected") || icon.hasClass("star-selected")) {
        // Incrementar el número
        count += 1;
    } else {
        // Disminuir el número
        count -= 1;
    }

    // Actualizar el número mostrado
    countLabel.text(count);
}

/**
 * Añadir o eliminar un like a la lista
 */
function handleLikeClick() {
    if (blockLikeBtn.isBlocked()) return;

    blockLikeBtn.block();

    promiseAjax(`/api/list/${share_code}/like`, "GET").then(response => {  // skipcq: JS-0125
        if (response.status === "success") {
            $(this).find('i').toggleClass('heart-selected');
            $(this).trigger("custom_click");
        } else if (response.status === "error") {
            toastMessage("error", response.message);
        }

        blockLikeBtn.release();
    }).catch(() => {
        toastMessage("error", "Error al dar like a la lista");
        blockLikeBtn.release();
    });
}

/**
 * Añadir o eliminar un favorito a la lista
 */
function handleFavoriteClick() {
    if (blockFavoriteBtn.isBlocked()) return;

    blockFavoriteBtn.block();

    promiseAjax(`/api/list/${share_code}/favorite`, "GET").then(response => {  // skipcq: JS-0125
        if (response.status === "success") {
            $(this).find('i').toggleClass('star-selected');
            $(this).trigger("custom_click");
        } else if (response.status === "error") {
            toastMessage("error", response.message);
        }

        blockFavoriteBtn.release();
    }).catch(() => {
        toastMessage("error", "Error al dar favorito a la lista");
        blockFavoriteBtn.release();
    });
}


/**
 * Obtener cuando se ha hecho click en el botón de compartir lista
 */
function onShareList() {
    toastMessage('success', '¡URL copiada al portapapeles!');
}

/**
 * Calcular el tiempo que le va a llevar al usuario completar la lista aproximadamente.
 */
function calculatePlayTime(items, mode) {
    const time_per_duel = 3;
    let total_time = 0;

    if (mode === 4) {
        total_time = items * time_per_duel * 2;
    } else if (mode === 2) {
        total_time = items * 3 * time_per_duel;
    }

    return secondsToTime(total_time, 2)
}

/**
 * Recargar el tiempo de juego estimado
 */
function reloadPlaytime() {
    const duel_items = parseInt($("#duel_elements_selector").val());
    const total_items = $("#total_items").text();
    const play_time = calculatePlayTime(total_items, duel_items);

    $("#estimated_playtime").text(play_time);
}

/**
 * Función que se ejecuta cuando el documento está listo
 */
function onDocumentReady() {
    const clipboardShareList = new ClipboardJS($('#share_list')[0]);  // skipcq: JS-0125

    clipboardShareList.on('success', onShareList);
    getAwards();
    getComments();
    handleIconClick();

    $("#write_comment").click(writeComment);
    $("#comment_input").on("keypress", function (event) {
        if (event.which === 13) { // Verificar si la tecla presionada es "Enter" (código 13)
            if ($(this).val()) {
                writeComment();
            }
            event.preventDefault();
        }

    });

    $(".sort_button").click(toggleSort)

    commentsContainer.on("click", ".buyable_award", function () {
        const award_id = $(this).data("award-id");
        const comment = $(this).parent().parent().parent().parent();

        uploadAward(award_id, comment);
    });

    $('.cursor-pointer').on("custom_click", handleIconClick);
    $('#heart-btn').on("click", handleLikeClick);
    $('#star-btn').on("click", handleFavoriteClick);


    $("#duel_elements_selector").on("change", reloadPlaytime);

    reloadPlaytime();
    removePageLoader();
}

$(document).ready(onDocumentReady);
