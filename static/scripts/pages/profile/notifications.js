
/**
 * Función que se ejecuta cuando el documento está listo
 */
function onDocumentReady() {
    if (window.location.href.includes('show_all=true')) {
        $('#show_all').text('Ocultar notificaciones leídas');
    }

    $('#show_all').on("click",  () => {
        if (window.location.href.includes('show_all=true')) {
            window.location.href = `/user/${share_code}/?card=notifications`;  // skipcq: JS-0125
        }else {
            window.location.href = `/user/${share_code}/?card=notifications&show_all=true`;  // skipcq: JS-0125
        }
    });
}

$(document).ready(onDocumentReady);