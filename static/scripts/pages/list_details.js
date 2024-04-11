import {removePageLoader, formatElapsedTime, toastMessage, promiseAjax} from "/static/assets/js/ranquiz/utils.js";


const templateComment = $("#template_comment");
const templateAward = $("#template_award");
let templateBuyableAward = $("#template_buyable_award");

let comments = [];
let awards = [];

let exampleComment = {
    "id": 1,
    "author": {
        "name": "John Doe",
        "avatar": "https://via.placeholder.com/150"
    },
    "content": "This is a comment",
    "date": "2021-05-01T12:00:00Z",
    "awards": [
        {
            "id_award": 1,
            "amount": 1
        },

        {
            "id_award": 2,
            "amount": 5
        }
    ]
};

/**
 * Obtiene los premios de la base de datos y los añade a la lista de premios en el comentario plantilla
 */
function getAwards() {
    // TODO: Get awards from the database
    awards = [
        {
            "id": 1,
            "title": "Legendario",
            "icon": "bi bi-trophy-fill",
            "color": "orange",
            "price": 10
        },

        {
            "id": 2,
            "title": "Good",
            "icon": "bi bi-ui-checks-grid",
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

/**
 * Añade un premio a un comentario
 * @param award_id
 * @param comment
 * @param new_award
 */
function addAwardToComment(award_id, comment, new_award = false) {
    let award = awards.find(award => award.id === award_id);

    if (!new_award && uploadAward(award_id, comment.data("comment-id")).state !== "success") {
        return;

    }else if (new_award) {
        toastMessage("success", "Premio otorgado");
    }

    if (comment.find(`div.award[data-award-id=${award_id}]`).length > 0) {
        comment.find(`div.award[data-award-id=${award_id}]`).find(".award_amount").text(parseInt(comment.find(`div.award[data-award-id=${award_id}]`).find(".award_amount").text()) + 1);
        console.log(comment.find(`div.award[data-award-id=${award_id}]`));

    }else {
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
        console.log(comment.find(".award_container"));
    }
}

/**
 * Sube un premio a la base de datos
 * @param id_award
 * @param id_comment
 * @returns {{reason: string, state: string, id_award}}
 */
function uploadAward(id_award, id_comment) {
    // TODO: Subir premio a la base de datos
    return {
        "state": "success",
        "reason": "Premio subido correctamente",
        id_award
    }
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

    console.log(comment);

    let element = templateComment.clone();

    element.removeAttr("id");
    element.removeClass("d-none").addClass("d-flex");

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

    element.appendTo("#comments_container");
    actualizeCommentCounter();
}

/**
 * Obtiene los comentarios de la base de datos y los añade
 */
function getComments() {
    promiseAjax(`/api/list/${share_code}/comments`).then(response => {
        comments = response.comments;

        $.each(comments, function (index, comment) {
            addComment(comment);
        });

        actualizeCommentCounter();

    }).catch(error => {
        toastMessage("error", "Error al obtener los comentarios");
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

    if (!content) {
        return;
    }

    let comment = {
        "content": content
    };

    $("#comment_input").val("");

    uploadComment(comment);
}

$(document).ready(function () {
    getAwards();
    getComments();

    $("#write_comment").click(writeComment);

     $("#comments_container").on("click", ".buyable_award", function () {
        let award_id = $(this).data("award-id");
        let comment = $(this).parent().parent().parent().parent();

        console.log(award_id);
        console.log(comment);

        addAwardToComment(award_id, comment, true);
    });

    removePageLoader();
});
