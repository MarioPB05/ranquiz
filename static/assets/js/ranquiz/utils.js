
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
 * @returns {*|[]}
 */
function initializeFlatpickr(elementSelector) {
    return flatpickr(elementSelector, {  // skipcq: JS-0125
      minDate: '1920-01-01',
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