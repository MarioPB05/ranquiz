import { removePageLoader } from "/static/assets/js/ranquiz/utils.js";

$(document).ready(function() {
    removePageLoader();
    $("#range_date_highlight").daterangepicker({
        minDate: moment(),
        locale: {
            format: 'DD/MM/YYYY',
        }
    });

    // $("#visibility").select2({
    //     hide_search: true,
    // });

});


$('#name').maxlength({
    warningClass: "badge badge-primary",
    limitReachedClass: "badge badge-danger"
});


