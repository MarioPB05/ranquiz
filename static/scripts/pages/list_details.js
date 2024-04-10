import { removePageLoader, formatElapsedTime } from "/static/assets/js/ranquiz/utils.js";

removePageLoader();

const templateComment = $("#template_comment");
const templateAward = $("#template_award");
let templateBuyableAward = $("#template_buyable_award");

const commentsOnPage = [];

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

let awards = [];

/**
 * Obtiene los premios de la base de datos y los añade a la lista de premios en el comentario plantilla
 */
function getAwards() {
    // TODO: Get awards from the database
    awards = [
        {
            "id": 1,
            "name": "Legendario",
            "icon": "bi-trophy-fill",
            "color": "orange",
            "price": 10
        },

        {
            "id": 2,
            "name": "Good",
            "icon": "bi-ui-checks-grid",
            "color": "#23B0FF",
            "price": 5
        }
    ];

    $.each(awards, function (index, award) {
        let award_element = templateBuyableAward.clone();
        award_element.removeAttr("id");
        award_element.removeClass("d-none").addClass("d-flex");

        award_element.find(".award_name").text(award.name);
        award_element.find(".award_icon").addClass(award.icon);
        award_element.find("a").css("background-color", award.color);
        award_element.find(".award_price").text(award.price);

        award_element.appendTo(templateComment.find(".menu"));
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
    let comment_temp_id = "award_comment_" + commentsOnPage.length;

    let element = templateComment.clone();

    element.removeAttr("id");
    element.removeClass("d-none").addClass("d-flex");

    element.find(".comment_content").text(content);
    element.find(".author_name").text(author_name);
    // TODO: Add author avatar
    element.find(".comment_date").text(formatElapsedTime(date));

    element.find("#award_comment_first").attr("id", comment_temp_id);
    element.find('[data-kt-menu]').each(function () {
        const menu = new KTMenu($(this)[0]);
    });

    commentsOnPage.push(comment);
    element.appendTo("#comments_container");
}

/**
 * Sube un comentario a la base de datos
 * @param comment
 * @returns {*}
 */
function uploadComment(comment) {
    return exampleComment;
}

/**
 * Añade el comentario que se ha escrito en la base de datos y a los comentarios
 */
function writeComment() {
    let content = $("#comment_input").val();
    let date = new Date();

    let comment = {
        "content": content,
        "date": date,
    };

    $("#comment_input").val("");

    addComment(uploadComment(comment));
}

$(document).ready(function () {
    getAwards();
    addComment(exampleComment);

    $("#write_comment").click(writeComment);
});
