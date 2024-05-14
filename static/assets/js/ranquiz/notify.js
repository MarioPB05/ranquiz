/*global Swal, performance*/
import { Toast, errorLog, infoLog, warningLog } from "/static/assets/js/ranquiz/utils.js";

const startTime = performance.now();

/**
 * Esta función se encarga de manejar la conexión con el servidor WebSocket
 */
function onOpen() {
    const connectionTime = performance.now() - startTime;

    infoLog(`Conectado al sistema de notificaciones (Tiempo de conexión: ${connectionTime.toFixed(2)} ms)`);
}

/**
 * Esta función se encarga de manejar el cierre de la conexión con el servidor WebSocket
 */
function onClose() {
    warningLog('Conexión cerrada con el sistema de notificaciones');
}

/**
 * Esta función se encarga de manejar los mensajes recibidos del servidor WebSocket
 * @param event
 */
function onMessage(event) {
    const message = JSON.parse(event.data);

    if (!message.icon) return;

    Toast.fire({
        html: `<div class="d-flex align-items-center">
                <i class="bi ${message.icon} fs-2x text-primary me-4"></i> 
                <span class="fw-bolder">${message.title}</span>
               </div>`
    })
}

/**
 * Esta función se encarga de manejar los errores en la conexión con el servidor WebSocket
 */
function onError() {
    errorLog('Error en la conexión del sistema de notificaciones');
}

const socket = new WebSocket('ws://127.0.0.1:8000/ws/notifications/');

socket.onopen = onOpen;
socket.onclose = onClose;
socket.onmessage = onMessage;
socket.onerror = onError;
