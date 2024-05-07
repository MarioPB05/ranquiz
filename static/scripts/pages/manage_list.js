import {removePageLoader, initializeFlatpickr, promiseAjax, toastMessage, addPageLoader} from "/static/assets/js/ranquiz/utils.js";

const minItems = 5;
let items_prefix = [];
let item_last_prefix = 0;
const categories = [];
const maxCategories = 5;
const maxCategoryLength = 25;
let allCategories = [];
const flatpickrInstance = initializeFlatpickr("#range_date_highlight", 'range', moment().format('YYYY-MM-DD')); // skipcq: JS-0125

/**
 * Cambiar la imagen de la lista
 */
function changedListImage() {
    $('label[for="id_image"]').hide();
}

/**
 * Eliminar el label para subir la imagen de la lista
 */
function removeListImage() {
    $('label[for="id_image"]').show();
}

/**
 * Actualizar el precio del destacado en base a las fechas seleccionadas
 */
function updateHighlightPrice() {
    const dates = $("#range_date_highlight").val().split(" hasta ");

    if (dates.length === 2) {
        promiseAjax(`/api/shop/highlight/calculator?start_date=${dates[0]}&end_date=${dates[1]}`)
            .then(response => {
                $('#highlight_price').text(response.price);
            })
            .catch(() => {
                toastMessage('error', 'Ha ocurrido un error al calcular el precio del destacado')
            });
    }
}

/**
 * Cancelar el destacado
 */
function cancelHighlight() {
    flatpickrInstance.clear();
    $('#highlight_price').text('0');
}

/**
 * Crear un item
 */
function createItem() {
    // Verificar que no haya ningun item vacio
    if (anyItemInputEmpty() && items_prefix.length > minItems - 1) {
        focusOnFirstEmptyItem();
        toastMessage('error', 'Hay elementos vacíos, rellénelos todos antes de añadir uno nuevo.');
        return;
    }

    // Clonar la plantilla de un item
    const item = $('#item_template').clone();

    // Remover el ID de la plantilla
    item.removeAttr('id');

    // Vaciar los inputs
    item.find('input[type="text"]').val('');

    // Obtener el prefijo del item
    const prefix = `${item_last_prefix + 1}-`;

    // Actualizar los datos del prefijo
    item_last_prefix++;
    items_prefix.push(item_last_prefix);

    // Guardar el prefijo en el item
    item.attr('data-prefix', item_last_prefix);

    // Cambiar el ID y name del input de la imagen
    const imageInput = item.find('#id_template-image');
    imageInput.attr('id', `id_${prefix}image`);
    imageInput.attr('name', `${prefix}image`);

    // Actualizar el atributo for del label
    item.find('label[for="id_template-image"]').attr('for', `id_${prefix}image`);

    // Cambiar el ID y name del input del nombre
    const nameInput = item.find('#id_template-name');
    nameInput.attr('id', `id_${prefix}name`);
    nameInput.attr('name', `${prefix}name`);

    // Actualizar el atributo for del label
    item.find('label[for="id_template-name"]').attr('for', `id_${prefix}name`);

    // Mostrar el item
    item.removeClass('d-none').addClass('d-flex');

    // Añadir el item al contenedor
    $('#items_container').append(item);

    // Actualizar el número de items
    actualizeItemNumber();

    // Enfocar en el input del nombre
    focusOnFirstEmptyItem();
}

/**
 * Eliminar un item
 * @param event
 */
function removeItem(event) {
    // Comprobar que haya más de 5 items
    if (items_prefix.length <= minItems) {
        toastMessage('error', `El minimo de elementos es ${minItems}.`);
        return;
    }

    // Obtener el padre del botón
    const parent = $(event.target).parent().parent();

    // Obtener el prefijo del item
    const prefix = parent.attr('data-prefix');

    // Eliminar el prefijo de la lista
    items_prefix = items_prefix.filter(item => item !== parseInt(prefix));

    // Eliminar el item
    parent.remove();

    // Actualizar el número de items
    actualizeItemNumber();
}

/**
 * Mostrar el modal de vista previa de la imagen
 * @param target
 */
function showItemPreviewModal(target) {
    // Obtenemos el padre
    const parent = $(target).parent();

    // Obtenemos el nombre del item
    const name = parent.find('.item-name').val();

    // Si el nombre no está vacío
    if (name) {
        // Mostrar el nombre en el modal
        $('#temp_item_name').text(name).show();
    }

    // Configurar el target para posterior uso
    $('#change_item_img').parent().attr('data-target', `#${target.id}`);

    // Mostrar el modal
    $('#image_previewer').modal('show');
}

