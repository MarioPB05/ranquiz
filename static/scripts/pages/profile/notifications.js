
/**
 * Función que se ejecuta cuando el documento está listo
 */
function onDocumentReady() {
    if (window.location.href.includes('show_all=True')) {
        $('#show_all').text('Ocultar notificaciones leídas');
    }

    $('#show_all').on("click",  () => {
        if (window.location.href.includes('show_all=True')) {
            window.location.href = `/user/${share_code}/?card=notifications`;  // skipcq: JS-0125
        }else {
            window.location.href = `/user/${share_code}/?card=notifications&show_all=True`;  // skipcq: JS-0125
        }
    });
}

$(document).ready(onDocumentReady);