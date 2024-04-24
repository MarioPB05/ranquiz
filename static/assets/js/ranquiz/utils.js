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
 * Esta función se encarga de volver a añadir el loader de la página
 */
function addPageLoader() {
    $('body').css("overflow-y", "hidden");
    $('#loading_indicator').addClass("d-flex");
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

/**
 * Esta función se encarga de recargar la información del usuario
 */
function reloadUserData() {
    promiseAjax('/api/user')
        /**
         * @param response
         * @param response.user Información del usuario
         * @param response.user.avatar URL del avatar del usuario
         * @param response.user.money Gemas del usuario
         */
        .then((response) => {
            if (response.user) {
                $('.user_avatar').attr('src', response.user.avatar);
                $('.user_money').text(response.user.money);
            }
        });
}

/**
 * Esta función tiene como objetivo transformar un número de segundos en un formato de cantidades de tiempo.
 */
function secondsToTime(seconds, digits) {
    let time = {
        "d": 86400,
        "h": 3600,
        "m": 60,
        "s": 1
    };

    let timeString = "";
    let count = 0;

    if (seconds > 2592000) {
        return new Date(seconds * 1000).toLocaleDateString();
    }

    for (let key in time) {
        if (Object.prototype.hasOwnProperty.call(time, key) === false) continue;

        let value = time[key];
        let timeCount = Math.floor(seconds / value);

        if (timeCount > 0) {
            if (count < digits) {
                timeString += timeCount + " " + key + " ";
                count++;
            }
            seconds -= timeCount * value;
        }
    }

    return timeString;
}

export { removePageLoader, initializeFlatpickr, promiseAjax, toastMessage, addPageLoader, reloadUserData, formatElapsedTime, secondsToTime };

