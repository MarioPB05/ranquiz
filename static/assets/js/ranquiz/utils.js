
/**
 * Esta función se encarga de remover el loader de la página
 */
function removePageLoader() {
    $('body').css("overflow-y", "auto");
    $('#loading_indicator').removeClass("d-flex");
}

export { removePageLoader };