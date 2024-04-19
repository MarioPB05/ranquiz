import { removePageLoader } from "/static/assets/js/ranquiz/utils.js";
const blockcontent = new KTBlockUI($("#content")[0], { // skipcq: JS-0125
    message: '<div class="blockui-message"><span class="spinner-border text-primary"></span> Cargando...</div>',
});

const templateList = $("#template_list");

const lists = [];
const exampleList = {
    id: 1,
    name: "Lista 1",
    image: "https://images.wikidexcdn.net/mwuploads/wikidex/thumb/a/a7/latest/20220715200149/EP1206_Dragonite_de_Iris.png/640px-EP1206_Dragonite_de_Iris.png",
    url: "http://127.0.0.1:8000/list/LSdYgfiXomAobVAXHnnk",
    liked: true,
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
 * Función que obtiene las listas de la base de datos
 * @param search
 * @param page
 * @param reset
 * @param sort (default, popular, newest)
 */
function getLists(search, page, reset = false, sort = "default") {
    // Verificar si se debe resetear la lista
    if (reset) lists.length = 0;

    // Bloquear contenido
    blockcontent.block();

    // TODO: Obtener listas de base de datos

    // Desbloquear contenido
    blockcontent.release();

    lists.push(exampleList);

    // Añadir listas a la página
    $.each(lists, (index, list) => {
        addList(list);
    });
}

/**
 * Función que se ejecuta cuando el documento está listo
 */
function onDocumentReady() {
    $("nav button").on("click", (event) => {
        if ($(event.target).hasClass("nav_selected")) return;
        const selected = $(event.target).attr("id").split("_")[0];
        toggleNavs(selected);

        $("#content").empty();
        if (selected === "list") {
            getLists("", 1, true, getSort());
        }
    });

    getLists("", 1);
    removePageLoader();
}

$(document).ready(onDocumentReady);