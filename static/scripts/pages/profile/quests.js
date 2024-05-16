/*global $, Confetti*/
import {promiseAjax, toastMessage, reloadUserData, secondsToTime} from "/static/assets/js/ranquiz/utils.js";
const confetti = [];

/**
 * Claim a quest
 * @param goal_id
 * @param element_id
 * @param event
 */
function claimQuest(goal_id, element_id, event) {
    promiseAjax(`/api/quest/claim?goal=${goal_id}`, "GET").then((response) => {
        if (response.status === "success") {
            confetti[element_id].burst(event.clientX, event.clientY);
            reloadUserData();
            $(`#${element_id}`).find(".claim_quest").remove();
            $(`#${element_id}`).find(".quest_completed").removeClass("d-none");
        }else {
            toastMessage("error", response.message);
            $(`#${element_id}`).find(".claim_quest").removeClass("disabled");
        }
    }).catch(() => {
        toastMessage("error", "Ha ocurrido un error al intentar reclamar la misión");
        $(`#${element_id}`).find(".claim_quest").removeClass("disabled");
    });
}

function updateCountdown() {
    // Get the current time
    const now = new Date();

    // Get the time for the next midnight
    const tomorrow = new Date();
    tomorrow.setHours(24, 0, 0, 0); // Set to next midnight

    // Calculate the difference in seconds
    const secondsLeft = Math.floor((tomorrow - now) / 1000);

    // Update the countdown element
    $('#countdown').text(secondsToTime(secondsLeft));
}

$(document).ready(() => {

    $(".claim_quest").each((index, element) => {
        confetti[$(element).parent().attr("id")] = new Confetti($(element).parent().attr("id"));
        confetti[$(element).parent().attr("id")].setCount(75);
        confetti[$(element).parent().attr("id")].setSize(1);
        confetti[$(element).parent().attr("id")].setPower(25);
        confetti[$(element).parent().attr("id")].setFade(false);
        confetti[$(element).parent().attr("id")].destroyTarget(false);
    });

    $(".claim_quest").on("click", (event) => {
        event.stopPropagation();
        const id = $(event.currentTarget).parent().attr("id");
        const goal_id = id.split("_")[1];
        $(event.currentTarget).blur();
        $(event.currentTarget).addClass("disabled");
        claimQuest(goal_id, id, event);
    });

    // Update the countdown immediately
    updateCountdown();

    // Update the countdown every second
    setInterval(updateCountdown, 1000);
});
