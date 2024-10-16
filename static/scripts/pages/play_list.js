import { removePageLoader, toastMessage, promiseAjax, secondsToTime } from "/static/assets/js/ranquiz/utils.js";

const twoOptions = $("#item_template_2_options");
const fourOptions = $("#item_template_4_options");
const horaInicio = new Date();
let contadorAutomatico = 0;
const intervalContador = setInterval(actualizarContador, 1000);

/**
 * Clase que representa una opción y guarda los puntos y descartes
 */
class Opcion {
    constructor(id, nombre, image=null) {
        this.id = id;
        this.nombre = nombre;
        this.image = image;
        this.puntos = 0;
        this.descartes = 0;
    }
}

class Enfrentamiento {
    /**
     * @param {Opcion} opcion1
     * @param {Opcion} opcion2
     * @param {Opcion} opcion3
     * @param {Opcion} opcion4
     * @param {Opcion} ganador
     */
    constructor(opcion1, opcion2, opcion3= null, opcion4 = null, ganador) {
        this.opcion1 = opcion1;
        this.opcion2 = opcion2;
        this.opcion3 = opcion3;
        this.opcion4 = opcion4;
        this.ganador = ganador;
    }
}

const opciones = [];
const enfrentamientos = [];

/**
 * Función principal
 * @returns {Promise<void>}
 */
async function main() {
    await rondaInicial();

    // Ordenar las opciones por menos descartes
    opciones.sort((a, b) => a.descartes - b.descartes);

    while(comprobarEmpates()) {
        await resolverEmpates();

        opciones.sort((a, b) => a.descartes - b.descartes);
    }
}

/**
 * Ronda inicial
 * @returns {Promise<void>}
 */
async function rondaInicial() {
    // Agrupar las opciones en grupos de 4, para el ultimo enfrentamiento se rellenara cogiendo las opciones de inicio
    const opcionesRestantes = [...opciones];

    while (opcionesRestantes.length > 0) {
        let opcion1 = opcionesRestantes.shift();
        let opcion2 = opcionesRestantes.shift();
        let opcion3 = opcionesRestantes.shift();
        let opcion4 = opcionesRestantes.shift();

        let i = 0;
        [opcion1, opcion2, opcion3, opcion4] = [opcion1, opcion2, opcion3, opcion4].map(opcion => {
            if(opcion === undefined) {
                opcion = opciones[i];
                i++;
            }
            return opcion;
        });

        await generarEnfrentamiento(opcion1, opcion2, opcion3, opcion4);

        actualizarTop();
        actualizarProgreso();
    }
}

/**
 * Sumar puntos al ganador
 * @param ganador
 */
function sumarPuntos(ganador) {
    opciones.find(opcion => opcion.nombre === ganador.nombre).puntos++;
}

/**
 * Sumar descarte al perdedor
 * @param perdedor
 */
function sumarDescarte(perdedor) {
    opciones.find(opcion => opcion.nombre === perdedor.nombre).descartes++;
}

/**
 * Contar las opciones empatadas
 * @returns {number}
 */
function contarEmpates() {
    // Contar las opciones que tienen el mismo número de descartes
    const opcionesEmpatadas = opciones.filter(opcion => opciones.filter(op => op.descartes === opcion.descartes).length > 1);
    return opcionesEmpatadas.length;
}

/**
 * Comprobar si hay opciones empatadas
 * @returns {boolean}
 */
function comprobarEmpates() {
    // Comprobar si hay opciones empatadas
    return contarEmpates() > 0;
}

/**
 * Insertar o actualizar un objeto en la lista
 * @param orden
 * @param nuevoObjeto
 */
function insertOrUpdateObject(orden, nuevoObjeto) {
    const index = orden.findIndex(obj => obj.opc === nuevoObjeto.opc);
    if (index !== -1) {
        orden[index].peso += nuevoObjeto.peso;
    } else {
        orden.push(nuevoObjeto);
    }
}

/**
 * Desempatar las opciones
 * @param opcion1
 * @param opcion2
 * @returns {Promise<boolean>}
 */
