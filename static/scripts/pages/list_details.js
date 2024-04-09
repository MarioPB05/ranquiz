import { removePageLoader, formatElapsedTime } from "/static/assets/js/ranquiz/utils.js";

removePageLoader();

const templateComment = $("#template_comment");
const templateAward = $("#template_award");

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
            "name": "Best Comment",
            "icon": "fa-trophy",
            "color": "gold",
            "amount": 1
        },

        {
            "name": "Good Comment",
            "icon": "fa-thumbs-up",
            "color": "blue",
            "amount": 5
        }
    ]
};


function addComment(comment) {
    let content = comment.content;
    let author_name = comment.author.name;
    let author_avatar = comment.author.avatar;
    let date = new Date(comment.date);
    let awards = comment.awards;

    let element = templateComment.clone();

    element.removeAttr("id");
    element.removeClass("d-none").addClass("d-flex");

    element.find(".comment_content").text(content);
    element.find(".author_name").text(author_name);
    // TODO: Add author avatar
    element.find(".comment_date").text(formatElapsedTime(date));

    element.appendTo("#comments_container");
}

$(document).ready(function () {
    addComment(exampleComment);
});
