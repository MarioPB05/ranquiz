const Toast = Swal.mixin({ // skipcq: JS-0125
  toast: true,
  position: "top-end",
  showConfirmButton: false,
  timer: 3000,
  timerProgressBar: true,
  didOpen: (toast) => {
    toast.onmouseenter = Swal.stopTimer; // skipcq: JS-0125
    toast.onmouseleave = Swal.resumeTimer; // skipcq: JS-0125
  }
});


/**
 * Esta función se encarga de remover el loader de la página
 */
function removePageLoader() {
    $('body').css("overflow-y", "auto");
    $('#loading_indicator').removeClass("d-flex");
}

/**
 * Esta función se encarga de inicializar el componente Flatpickr
 * @param elementSelector
 * @param mode
 * @param minDate
 * @returns {*|[]}
 */
function initializeFlatpickr(elementSelector, mode = 'single', minDate = '1900-01-01') {
    return flatpickr(elementSelector, { // skipcq: JS-0125
        mode,
        dateFormat: 'Y-m-d',
        altFormat: 'd/m/Y',    // Formato de fecha alternativo que se enviará al backend
        altInput: true,
        minDate,
        locale: {
            firstDayOfWeek: 1,
            weekdays: {
                shorthand: ['Do', 'Lu', 'Ma', 'Mi', 'Ju', 'Vi', 'Sa'],
                longhand: ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'],
            },
            months: {
                shorthand: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
                longhand: ['Enero', 'Febrero', 'Мarzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
            },

            rangeSeparator: ' hasta ',
        },
    });
}


/***
* Esta función se encarga de realizar una petición AJAX
* @param url
* @param data
* @param method
* @returns {Promise<unknown>}
 */
function promiseAjax(url, method = 'GET', data = null) {
    return new Promise((resolve, reject) => {
        $.ajax({
            url,
            method,
            data,
            success: resolve,
            error: reject
        });
    });
}

/**
 * Esta función se encarga de mostrar un mensaje de tipo toast
 * @param icon
 * @param message
 */
function toastMessage(icon, message) {
    Toast.fire({
        icon,
        title: message
    });
}

function infoLog(message) {
    console.log(
        '%c INFO ',
        'background-color: #BD20E9;color: white;font-weight: bold;border-radius:2px;padding: 2px 6px;',
        message
    ); // skipcq: JS-0002
}

function warningLog(message) {
    console.log(
        '%c WARNING ',
        'background-color: #f1bc00;color: white;font-weight: bold;border-radius:2px;padding: 2px 6px;',
        message
    ); // skipcq: JS-0002
}

function errorLog(message) {
    console.log(
        '%c ERROR ',
        'background-color: #d9214e;color: white;font-weight: bold;border-radius:2px;padding: 2px 6px;',
        message
    ); // skipcq: JS-0002
}

export {removePageLoader, initializeFlatpickr, promiseAjax, toastMessage, infoLog, warningLog, errorLog};