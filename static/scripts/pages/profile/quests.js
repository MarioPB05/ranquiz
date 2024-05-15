import {promiseAjax, toastMessage, reloadUserData} from "/static/assets/js/ranquiz/utils.js";
let confetti = [];

function claimQuest(goal_id, element_id, event) {
    promiseAjax(`/api/quest/claim?goal=${goal_id}`, "GET").then((response) => {
        if (response.status === "success") {
            confetti[element_id].burst(event.clientX, event.clientY);
            reloadUserData();
            $(`#${element_id}`).find(".claim_quest").remove();
            $(`#${element_id}`).find(".quest_completed").removeClass("d-none");
        }
    }).catch(() => {
        toastMessage("error", "Ha ocurrido un error al intentar reclamar la misión");
        $(`#${element_id}`).find(".claim_quest").removeClass("disabled");
    });
}

$(document).ready(() => {

    $(".claim_quest").each((index, element) => {
        confetti[$(element).parent().attr("id")] = new Confetti($(element).parent().attr("id"));
        confetti[$(element).parent().attr("id")].setCount(75);
        confetti[$(element).parent().attr("id")].setSize(1);
        confetti[$(element).parent().attr("id")].setPower(25);
        confetti[$(element).parent().attr("id")].setFade(false);
        confetti[$(element).parent().attr("id")].destroyTarget(false);
        console.log($(element).parent().attr("id"));
    });

    $(".claim_quest").on("click", (event) => {
        event.stopPropagation();
        const id = $(event.currentTarget).parent().attr("id");
        const goal_id = id.split("_")[1];
        $(event.currentTarget).blur();
        $(event.currentTarget).addClass("disabled");
        claimQuest(goal_id, id, event);
    });
});
