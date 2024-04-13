import {removePageLoader, formatElapsedTime, toastMessage, promiseAjax} from "/static/assets/js/ranquiz/utils.js";

const blockUI = new KTBlockUI($("#comments_container").parent()[0], {
    message: '<div class="blockui-message"><span class="spinner-border text-primary"></span>Cargando comentarios...</div>',
});
const templateComment = $("#template_comment");
const templateAward = $("#template_award");
let templateBuyableAward = $("#template_buyable_award");

let comments = [];
let awards = [];


/**
 * Obtiene los premios de la base de datos y los añade a la lista de premios en el comentario plantilla
 */
function getAwards() {
    // TODO: Get awards from the database
    awards = [
        {
            "id": 1,
            "title": "Legendario",
            "icon": "bi-trophy-fill",
            "color": "orange",
            "price": 10
        },

        {
            "id": 2,
            "title": "Good",
            "icon": "bi-ui-checks-grid",
            "color": "#23B0FF",
            "price": 5
        }
    ];

    $.each(awards, function (index, award) {
        let award_element = templateBuyableAward.clone();
        award_element.removeAttr("id");
        award_element.removeClass("d-none").addClass("d-flex");

        award_element.find(".award_name").text(award.title);
        award_element.find(".award_icon").addClass(award.icon);
        award_element.find("div").css("background-color", award.color);
        award_element.find(".award_price").text(award.price);

        award_element.attr("data-award-id", award.id);

        award_element.appendTo(templateComment.find(".menu"));
    });
}

function addAwardToComment(award_id, comment) {
    let award = awards.find(award => award.id === award_id);

    if (comment.find(`div.award[data-award-id=${award_id}]`).length > 0) {
        comment.find(`div.award[data-award-id=${award_id}]`).find(".award_amount").text(parseInt(comment.find(`div.award[data-award-id=${award_id}]`).find(".award_amount").text()) + 1);
        console.log(comment.find(`div.award[data-award-id=${award_id}]`));

    } else {
        let award_element = templateAward.clone();
        award_element.removeAttr("id");
        award_element.removeClass("d-none").addClass("d-flex");

        award_element.find(".award_icon").addClass(award.icon);
        award_element.find(".award_name").text(award.title);
        award_element.find(".award_amount").text(1);
        award_element.css("background-color", award.color);

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
    let award = awards.find(award => award.id === award_id);
    let id_comment = comment.attr("data-comment-id");
    let token = $('input[name=csrfmiddlewaretoken]').val();

    promiseAjax(`/api/list/${share_code}/comment/${id_comment}/add_award`, "POST", {"id_award": award_id, "csrfmiddlewaretoken": token}).then(response => {
        addAwardToComment(comment, award_id, award);
    });
}

/**
 * Añade un comentario a la lista de comentarios
 * @param comment
 */
function addComment(comment) {
    let content = comment.content;
    let author_name = comment.author.name;
    let author_avatar = comment.author.avatar;
    let date = new Date(comment.date);
    let awards = comment.awards;
    let id = comment.id;

    console.log(comment);

    let element = templateComment.clone();

    element.removeAttr("id");
    element.removeClass("d-none").addClass("d-flex");
    element.attr("data-comment-id", id);

    element.find(".comment_content").text(content);
    element.find(".author_name").text(author_name);
    element.find(".author_avatar").attr("src", author_avatar);
    element.find(".comment_date").text(formatElapsedTime(date));

    element.find('[data-kt-menu]').each(function () {
        const menu = new KTMenu($(this)[0]);
    });

    if (awards) {
        $.each(awards, function (index, award) {
            addAwardToComment(award.id_award, element);
        });
    }

    element.prependTo("#comments_container");
    actualizeCommentCounter();
}

/**
 * Obtiene los comentarios de la base de datos y los añade
 * @param mode
 */
function getComments(mode = "featured") {
    $("#comments_container").empty();
    comments = [];

    console.log(blockUI)
    blockUI.block();

    promiseAjax(`/api/list/${share_code}/comments?mode=${mode}`).then(response => {
        comments = response.comments;

        $.each(comments, function (index, comment) {
            addComment(comment);
        });

        blockUI.release();

        actualizeCommentCounter();

    }).catch(error => {
        toastMessage("error", "Error al obtener los comentarios" + error);
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

    promiseAjax(`/api/list/${share_code}/comment/create`, "POST", comment).then(response => {
        addComment(response.comment);
        comments.push(response.comment);
        actualizeCommentCounter();

    }).catch(error => {
        toastMessage("error", "Error al subir el comentario");
    });
}

function actualizeCommentCounter() {
    $("#comment_counter").text(comments.length);
}

/**
 * Añade el comentario que se ha escrito en la base de datos y a los comentarios
 */
function writeComment() {
    let content = $("#comment_input").val();

    if (!content.trim()) {
        return;
    }

    let comment = {
        "content": content
    };

    $("#comment_input").val("");

    uploadComment(comment);
}

/**
 * Cambia entre comentarios recientes y destacados
 */
function toggleRecientComments() {
    if ($("#recientComents").hasClass("badge-outline-primary-selected")) {
        $("#recientComents").removeClass("badge-outline-primary-selected");
        getComments("featured")
    }else {
        $("#recientComents").addClass("badge-outline-primary-selected");
        getComments("recient");
    }
}

function handleIconClick() {
    // Función para manejar el clic en los elementos de corazones y estrellas
    $('.cursor-pointer').click(function() {
        var countLabel = $(this).next('label');
        var icon = $(this).find('i');

        // Obtener el número actual
        var count = parseInt(countLabel.text());

        // Verificar el ID del icono y aplicar la clase correspondiente
        if (icon.attr('id') === 'heart-count') {
            // Si el icono es el de corazón, añadir la clase heart-selected
            icon.toggleClass("heart-selected");
        } else if (icon.attr('id') === 'star-count') {
            // Si el icono es el de estrella, añadir la clase star-selected
            icon.toggleClass("star-selected");
        }

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
    });
}

// Llamar a la función para que maneje los clics en los iconos
handleIconClick();

$(document).ready(function () {
    getAwards();
    getComments();

    $("#write_comment").click(writeComment);

    $("#recientComents").click(toggleRecientComments)

     $("#comments_container").on("click", ".buyable_award", function () {
        let award_id = $(this).data("award-id");
        let comment = $(this).parent().parent().parent().parent();

        console.log(award_id);
        console.log(comment);

        uploadAward(award_id, comment, true);
    });

     removePageLoader();
});


