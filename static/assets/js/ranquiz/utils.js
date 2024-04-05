
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
    return flatpickr(elementSelector, {
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

export { removePageLoader, initializeFlatpickr };