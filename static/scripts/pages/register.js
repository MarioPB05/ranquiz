import {removePageLoader} from "/static/assets/js/ranquiz/utils.js";

$(document).ready(() => {

    const element = document.querySelector("#kt_stepper_example_basic");
    const stepper = new KTStepper(element);

    stepper.on("kt.stepper.next", function (stepper) {
        stepper.goNext();
    });

    stepper.on("kt.stepper.previous", function (stepper) {
        stepper.goPrevious();
    });
    removePageLoader();
});