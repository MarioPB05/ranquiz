import {errorLog, infoLog, warningLog} from "/static/assets/js/ranquiz/utils.js";

function onOpen() {
    const connectionTime = performance.now() - startTime;

    infoLog(`Conectado al sistema de notificaciones (Tiempo de conexión: ${connectionTime.toFixed(2)} ms)`);
}

function onClose() {
    warningLog('Conexión cerrada con el sistema de notificaciones');
}

function onMessage(event) {
    const message = JSON.parse(event.data);
    console.log('Mensaje recibido del servidor WebSocket:', message); // skipcq: JS-0002
}

function onError() {
    errorLog('Error en la conexión del sistema de notificaciones');
}


const startTime = performance.now();

const socket = new WebSocket('ws://127.0.0.1:8000/ws/notifications/');

socket.onopen = onOpen;
socket.onclose = onClose;
socket.onmessage = onMessage;
socket.onerror = onError;
