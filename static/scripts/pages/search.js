import {removePageLoader, toastMessage} from "/static/assets/js/ranquiz/utils.js";
const blockcontent = new KTBlockUI($("#content")[0], { // skipcq: JS-0125
    message: '<div class="blockui-message"><span class="spinner-border text-primary"></span> Cargando...</div>',
});
const elementsPerPage = 30;

const search = $("#search");
const templateList = $("#template_list");

let elements = [];
const exampleList = {
    id: 1,
    name: "Lista 1",
    image: "https://images.wikidexcdn.net/mwuploads/wikidex/thumb/a/a7/latest/20220715200149/EP1206_Dragonite_de_Iris.png/640px-EP1206_Dragonite_de_Iris.png",
    url: "http://127.0.0.1:8000/list/LSdYgfiXomAobVAXHnnk",
    liked: false,
    plays: 23,
    highlighted: true,
    author: {
        username: "user1",
        avatar: "http://res.cloudinary.com/dhewpzvg9/image/upload/c_fill/v1712514744/avatars/kidcithbb1ogolsssdma.png",
        url: "http://127.0.0.1:8000/user/"
    }
};

/**
 * Función que cambia la vista de los elementos de la página
 * @param selected puede ser "list", "category" o "user"
 */
function toggleNavs(selected) {
    const allNavs = $("nav button");
    const selectedNav = $(`#${selected}_nav`);

    // Remover clases de nav seleccionado a todos los botones
    allNavs.removeClass("nav_selected");
    allNavs.removeClass("text-white");
    allNavs.removeClass("btn-primary");
    allNavs.hasClass("btn-outline-primary") ? allNavs.addClass("btn-outline-primary") : "";
    allNavs.hasClass("text-secondary-dark") ? allNavs.addClass("text-secondary-dark") : "";

    // Añadir clases al nav seleccionado
    selectedNav.addClass("nav_selected");
    selectedNav.addClass("text-white");
    selectedNav.addClass("btn-primary");
    selectedNav.removeClass("btn-outline-primary");
    selectedNav.removeClass("text-secondary-dark");
}

/**
 * Función que obtiene el tipo de ordenamiento seleccionado
 * @returns string (default, popular, newest)
 */
function getSort() {
    if(!$("#sort_container button").hasClass("btn-primary")) return "default";

    if ($("#newest").hasClass("btn-primary")) return "newest";
    if ($("#popular").hasClass("btn-primary")) return "popular";
}

/**
 * Función que añade una lista a la página
 * @param list
 */
function addList(list) {
    const newList = templateList.clone();
    newList.removeAttr("id");
    newList.removeClass("d-none");

    newList.attr("data-id", list.id);
    newList.find(".list_name").text(list.name);
    newList.find(".list_image").attr("src", list.image);
    newList.attr("href", list.url);

    newList.find(".author_name").text(list.author.username);
    newList.find(".list_author_group").attr("href", list.author.url);
    newList.find(".author_image").attr("src", list.author.avatar);

    newList.find(".list_plays_number").text(list.plays);
    list.highlighted ? newList.find(".highlight_list").removeClass("d-none") : "";
    list.liked ? newList.find(".list_like").addClass("bi-heart-fill").removeClass("bi-heart") : "";
    list.liked ? newList.find(".list_like").addClass("text-danger") : "";

    $("#content").append(newList);
}

/**
 * Función que obtiene los elementos de la página
 * @param type (list, category, user)
 * @param search
 * @param page
 * @param reset
 * @param sort (default, popular, newest)
 */
async function getElements(type, search, page, reset = false, sort = "default") {
    console.log(`Buscando ${type} con: ${search}, en la página ${page}, ordenadas por ${sort}`);

    // Verificar si se debe resetear la lista
    if (reset) elements.length = 0;

    // Bloquear contenido
    blockcontent.block();

    if (type === "list") {
        elements = await getLists("", 1, getSort());
        changeGridColumnsOfParent("350px");
    }else if (type === "category") {
        notFoundResults();
    } else if (type === "user") {
        notFoundResults();
    }else {
        toastMessage("Error", "No se ha seleccionado un modo de búsqueda", "error");
        notFoundResults();
    }

    // Desbloquear contenido
    blockcontent.release();

    // Verificar si se encontraron resultados
    if (elements.length === 0) {
        notFoundResults();
        return;
    }

    // Verificar si se deben mostrar más elementos
    if (elements.length === elementsPerPage) {
        $("#load_more").removeClass("d-none").addClass("d-flex");
    }

    // Añadir listas a la página
    $.each(elements, (index, element) => {
        addList(element);
    });
}

/**
 * Función que obtiene las listas de la base de datos
 * @param search
 * @param page
 * @param sort
 * @returns {Promise<list>}
 */
async function getLists(search, page, sort = "default") {
    return new Promise((resolve, reject) => {
        // TODO: Obtener {elementsPerPage} listas de base de datos a partir de la página {page}
        resolve([exampleList]);
    });
}

/**
 * Función que se activa o desactiva el mensaje de no se encontraron resultados
 * @param active true para activar, false para desactivar
 */
function notFoundResults(active = true) {
    if (active) {
        $("#load_more").removeClass("d-flex").addClass("d-none");
        changeGridColumnsOfParent("100%");
        $("#notFoundResults").removeClass("d-none").addClass("d-flex");
    }else if ($("#notFoundResults").hasClass("d-flex")) {
        $("#notFoundResults").removeClass("d-flex").addClass("d-none");
    }
}

/**
 * Función que obtiene el modo de búsqueda seleccionado
 * @returns {*}
 */
function getSelectedNav() {
    return $("nav button.nav_selected").attr("id").split("_")[0];
}

/**
 * Función que cambia el tamaño de las columnas de la vista principal
 * @param minWidth
 */
function changeGridColumnsOfParent(minWidth) {
    $("#content").css("grid-template-columns", `repeat(auto-fill, minmax(${minWidth}, 1fr)`);
}

/**
 * Función que limpia los elementos de la página
 */
function emptyContent() {
    $("#content>*").filter(function() {
        return !this.id.startsWith("template");
    }).not("#notFoundResults").remove()
}

/**
 * Función que se ejecuta cuando el documento está listo
 */
function onDocumentReady() {

    // Evento para cambiar lo que el usuario está buscando
    $("nav button").on("click", (event) => {
        // Si el botón ya está seleccionado, no hacer nada
        if ($(event.target).hasClass("nav_selected")) return;

        // Obtenemos el modo seleccionado y cambiamos la vista
        const selected = $(event.target).attr("id").split("_")[0];
        toggleNavs(selected);

        // Limpiamos el contenido y obtenemos los elementos
        emptyContent();
        $("#content").attr("data-page", 1);
        notFoundResults(false);

        getElements(selected, search.val(), 1, true, getSort());
    });

    $("#load_more button").on("click", () => {
        const page = parseInt($("#content").attr("data-page")) + 1;
        const selected = getSelectedNav();

        $("#content").attr("data-page", page);

        if (selected === "list") {
            getElements(selected, search.val(), page, false, getSort());
        }else if (selected === "category") {
            notFoundResults();
        } else if (selected === "user") {
            notFoundResults();
        }
    });

    getElements(getSelectedNav(), "", 1);
    removePageLoader();
}

$(document).ready(onDocumentReady);