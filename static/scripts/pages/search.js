import {promiseAjax, removePageLoader, toastMessage} from "/static/assets/js/ranquiz/utils.js";

const elementsPerPage = 30;
let previousSearch = "";

const search = $("#search");
const templateList = $("#template_list");
const templateCategory = $("#template_category");
const templateUser = $("#template_user");
const content = $("#content");
const loadMore = $("#load_more");
const allNavs = $("nav button");

const blockcontent = new KTBlockUI(content[0], { // skipcq: JS-0125
    message: '<div class="blockui-message"><span class="spinner-border text-primary"></span> Cargando...</div>',
});

let elements = [];


/**
 * Función que cambia la vista de los elementos de la página
 * @param selected puede ser "list", "category" o "user"
 */
function toggleNavs(selected) {
    const selectedNav = $(`#${selected}_nav`);

    // Bloquear todos los botones
    allNavs.attr("disabled", true);

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
 * Función que cambia el ordenamiento seleccionado
 * @param selected (newest, popular)
 */
function toggleSort(selected) {
    const allSorts = $("#sort_container button");
    const selectedSort = $(`#${selected}`);

    if (selectedSort.hasClass("btn-primary")) {
        selectedSort.removeClass("btn-primary");
        selectedSort.addClass("btn-outline-primary");
        selectedSort.blur();
    }else {
        allSorts.removeClass("btn-primary").addClass("btn-outline-primary");
        selectedSort.addClass("btn-primary");
        selectedSort.removeClass("btn-outline-primary");
    }
}

/**
 * Función que obtiene el tipo de ordenamiento seleccionado
 * @returns string (default, popular, newest)
 */
function getSort() {
    if ($("#newest").hasClass("btn-primary")) return "newest";
    if ($("#popular").hasClass("btn-primary")) return "popular";

    return "default"
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
    !list.image ? newList.find(".list_image").attr("src", "/static/assets/media/placeholders/list_mix2.png") : "";
    newList.attr("href", list.url);

    newList.find(".author_name").text(list.author.username);
    newList.find(".list_author_group").attr("href", list.author.url);
    newList.find(".author_image").attr("src", list.author.avatar);

    newList.find(".list_plays_number").text(list.plays);
    !list.highlighted ? newList.find(".highlight_list").addClass("d-none") : '';
    list.liked ? newList.find(".list_like").addClass("bi-heart-fill").removeClass("bi-heart") : "";
    list.liked ? newList.find(".list_like").addClass("text-danger") : "";

    content.append(newList);
}

/**
 * Función que añade una categoría a la página
 * @param category
 */
function addCategory(category) {
    const newCategory = templateCategory.clone();
    newCategory.removeAttr("id");
    newCategory.removeClass("d-none");

    newCategory.attr("data-id", category.id);
    newCategory.find(".category_name").text(category.name);
    newCategory.find(".category_list_number").text(category.lists);
    newCategory.attr("href", category.url);

    if (category.followed) {
        newCategory.find(".category_follow").addClass("btn-primary");
        newCategory.find(".category_follow").removeClass("btn-outline-primary");
        newCategory.find(".category_follow").text("Siguiendo");
    }

    newCategory.find(".category_follower_number").text(category.followers);

    content.append(newCategory);
}

/**
 * Función que añade un usuario a la página
 * @param user
 */
function addUser(user) {
    const newUser = templateUser.clone();
    newUser.removeAttr("id");
    newUser.removeClass("d-none");

    newUser.attr("data-id", user.id);
    newUser.find(".user_name").text(user.username);
    newUser.attr("href", user.url);
    newUser.find(".user_list_number").text(user.lists);
    newUser.find(".user_follower_number").text(user.followers);
    newUser.find(".user_avatar").attr("src", user.avatar);

    if (user.followed) {
        newUser.find(".user_follow_icon").addClass("bi-person-check-fill")
        newUser.find(".user_follow_icon").removeClass("bi-person-plus-fill");
        newUser.find(".user_follow_icon").addClass("text-primary").removeClass("text-secondary");
    }

    content.append(newUser);
}

/**
 * Función que obtiene los elementos de la página
 * @param type (list, category, user)
 * @param search
 * @param page
 * @param reset boolean
 * @param sort (default, popular, newest)
 * @returns no-return
 */
async function getElements(type, search, page, reset = false, sort = "default") {
    // Verificar si se debe resetear la lista y limpiamos el contenido
    if (reset) {
        emptyContent();
        content.attr("data-page", 1);
        notFoundResults(false);
        elements.length = 0;
    }

    // Bloquear contenido
    blockcontent.block();

    // Esconder botón de cargar más
    loadMore.removeClass("d-flex").addClass("d-none");

    // Obtener elementos
    if (type === "list") {
        elements = await getLists(search, page, sort);
        changeGridColumnsOfParent("350px");
    }else if (type === "category") {
        elements = await getCategories(search, page, sort);
        changeGridColumnsOfParent("250px");
    } else if (type === "user") {
        elements = await getUsers(search, page, sort);
        changeGridColumnsOfParent("200px");
    }else {
        toastMessage("Error", "No se ha seleccionado un modo de búsqueda");
        notFoundResults();
        allNavs.attr("disabled", false);
        return;
    }

    // Desbloquear botones del nav
    allNavs.attr("disabled", false);

    // Desbloquear contenido
    blockcontent.release();

    // Verificar si se encontraron resultados
    if (elements.length === 0 && page === 1) {
        notFoundResults();
        return;
    }

    // Verificar si se deben mostrar más elementos
    if (elements.length === elementsPerPage) {
        loadMore.removeClass("d-none").addClass("d-flex");
    }

    // Añadir listas a la página
    $.each(elements, (index, element) => {
        if (type === "list") {
            addList(element);
        }else if (type === "category") {
           addCategory(element);
        } else if (type === "user") {
            addUser(element);
        }
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
    return new Promise((resolve) => {
        promiseAjax(`/api/list/filter?page=${page}&search=${search}&sort=${sort}`, "GET").then((response) => {
            resolve(response.lists);
        }).catch(() => {
            toastMessage("error", "No se pudieron obtener las listas");
            allNavs.attr("disabled", false);
        });
    });
}

/**
 * Función que obtiene las categorías de la base de datos
 * @param search
 * @param page
 * @param sort
 * @returns {Promise<unknown>}
 */
async function getCategories(search, page, sort = "default") {
    return new Promise((resolve) => {
        promiseAjax(`/api/category/filter?page=${page}&search=${search}&sort=${sort}`, "GET").then((response) => {
            resolve(response.categories);
        }).catch(() => {
            toastMessage("error", "No se pudieron obtener las categorías");
            allNavs.attr("disabled", false);
        });
    });
}

/**
 * Función que obtiene los usuarios de la base de datos
 * @param search
 * @param page
 * @param sort
 * @returns {Promise<unknown>}
 */
async function getUsers(search, page, sort = "default") {
    return new Promise((resolve) => {
        promiseAjax(`/api/user/filter?page=${page}&search=${search}&sort=${sort}`, "GET").then((response) => {
            resolve(response.users);
        }).catch(() => {
            toastMessage("error", "No se pudieron obtener los usuarios");
            allNavs.attr("disabled", false);
        });
    });
}

/**
 * Función que se activa o desactiva el mensaje de no se encontraron resultados
 * @param active true para activar, false para desactivar
 */
function notFoundResults(active = true) {
    if (active) {
        loadMore.removeClass("d-flex").addClass("d-none");
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
    content.css("grid-template-columns", `repeat(auto-fill, minmax(${minWidth}, 1fr)`);
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
    allNavs.on("click", (event) => {
        // Si el botón ya está seleccionado, no hacer nada
        if ($(event.target).hasClass("nav_selected")) return;

        // Obtenemos el modo seleccionado y cambiamos la vista
        const selected = $(event.target).attr("id").split("_")[0];
        toggleNavs(selected);

        // Obtenemos los elementos
        getElements(selected, search.val(), 1, true, getSort());
    });

    // Evento de carga de más elementos
    $("#load_more button").on("click", () => {
        // Obtenemos la página actual y la incrementamos
        const page = parseInt(content.attr("data-page")) + 1;
        content.attr("data-page", page);

        // Obtenemos los elementos
        getElements(getSelectedNav(), search.val(), page, false, getSort());
    });

    // Evento de cambio de ordenamiento
    $("#sort_container button").on("click", (event) => {
        // Cambiamos el ordenamiento seleccionado
        toggleSort($(event.target).attr("id"));

        // Obtenemos los elementos
        getElements(getSelectedNav(), search.val(), 1, true, getSort());
    });

    // Evento de clic en un elemento
    content.on("click", ".list, .category, .user", (event) => {
       if (event.target.tagName === "A") return;

        const url = $(event.currentTarget).attr("href");
        if (url) window.location.href = url;
    });

    // Evento de búsqueda al pulsar enter
    search.on("keypress", (event) => {
        if (event.key === "Enter" && search.val() !== previousSearch) {
            previousSearch = search.val();
            getElements(getSelectedNav(), search.val(), 1, true, getSort());
        }
    });

    // Evento de búsqueda al hacer clic en el botón
    $("#search_button").on("click", () => {
        if (search.val() === previousSearch) return;

        previousSearch = search.val();
        getElements(getSelectedNav(), search.val(), 1, true, getSort());
    });

    getElements(getSelectedNav(), "", 1);
    removePageLoader();
}

$(document).ready(onDocumentReady);