/**
 * Cambiar la imagen del item
 * @param event
 */
function itemImageChanged(event) {
    // Obtener el archivo seleccionado
    const file = $(event.target).prop('files')[0];

    // Verificar si se seleccionó un archivo
    if (file) {
        // Crear un objeto FileReader para leer el archivo
        const reader = new FileReader();

        // Cuando se termine de cargar el archivo
        reader.onload = function () {
            // Mostrar la imagen en el elemento img
            $('#temp_image_preview').attr('src', reader.result);
        }

        // Leer el archivo como una URL de datos
        reader.readAsDataURL(file);
    }

    showItemPreviewModal(event.target);
}

/**
 * Obtener el target del input del modal
 * @param event
 * @returns {jQuery|HTMLElement|*}
 */
function getModalInputTarget(event) {
    return $($(event.target).parent().attr('data-target'));
}

/**
 * Cambiar la imagen del item
 * @param event
 */
function changeItemImage(event) {
    // Obtener el target (Input)
    /*const target = $(event.target).attr('data-target');
    const input = $(target);*/
    const input = getModalInputTarget(event);

    // Limpiar el input
    input.val('');

    // Fingir que se pulsó el botón de selección de archivo
    input.trigger('click');

    // Quitar el foco del input
    $(event.target).blur();
}

/**
 * Establecer la imagen del item
 * @param event
 */
function setItemImage(event) {
    // Obtener el target (Input)
    const input = getModalInputTarget(event);

    // Cambiar la clase para indicarle al usuario que la imagen se ha seleccionado
    input.parent().find('label>i')
        .removeClass('text-primary-800').addClass('text-white');
}

/**
 * Cancelar la selección de la imagen del item
 * @param event
 */
function cancelItemImage(event) {
    // Obtener el target (Input)
    const input = getModalInputTarget(event);

    // Cambiar la clase para indicarle al usuario que la imagen no se ha seleccionado
    input.parent().find('label>i')
        .removeClass('text-white').addClass('text-primary-800');

    // Limpiar el input
    input.val('');
}

/**
 * Comprobar si el item tiene una imagen
 * @param event
 */
function itemHasImage(event) {
    // Obtener el target (Input)
    const input = $(`#${$(this).attr('for')}`);

    // Comprobar si ya se ha seleccionado una imagen para mostrar el modal directamente
    if (input[0] && input.prop('files').length > 0) {
        event.preventDefault();

        itemImageChanged({target: input});

        showItemPreviewModal(input[0]);
    }
}

/**
 * Recibe un elemento y le añade un border rojo durante un segundo
 */
function temporalRedBorder(element) {
    element.addClass('border border-danger');
    setTimeout(() => element.removeClass('border border-danger'), 1000);
}

/**
 * Comprobar si hay algún input de item vacío
 * @returns {boolean}
 */
function anyItemInputEmpty() {
    // Comprueba si hay algún input de item vacío
    let empty = false;

    $('#items_container').find('.list_item:not(#item_template) .item-name').each((index, element) => {
        if (!$(element).val() && $(element).val() !== '0') {
            empty = true;
        }
        return !empty;
    });

    return empty;
}

/**
 * Enfocar en el primer item con mas de 50 caracteres
 */
function focusOnFirstTooLongInput() {
    let found = false;

    // Enfoca en el primer item con más de 50 caracteres
    $('#items_container').find('.list_item:not(#item_template)').find('.item-name').each(function () {

        if ($(this).val().length > 50) {
            $(this).focus();
            found = true;
            temporalRedBorder($(this));
        }

        return !found;
    });

}

/**
 * Al crear o editar una lista, el nombre de todos sus ítems no superen los 50 caracteres.
 */
function AnyInputTooLong() {
    // Comprueba si hay algún input con mas de 50 caracteres
    let invalid = false;

    $('#items_container').find('.list_item:not(#item_template) .item-name').each((index, element) => {
        if ($(element).val().length > 50) {
            invalid = true;
        }
        return !invalid;

    });

    return invalid;
}



/**
 * Enfocar en el primer item vacio
 */
function focusOnFirstEmptyItem() {
    let found = false;

    // Enfoca en el primer item vacío
    $('#items_container .list_item:not(#item_template)').find('input[type="text"]').each(function () {

        if ($(this).val() === '') {
            $(this).focus();
            found = true;
            temporalRedBorder($(this));
        }

        return !found;
    });
}

