import { removePageLoader } from "/static/assets/js/ranquiz/utils.js";

class Opcion {
    constructor(nombre, letra) {
        this.nombre = nombre;
        this.letra = letra;
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

let opciones = [
    new Opcion('Colette', 'A'),
    new Opcion('Señor P.', 'B'),
    new Opcion('Mico', 'C'),
    new Opcion('Carl', 'D'),
    new Opcion('Tara', 'E'),
    new Opcion('Mortis', 'F'),
    new Opcion('Fang', 'G'),
    new Opcion('Nita', 'H'),
    new Opcion('Sprout', 'I'),
    new Opcion('Byron', 'J')
];
let enfrentamientos = [];
let cantidadIteracionesUsuario = 0;

async function main() {
    await rondaInicial();

    // Ordenar las opciones por menos descartes
    opciones.sort((a, b) => a.descartes - b.descartes);
    console.log(opciones)

    while(comprobarEmpates()) {
        await resolverEmpates();

        opciones.sort((a, b) => a.descartes - b.descartes);
        console.log(opciones)
    }

    rl.close();
}

async function rondaInicial() {
    // Agrupar las opciones en grupos de 4, para el ultimo enfrentamiento se relennara cogiendo las opciones de inicio
    const enfrentamientos = [];
    let opcionesRestantes = [...opciones];

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
    }
}

function sumarPuntos(ganador) {
    opciones.find(opcion => opcion.nombre === ganador.nombre).puntos++;
}

function sumarDescarte(perdedor) {
    opciones.find(opcion => opcion.nombre === perdedor.nombre).descartes++;
}

function comprobarEmpates() {
    // Comprobar si hay opciones empatadas
    const opcionesEmpatadas = opciones.filter(opcion => opciones.filter(op => op.descartes === opcion.descartes).length > 1);
    return opcionesEmpatadas.length > 0;
}

function insertOrUpdateObject(orden, nuevoObjeto) {
    const index = orden.findIndex(obj => obj.opc === nuevoObjeto.opc);
    if (index !== -1) {
        orden[index].peso += nuevoObjeto.peso;
    } else {
        orden.push(nuevoObjeto);
    }
}

async function desempatarPares(opcion1, opcion2) {
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
            let orden = [{opc: opcion1, peso: 0}, {opc: opcion2, peso: 0}];
            // let tempOrden = [];

            for (const contrincante of contrincantes) {
                if(opcion1.nombre === 'Mico' && opcion2.nombre === 'Sprout') {
                    // Crear punto de ruptura
                    console.log('Punto de ruptura')
                }

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

                [enfrentamientoOpcion1, enfrentamientoOpcion2].forEach((enfrentamiento, index) => {
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
                console.log('La ' + opcion1.nombre + ' ha ganado a la ' + opcion2.nombre);
                sumarDescarte(opcion2);
            }else if(pesoOpcion1.peso < pesoOpcion2.peso) {
                console.log('La ' + opcion2.nombre + ' ha ganado a la ' + opcion1.nombre);
                sumarDescarte(opcion1);
            }

            console.log(orden)
        }

        return false;
    }

    ganadorEnfrentamientosComunes.forEach(enfrentamiento => {
        sumarDescarte(enfrentamiento.ganador === opcion1 ? opcion2 : opcion1)
    });

    return true
}

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
        for(const combinacion of combinaciones) {
            await desempatarPares(combinacion[0], combinacion[1]).then((res) => {
              if(!res) {
                  combinacionesRestantes.push(combinacion);
              }
            });
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
    }
}

async function generarEnfrentamiento(opcion1, opcion2, opcion3= null, opcion4 = null) {
    // TODO: Al usuario se le presentan dos opciones, y tiene que elegir una (INTERFAZ)
    return new Promise((resolve, reject) => {
        if(opcion3 === null) {
            // rl.question(`Cuál prefieres? ${opcion1.nombre} (${opcion1.letra}) o ${opcion2.nombre} (${opcion2.letra}): `, respuesta => {
            //     const ganador = opciones.filter(opcion => opcion.letra === respuesta.toUpperCase())[0];
            //
            //     enfrentamientos.push(new Enfrentamiento(opcion1, opcion2, null, null, ganador));
            //
            //     // Buscar el perdedor para sumarle un descarte
            //     if(ganador === opcion1) {
            //         sumarDescarte(opcion2);
            //     } else {
            //         sumarDescarte(opcion1);
            //     }
            //
            //     // Sumar puntos al ganador
            //     sumarPuntos(ganador)
            //
            //     // Resolver la promesa
            //     resolve();
            // });
        } else {
        //     rl.question(`Cuál prefieres? ${opcion1.nombre} (${opcion1.letra}) o ${opcion2.nombre} (${opcion2.letra}) o ${opcion3.nombre} (${opcion3.letra}) o ${opcion4.nombre} (${opcion4.letra}): `, respuesta => {
        //         const ganador = opciones.filter(opcion => opcion.letra === respuesta.toUpperCase())[0];
        //
        //         enfrentamientos.push(new Enfrentamiento(opcion1, opcion2, opcion3, opcion4, ganador));
        //
        //         // Buscar a los perdedores para sumarle un descarte
        //         [opcion1, opcion2, opcion3, opcion4].forEach(opcion => {
        //             if(ganador !== opcion) {
        //                 sumarDescarte(opcion);
        //             }
        //         });
        //
        //         // Sumar puntos al ganador
        //         sumarPuntos(ganador)
        //
        //         // Resolver la promesa
        //         resolve();
        //     });
        }
        //
        // cantidadIteracionesUsuario++;
    });
}



function onDocumentReady() {
    main().then(() => {
        console.log('Opciones ordenadas por descartes');
        opciones.sort((a, b) => a.descartes - b.descartes);

        let i = 1;
        for(const opcion of opciones) {
            console.log(`TOP ${i} | ${opcion.nombre}: ${opcion.descartes} descartes`);
            i++;
        }

        console.log('Cantidad de iteraciones: ' + cantidadIteracionesUsuario)
    });

    removePageLoader();
}

$(document).ready(onDocumentReady);