import {promiseAjax, toastMessage} from "/static/assets/js/ranquiz/utils.js";

/**
 * Función que limpia las notificaciones
 */
function clear_notifications() {
    promiseAjax('/api/notification/clear', 'GET').then(response => {
        if (response.status === 'success') {
            toastMessage('success', 'Notificaciones limpiadas');

            setTimeout(() => {
                window.location.reload();
            }, 1000);
        }
    });
}

/**
 * Función que se ejecuta cuando el documento está listo
 */
function onDocumentReady() {
    $('#clear_notifications').on("click",  () => {
        Swal.fire({ // skipcq: JS-0125
            title: "¿Estás seguro?",
            icon: "warning",
            showCancelButton: true,
            confirmButtonClass: "btn btn-primary",
            confirmButtonText: "Limpiar",
            closeOnConfirm: false,
            cancelButtonClass: "btn btn-secondary",
            cancelButtonText: "Cancelar"
        }).then((result) => {
            if (result.isConfirmed) {
                clear_notifications();
            }
        });
    });
}


$(document).ready(onDocumentReady);