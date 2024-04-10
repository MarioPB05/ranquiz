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
function initializeFlatpickr(elementSelector, mode = 'single', minDate = '01-01-1900') {
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

export {removePageLoader, initializeFlatpickr, promiseAjax, toastMessage};