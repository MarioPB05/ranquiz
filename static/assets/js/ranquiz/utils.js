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

/**
 * Esta función se encarga de dar formato a la fecha y hora de creación de una publicación
 * @param dateTime
 * @returns {string}
 */
function formatElapsedTime(dateTime) {
    const currentDate = new Date();
    const elapsedTime = currentDate - dateTime;
    const elapsedSeconds = Math.floor(elapsedTime / 1000);

    if (elapsedSeconds < 60) {
        return `Hace ${elapsedSeconds} s`;
    }

    const elapsedMinutes = Math.floor(elapsedSeconds / 60);
    if (elapsedMinutes < 60) {
        return `Hace ${elapsedMinutes} min`;
    }

    const elapsedHours = Math.floor(elapsedMinutes / 60);
    if (elapsedHours < 24) {
        return `Hace ${elapsedHours} h`;
    }

    const elapsedDays = Math.floor(elapsedHours / 24);
    if (elapsedDays < 30) {
        return `Hace ${elapsedDays} d`;
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
 * Esta función se encarga de mostrar un mensaje de tipo info en la consola
 * @param message
 */
function infoLog(message) {
    console.log(  // skipcq: JS-0002
        '%c INFO ',
        'background-color: #BD20E9;color: white;font-weight: bold;border-radius:2px;padding: 2px 6px;',
        message
    );
}

/**
 * Esta función se encarga de mostrar un mensaje de tipo warning en la consola
 * @param message
 */
function warningLog(message) {
    console.log( // skipcq: JS-0002
        '%c WARNING ',
        'background-color: #f1bc00;color: white;font-weight: bold;border-radius:2px;padding: 2px 6px;',
        message
    );
}

/**
 * Esta función se encarga de mostrar un mensaje de tipo error en la consola
 * @param message
 */
function errorLog(message) {
    console.log( // skipcq: JS-0002
        '%c ERROR ',
        'background-color: #d9214e;color: white;font-weight: bold;border-radius:2px;padding: 2px 6px;',
        message
    );
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
    const time = {
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

    for (const key in time) {
        if (Object.prototype.hasOwnProperty.call(time, key) === false) continue;

        const value = time[key];
        const timeCount = Math.floor(seconds / value);

        if (timeCount > 0) {
            if (count < digits) {
                timeString += `${timeCount} ${key} `;
                count++;
            }
            seconds -= timeCount * value;
        }
    }

    return timeString;
}

// Función para cambiar los estilos del botón y llamar al backend
function toggleListLike(event) {
    event.stopPropagation()

    // Obtener el botón y el estado actual
    const button = $(event.currentTarget);
    const icon = button.find('i');
    const isLiked = button.find('i').hasClass('text-danger');

    if (isLiked) {
        icon.removeClass("bi-heart-fill text-danger").addClass("bi-heart");
    } else {
        icon.removeClass("bi-heart").addClass("bi-heart-fill text-danger");
    }

    // Llamar al backend
    const shareCode = button.parent().attr('data-share_code');
    promiseAjax(`/api/list/${shareCode}/like?isLiked=${!isLiked}`, "GET").then(response => {
        if (response.status === "success") {
        } else if (response.status === "error") {
            toastMessage("error", response.message);
            if (!isLiked) {
                icon.removeClass("bi-heart-fill text-danger").addClass("bi-heart");
            } else {
                icon.removeClass("bi-heart").addClass("bi-heart-fill text-danger");
            }
        }

    }).catch(() => {
        toastMessage("error", "Error al dar like");
        if (!isLiked) {
            icon.removeClass("bi-heart-fill text-danger").addClass("bi-heart");
        } else {
            icon.removeClass("bi-heart").addClass("bi-heart-fill text-danger");
        }
    })
}

function toggleUserFollow(event) {
    event.stopPropagation()

    // Obtener el botón y el estado actual
    const button = $(event.currentTarget);
    const isFollowed = button.attr('data-is_followed') === 'true';

    // Llamar al backend
    const shareCode = button.parent().attr('data-share_code');

    return new Promise((resolve, reject) => {
        promiseAjax(`/api/user/${shareCode}/follow?isFollowed=${!isFollowed}`, "GET").then(response => {
            if (response.status === "success") {
                button.attr('data-is_followed', !isFollowed);
                resolve(isFollowed);
            } else if (response.status === "error") {
                toastMessage("error", response.message);
            }
        }).catch(() => {
            toastMessage("error", "Error al seguir usuario");
            reject();
        });
    });
}

export {
    removePageLoader,
    initializeFlatpickr,
    promiseAjax,
    toastMessage,
    addPageLoader,
    reloadUserData,
    formatElapsedTime,
    secondsToTime,
    infoLog,
    warningLog,
    errorLog,
    toggleListLike,
    toggleUserFollow
};