/**
 * Actualizar el número de items
 */
function actualizeItemNumber() {
    // Actualiza el número de items
    let i = 0;

    $('#items_container').find('.list_item:not(#item_template)').each(() => i++);

    $("#item_number").text(i);
}

/**
 * Añadir una categoría
 * @param name
 * @param skipValidation
 * @returns {Promise<void>}
 */
async function addCategory(name, skipValidation = false) {

    if (!skipValidation) {
        // Verificar que la categoría sea válida
        if (!validateCategory(name)) {
            return;
        }

        // Verificar si la categoría no existe y si es similar a alguna
        if (allCategories.indexOf(name) === -1) {
            if (await acceptSimilarCategory(name)) {
                return;
            }else {
                uploadCategory(name);
            }
        }
    }

    // Añadir la categoría a la lista
    categories.push(name);
    $('#add_category').val('');

    // Añadir la categoría al contenedor
    const category = $('#category_template').clone();

    category.removeAttr('id');
    category.removeClass('d-none').addClass('d-flex');

    category.html(category.html().replace('{NAME}', name));

    $('#categories_container').append(category);
}

function validateCategory(name) {
    // Verificar que no esté vacío, si existe, que no haya más de 5 categorías y que no sea mayor a 50 caracteres
    if (!name) {
        toastMessage('error', 'El campo de categoría no puede estar vacío');
        return false;

    } else if (categories.includes(name)) {
        toastMessage('error', 'La categoría ya está añadida');
        return false;

    } else if (categories.length >= maxCategories) {
        toastMessage('error', `El máximo de categorías es ${maxCategories}`);
        return false;

    } else if (name.length >= maxCategoryLength) {
        toastMessage('error', `El nombre de la categoría no puede ser mayor a ${maxCategoryLength} caracteres`);
        return false;

    } else {
        return true;
    }

}

function removeCategory(event) {
    // Eliminar el item
    $(this).remove();

    // Eliminar la categoría de la lista
    categories.splice(categories.indexOf(event.target.text), 1);
}

/**
 * Obtener las categorías del servidor y añadirlas al select
 */
function getCategories() {
    promiseAjax('/api/category/').then(response => {
        allCategories = response.categories.map((category) => {
            return category.name;
        });

        $("#actual_categories").html('');
        allCategories.forEach(category => {
            $("#actual_categories").append(`<option value="${category}">`);
        });
    });
}

/**
 * Aceptar una categoría similar
 * @param name
 * @returns {Promise<*|boolean>}
 */
async function acceptSimilarCategory(name) {
    try {
        const response = await promiseAjax(`/api/category/validate/${name}`);

        if (!response.validate) {
            const result = await Swal.fire({ // skipcq: JS-0125
                title: `¿Quieres decir ${response.similar_category.name} ?`,
                showCancelButton: true,
                icon: "question",
                confirmButtonClass: "btn btn-primary",
                cancelButtonClass: "btn btn-outline-primary",
                confirmButtonText: "Sí",
                cancelButtonText: "No"
            });

            if (result.isConfirmed) {
                addCategory(response.similar_category.name);
            }

            return result.isConfirmed;
        } else {
            return false;
        }
    } catch (error) {
        return false;
    }
}

/**
 * Subir una categoría al servidor
 * @param name
 * @returns {Promise<void>}
 */
function uploadCategory(name) {
    promiseAjax('/api/category/create/', 'POST', {
        name,
        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
    }).then(() => {
        allCategories.push(name);
    });
}

/**
 * Convertir una URL a un archivo Blob
 * @param url
 * @param target
 */
function convertToBlob(url, target) {
    const xhr = new XMLHttpRequest();
    xhr.open('GET', url);
    xhr.responseType = 'blob';
    xhr.onload = () => {
        const blob = xhr.response;
        const fileName = url.substring(url.lastIndexOf('/') + 1); // Extraemos el nombre del archivo de la URL
        const file = new File([blob], fileName);
        const input = $(`#${target}`)[0];

        const container = new DataTransfer();
        container.items.add(file);
        input.files = container.files;

        input.dispatchEvent(new Event('change'));
    };
    xhr.send();
}

/**
 * Añadir las imágenes de los items al input
 */
function addItemImagesToInput() {
    $('#items_container').find('.list_item:not(#item_template) input[type="file"]').each((index, element) => {
        const url = $(element).parent().find(".item-image-url").val();
        const item_prefix = parseInt($(element).parent().attr('id'));

        $(element).attr('id', `id_${item_prefix}-image`);
        $(element).parent().find('.item-name').attr('id', `id_${item_prefix}-name`);

        if (url) {
            convertToBlob(url, $(element).attr('id'));
        }

        items_prefix.push(item_prefix);
    });

    item_last_prefix = items_prefix[items_prefix.length - 1];
}

