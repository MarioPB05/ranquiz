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
function initializeFlatpickr(elementSelector, mode = 'single', minDate = '1920-01-01') {
    return flatpickr(elementSelector, { // skipcq: JS-0125
        mode: mode,
        dateFormat: 'd-m-Y',
        minDate: minDate,
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

function formatElapsedTime(dateTime) {
    let currentDate = new Date();
    let elapsedTime = currentDate - dateTime;
    let elapsedSeconds = Math.floor(elapsedTime / 1000);

    if (elapsedSeconds < 60) {
        return "Hace " + elapsedSeconds + " s";
    }

    let elapsedMinutes = Math.floor(elapsedSeconds / 60);
    if (elapsedMinutes < 60) {
        return "Hace " + elapsedMinutes + " min";
    }

    let elapsedHours = Math.floor(elapsedMinutes / 60);
    if (elapsedHours < 24) {
        return "Hace " + elapsedHours + " h";
    }

    let elapsedDays = Math.floor(elapsedHours / 24);
    if (elapsedDays < 30) {
        return "Hace " + elapsedDays + " d";
    }

    // If it has been more than a month, return the original date
    return dateTime.toLocaleDateString();
}



export { removePageLoader, initializeFlatpickr, formatElapsedTime };

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
            url: url,
            method: method,
            data: data,
            success: function (response) {
                resolve(response);
            },
            error: function (error) {
                reject(error);
            }
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
        icon: icon,
        title: message
    });
}

export {removePageLoader, initializeFlatpickr, promiseAjax, toastMessage};