async function desempatarPares(opcion1, opcion2) {
    contadorAutomatico++;

    if (contadorAutomatico > 4) {
        return false;
    }

    // Buscar enfrentamientos en los que hayan participado
    const enfrentamientosComunes = enfrentamientos.filter(enfrentamiento => {
        return (enfrentamiento.opcion1 === opcion1 || enfrentamiento.opcion2 === opcion1 || enfrentamiento.opcion3 === opcion1 || enfrentamiento.opcion4 === opcion1)
            && (enfrentamiento.opcion1 === opcion2 || enfrentamiento.opcion2 === opcion2 || enfrentamiento.opcion3 === opcion2 || enfrentamiento.opcion4 === opcion2);
    });

    // Si no hay enfrentamientos comunes, se enfrentan
    if(enfrentamientosComunes.length === 0) {
        // await generarEnfrentamiento(opcion1, opcion2);
        return false;
    }

    // Mirar si el ganador de los enfrentamientos comunes es la opcion o la opcion empatada
    const ganadorEnfrentamientosComunes = enfrentamientosComunes.filter(enfrentamiento => enfrentamiento.ganador === opcion1 || enfrentamiento.ganador === opcion2);

    if(ganadorEnfrentamientosComunes.length === 0) {
        // Si no hay ganadores, se enfrentan
        // await generarEnfrentamiento(opcion1, opcion2);

        // Obtenemos los contrincantes
        const contrincantes = []; // Byron y Sprout
        for(const enfrentamiento of enfrentamientosComunes) {
            for (const opcion of [enfrentamiento.opcion1, enfrentamiento.opcion2, enfrentamiento.opcion3, enfrentamiento.opcion4]) {
                if (opcion !== opcion1 && opcion !== opcion2 && !contrincantes.includes(opcion) && opcion !== null) {
                    contrincantes.push(opcion);
                }
            }
        }

        if(contrincantes.length === 2) {
            // Orden sería una lista con esta forma: [{opc: Opcion, peso: 0}]
            const orden = [{opc: opcion1, peso: 0}, {opc: opcion2, peso: 0}];

            for (const contrincante of contrincantes) {
                // Comprobamos si opcion1 ha jugado contra ese contrincante, y si ha ganado
                const enfrentamientoOpcion1 = enfrentamientos.find(enfrentamiento =>
                    (enfrentamiento.opcion1 === opcion1 || enfrentamiento.opcion2 === opcion1 || enfrentamiento.opcion3 === opcion1 || enfrentamiento.opcion4 === opcion1) &&
                    (enfrentamiento.opcion1 === contrincante || enfrentamiento.opcion2 === contrincante || enfrentamiento.opcion3 === contrincante || enfrentamiento.opcion4 === contrincante) &&
                    (enfrentamiento.ganador === opcion1 || enfrentamiento.ganador === contrincante)
                );

                const enfrentamientoOpcion2 = enfrentamientos.find(enfrentamiento =>
                    (enfrentamiento.opcion1 === opcion2 || enfrentamiento.opcion2 === opcion2 || enfrentamiento.opcion3 === opcion2 || enfrentamiento.opcion4 === opcion2) &&
                    (enfrentamiento.opcion1 === contrincante || enfrentamiento.opcion2 === contrincante || enfrentamiento.opcion3 === contrincante || enfrentamiento.opcion4 === contrincante) &&
                    (enfrentamiento.ganador === opcion2 || enfrentamiento.ganador === contrincante)
                );

                [enfrentamientoOpcion1, enfrentamientoOpcion2].forEach((enfrentamiento) => {
                    if(enfrentamiento) {
                        if(enfrentamiento.ganador === opcion1) {
                            insertOrUpdateObject(orden, {opc: opcion1, peso: 10});
                        }else if(enfrentamiento.ganador === opcion2) {
                            insertOrUpdateObject(orden, {opc: opcion2, peso: 10});
                        }else {
                            insertOrUpdateObject(orden, {opc: contrincante, peso: 10});
                        }
                    }else {
                        // Si no ha jugado contra el contrincante, se le resta 10 puntos a la opcion de ese enfrentamiento
                        // insertOrUpdateObject(orden, {opc: (index === 0 ? opcion2 : opcion1), peso: -10});
                    }
                });
            }

            // Quitamos los duplicados de la lista
            // orden = orden.filter((item, index) => orden.indexOf(item) === index);

            // Obtener el peso de la opcion1 y la opcion2
            const pesoOpcion1 = orden.find(obj => obj.opc === opcion1);
            const pesoOpcion2 = orden.find(obj => obj.opc === opcion2);

            // Si la opcion1 tiene más peso que la opcion2 (O la opcion2 no tiene peso), se suman descartes a la opcion2
            if(pesoOpcion1.peso > pesoOpcion2.peso) {
                sumarDescarte(opcion2);
            }else if(pesoOpcion1.peso < pesoOpcion2.peso) {
                sumarDescarte(opcion1);
            }
        }

        return false;
    }

    ganadorEnfrentamientosComunes.forEach(enfrentamiento => {
        sumarDescarte(enfrentamiento.ganador === opcion1 ? opcion2 : opcion1)
    });

    return true
}

