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
    return flatpickr(elementSelector, {
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

export {removePageLoader, initializeFlatpickr};