/**
 * Poner la imagen de la lista por URL
 */
function putListImageByURL() {
    const url = $('#image_url').val();
    const target = 'image';
    convertToBlob(url, target);
}

/**
 * Recargar las categorías
 */
function reloadCategories() {
    let text_categories = $("#categories").val();
    text_categories = text_categories.split(",");

    $.each(text_categories, (index, element) => {
        addCategory(element, true);
    });
}

/**
 * Esta función se llama antes de enviar el formulario
 * @param event
 */
function beforeSendForm(event) {
    // Verificar que el nombre no esté vacío
    if (!$('#id_name').val().trim()) {
        toastMessage('error', 'El nombre de la lista no puede estar vacío');
        $('#id_name').focus();
        event.preventDefault();
        return;
    }

    // Verificar que la pregunta no esté vacía
    if (!$('#question').val().trim()) {
        toastMessage('error', 'La pregunta no puede estar vacía');
        $('#id_question').focus();
        event.preventDefault();
        return;
    }

    // Verificar que no haya ningun item vacio
    if (anyItemInputEmpty()) {
        focusOnFirstEmptyItem();
        toastMessage('error', 'Hay elementos vacíos, rellénelos todos antes de crear la lista');
        event.preventDefault();
        return;
    }

    // Verificar que no haya ningún item con más de 50 caracteres
    if (AnyInputTooLong()) {
        focusOnFirstTooLongInput();
        toastMessage('error', 'Ningún item puede tener más de 50 caracteres');
        event.preventDefault();
        return;
    }

    // Verificar que haya alguna categoría seleccionada
    if (categories.length === 0) {
        toastMessage('error', 'Debes seleccionar al menos una categoría');
        event.preventDefault();
        return;
    }

    // Eliminar el template
    $('#item_template').remove();

    // Agregar los prefijos de los items
    $('#items_prefix').val(items_prefix);

    // Agregar las categorías seleccionadas
    $('#categories').val(categories);

    // Mostrar el loader
    addPageLoader();
}

/**
 * Esta función se llama cuando el documento está listo
 */
function onDocumentReady() {
    $('#name').maxlength({
        warningClass: "badge badge-primary",
        limitReachedClass: "badge badge-danger"
    });

    $('#type').select2({
        placeholder: 'Selecciona una opción',
        minimumResultsForSearch: -1,
        ajax: {
            url: '/api/list/types', // La URL de tu endpoint de búsqueda
            dataType: 'json',
            delay: 0,
            processResults(data) {
                return {
                    results: data.types
                };
            }
        }
    });

    $(window).keydown(function(event){
        if(event.keyCode === 13) {
          event.preventDefault();
          return false;
        }
      });

    const imageInput = KTImageInput.getInstance($('#kt_image_input')[0]); // skipcq: JS-0125
    const itemsContainer = $('#items_container');

    imageInput.on('kt.imageinput.changed', changedListImage);
    imageInput.on('kt.imageinput.canceled', removeListImage);
    imageInput.on('kt.imageinput.removed', removeListImage);

    $('#create_element').on('click', createItem);

    itemsContainer.on('click', '.remove_item', removeItem);
    itemsContainer.on('change', '.item-image', itemImageChanged);

    $("#items_container").on('click', 'label.itemImageLabel', itemHasImage);

    $('#change_item_img').on('click', changeItemImage);
    $('#set_item_img').on('click', setItemImage);
    $('#cancel_item_img').on('click', cancelItemImage);

    $("#range_date_highlight").on("change", updateHighlightPrice);
    $("#cancel_highlight").on("click", cancelHighlight);

    getCategories();
    $('#add_category_button').on('click', () => {
        addCategory($('#add_category').val());
    });

    $("#categories_container").on('click', '.category', removeCategory);

    if (!edit_mode) { // skipcq: JS-0125
        // Añadir los items mínimos
        for (let i = 0; i < minItems; i++) {
            createItem();
        }
    }else {
        $("#submit_list").text("Guardar cambios");
        addItemImagesToInput();
        putListImageByURL();
        reloadCategories();
        actualizeItemNumber();
    }

    $('button[type=submit]').on('click', beforeSendForm);

    removePageLoader();
}

$(document).ready(onDocumentReady);