/**
 * Resolver los empates
 * @returns {Promise<void>}
 */
async function resolverEmpates() {
    for(const opcion of opciones) {
        // Coger las opciones con los mismos descartes
        const opcionesEmpatadas = opciones.filter(opc => opc.descartes === opcion.descartes);

        // Guardar en una lista todas las combinaciones posibles en pareja de las opciones empatadas
        const combinaciones = [];
        const combinacionesRestantes = [];

        for(let i = 0; i < opcionesEmpatadas.length; i++) {
            for(let j = i + 1; j < opcionesEmpatadas.length; j++) {
                combinaciones.push([opcionesEmpatadas[i], opcionesEmpatadas[j]]);
            }
        }

        // Desempatar las combinaciones
        if (contadorAutomatico < 5) {
            for(const combinacion of combinaciones) {
                await desempatarPares(combinacion[0], combinacion[1]).then((res) => {
                  if(!res) {
                      combinacionesRestantes.push(combinacion);
                  }
                });

                actualizarTop();
                actualizarProgreso();
            }
        }

        // Aplanar las combinaciones restantes y eliminar duplicados
        let combinacionesAplanadas = combinacionesRestantes.flat();
        combinacionesAplanadas = combinacionesAplanadas.filter((item, index) => combinacionesAplanadas.indexOf(item) === index);

        if(combinacionesAplanadas.length >= 4) {
            // Si hay 4 o más opciones empatadas, se enfrentan entre ellas
            await generarEnfrentamiento(combinacionesAplanadas[0], combinacionesAplanadas[1], combinacionesAplanadas[2], combinacionesAplanadas[3]);
        }else {
            // Si no, se enfrentan en parejas
            for(let i = 0; i < combinacionesAplanadas.length; i += 2) {
                if(combinacionesAplanadas[i + 1] !== undefined) {
                    await generarEnfrentamiento(combinacionesAplanadas[i], combinacionesAplanadas[i + 1]);
                }
            }
        }

        actualizarTop();
        actualizarProgreso();
    }
}

/**
 * Generar un enfrentamiento
 * @param opcion1
 * @param opcion2
 * @param opcion3
 * @param opcion4
 * @returns {Promise<unknown>}
 */
async function generarEnfrentamiento(opcion1, opcion2, opcion3= null, opcion4 = null) {
    contadorAutomatico = 0;

    return new Promise((resolve) => {
        if(opcion3 === null) {
            appendOptions([opcion1, opcion2]);

            $("#next_button").one("click", (event) => {
                $(event.currentTarget).prop("disabled", true);
                const respuesta = parseInt($(".selected_item").data("id"), 10);
                const ganador = opciones.filter(opcion => opcion.id === respuesta)[0];

                enfrentamientos.push(new Enfrentamiento(opcion1, opcion2, null, null, ganador));

                // Buscar el perdedor para sumarle un descarte
                if(ganador === opcion1) {
                    sumarDescarte(opcion2);
                } else {
                    sumarDescarte(opcion1);
                }

                // Sumar puntos al ganador
                sumarPuntos(ganador);

                resolve();
            });
        } else {
            appendOptions([opcion1, opcion2, opcion3, opcion4]);

            $("#next_button").one("click", (event) => {
                $(event.currentTarget).prop("disabled", true);

                const respuesta = parseInt($(".selected_item").data("id"), 10);
                const ganador = opciones.filter(opcion => opcion.id === respuesta)[0];

                enfrentamientos.push(new Enfrentamiento(opcion1, opcion2, opcion3, opcion4, ganador));

                // Buscar a los perdedores para sumarle un descarte
                [opcion1, opcion2, opcion3, opcion4].forEach(opcion => {
                    if(ganador !== opcion) {
                        sumarDescarte(opcion);
                    }
                });


                // Sumar puntos al ganador
                sumarPuntos(ganador)

                resolve();
            });

        }
    });
}

/**
 * Añadir las opciones al contenedor
 * @param options
 */
function appendOptions(options) {
    $("#items_container").find(".item_option:not(.d-none)").remove();
    const OptionsMode = options.length === 2 ? twoOptions : fourOptions;

    $.each(options, (index, option) => {
        const optionElement = OptionsMode.clone();
        optionElement.find('.item_name').text(option.nombre);
        optionElement.find('.item_image').attr('src', option.image);
        option.image == null ? optionElement.find('.item_image').remove() : "";
        option.image == null ? optionElement.find('.item_name').removeClass("ellipsis-two-lines") : "";
        optionElement.attr('data-id', option.id);
        optionElement.attr('id', '');
        optionElement.removeClass('d-none');
        OptionsMode.before(optionElement);
    });
}

/**
 * Actualizar el top
 */
function actualizarTop() {
    const templateTop = $("#template_top_item");
    $(".top_item").remove();

    $("#item_top_1").find(".top_item_name").text(opciones[0].nombre);
    $("#item_top_2").find(".top_item_name").text(opciones[1].nombre);
    $("#item_top_3").find(".top_item_name").text(opciones[2].nombre);

    $.each(opciones, (index, option) => {
        if (index > 2) {
            const optionElement = templateTop.clone();
            optionElement.attr('data-id', option.id);
            optionElement.attr('id', '');

            optionElement.find('.top_number').text(index + 1);
            optionElement.find('.top_item_name').text(option.nombre);
            optionElement.removeClass('d-none');
            optionElement.addClass('top_item');
            templateTop.before(optionElement);
        }
    });
}

/**
 * Actualizar el contador
 */
function actualizarContador() {
    const contador = $("#play_time");
    const horaActual = new Date();

    // Obtener los segundos transcurridos
    const segundosTranscurridos = parseInt(((horaActual - horaInicio) / 1000), 10);
    contador.text(secondsToTime(segundosTranscurridos, 2));
}

/**
 * Actualizar el progreso
 */
function actualizarProgreso() {
    // Calcular el progreso por los empates
    const progreso = $(".progress-bar");
    const progresoPorcentaje = parseInt((opciones.length - contarEmpates()) / opciones.length * 100, 10);

    progreso.text(`${progresoPorcentaje}%`);
    progreso.css("width", `${progresoPorcentaje}%`);
}

/**
 * Obtener las opciones
 * @returns {Promise<unknown>}
 */
function obtenerOpciones() {
    return new Promise((resolve) => {
        promiseAjax(`/api/list/${share_code}/item`, 'GET').then(response => { // skipcq: JS-0125
            if (response && response.items) {
                response.items.forEach(item => {
                    opciones.push(new Opcion(item.id, item.name, item.image));
                });
                actualizarTop();
                actualizarProgreso();
                removePageLoader();
                resolve();
            }
        });
    });
}

/**
 * Enviar los resultados
 */
function sendResults() {
    let opcionesFormateadas = [];

    let i = 0;

    opciones.forEach(opcion => {
        i++;
        opcionesFormateadas.push({
            id: opcion.id,
            order: i
        });
    });

    // Comvertir el array de opciones en un JSON
    opcionesFormateadas = JSON.stringify(opcionesFormateadas);

    promiseAjax(`/api/list/${share_code}/play/result/add`, 'POST', { result: opcionesFormateadas, startDate: horaInicio.getTime() }).then(response => { // skipcq: JS-0125
        if (response && response.status === "success") {
            $("#final_play_modal").modal("show");
            $("#showResultButton").attr("href", `/list/${share_code}/result/${response.result_id}`); // skipcq: JS-0125
        } else {
            toastMessage("error", "Ha ocurrido un error al enviar los resultados, por favor, inténtelo de nuevo.");
        }
    }).catch(() => {
        toastMessage("error", "Ha ocurrido un error al enviar los resultados, por favor, inténtelo de nuevo.");

        Swal.fire({ // skipcq: JS-0125
          title: "Error al enviar los resultados",
          text: "Ha ocurrido un error al enviar los resultados, por favor, inténtelo de nuevo.",
          allowOutsideClick: false,
          icon: "error",
          showDenyButton: true,
          showCancelButton: false,
          confirmButtonText: "Reintentar",
          confirmButtonClass: "btn btn-primary",
          denyButtonText: "Salir",
          denyButtonClass: "btn btn-secondary",
        }).then((result) => {
          if (result.isConfirmed) {
            sendResults();
          } else if (result.isDenied) {
              window.location.href = `/list/${share_code}/view`; // skipcq: JS-0125
          }
        });
    });
}

/**
 * Función que se ejecuta al cargar el documento
 */
function onDocumentReady() {
    $("#next_button").prop("disabled", true);

    obtenerOpciones().then(main).then(() => {
        opciones.sort((a, b) => a.descartes - b.descartes);

        actualizarTop();
        actualizarProgreso();
        sendResults();

        clearInterval(intervalContador);
    });

    // Evento para seleccionar una opción
    $("#items_container").on("click", ".item_option", (event) => {
        $(".item_option").removeClass("selected_item");
        $(event.currentTarget).addClass("selected_item");
        $("#next_button").prop("disabled", false);
    });
}

$(document).ready(onDocumentReady);