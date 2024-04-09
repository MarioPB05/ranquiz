import {removePageLoader, initializeFlatpickr, promiseAjax, toastMessage} from "/static/assets/js/ranquiz/utils.js";

const minItems = 5;
let items_prefix = [];
let item_last_prefix = 0;
let categories = [];
const maxCategories = 5;
const maxCategoryLength = 25;
let allCategories = [];


function changedListImage() {
    $('label[for="id_image"]').hide();
}

function removeListImage() {
    $('label[for="id_image"]').show();
}

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

    // Obtener el prefijo del item
    const prefix = (item_last_prefix + 1) + '-';

    // Actualizar los datos del prefijo
    item_last_prefix++;
    items_prefix.push(item_last_prefix);

    // Guardar el prefijo en el item
    item.attr('data-prefix', item_last_prefix);

    // Cambiar el ID y name del input de la imagen
    const imageInput = item.find('#id_template-image');
    imageInput.attr('id', 'id_' + prefix + 'image');
    imageInput.attr('name', prefix + 'image');

    // Actualizar el atributo for del label
    item.find('label[for="id_template-image"]').attr('for', 'id_' + prefix + 'image');

    // Cambiar el ID y name del input del nombre
    const nameInput = item.find('#id_template-name');
    nameInput.attr('id', 'id_' +  prefix + 'name');
    nameInput.attr('name', prefix + 'name');

    // Actualizar el atributo for del label
    item.find('label[for="id_template-name"]').attr('for', 'id_' + prefix + 'name');

    // Mostrar el item
    item.removeClass('d-none').addClass('d-flex');

    // Añadir el item al contenedor
    $('#items_container').append(item);

    // Actualizar el número de items
    actualizeItemNumber();

    // Enfocar en el input del nombre
    focusOnFirstEmptyItem();
}

function removeItem(event) {
    // Comprobar que haya más de 5 items
    if (items_prefix.length <= minItems) {
        toastMessage('error', 'El minimo de elementos es ' + minItems + '.');
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
    $('#change_item_img').parent().attr('data-target', '#' + target.id);

    // Mostrar el modal
    $('#image_previewer').modal('show');
}

function itemImageChanged(event) {
    // Obtener el archivo seleccionado
    const file = event.target.files[0];

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

function getModalInputTarget(event) {
    return $($(event.target).parent().attr('data-target'));
}

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

function setItemImage(event) {
    // Obtener el target (Input)
    const input = getModalInputTarget(event);

    // Cambiar la clase para indicarle al usuario que la imagen se ha seleccionado
    input.parent().find('label>i')
        .removeClass('text-primary-800').addClass('text-white');
}

function cancelItemImage(event) {
    // Obtener el target (Input)
    const input = getModalInputTarget(event);

    // Cambiar la clase para indicarle al usuario que la imagen no se ha seleccionado
    input.parent().find('label>i')
        .removeClass('text-white').addClass('text-primary-800');

    // Limpiar el input
    input.val('');
}

function updateHighlightPrice() {
    let dates = $("#range_date_highlight").val().split(" hasta ");

    if (dates.length === 2) {
        promiseAjax(`/api/shop/highlight/calculator?start_date=${dates[0]}&end_date=${dates[1]}`)
            .then(response => {
                $('#highlight_price').text(response.price);
            })
            .catch(error => {
                toastMessage('error', 'Ha ocurrido un error al calcular el precio del destacado')
            });
    }
}

function cancelHighlight() {
    $('#range_date_highlight').flatpickr().clear();
    $('#highlight_price').text('0');
}

function itemHasImage(event) {
    // Obtener el target (Input)
    const input = $("#" + $(this).attr('for'));

    // Comprobar si ya se ha seleccionado una imagen para mosrar el modal directamente
    if (input[0] && input[0].files.length > 0) {
        event.preventDefault();
        showItemPreviewModal(input[0]);
    }
}

function anyItemInputEmpty() {
    // Comprueba si hay algún input de item vacío
    let empty = false;

    $('#items_container .list_item:not(#item_template)').find('input[type="text"]').each(function () {

        if ($(this).val() === '') {
            empty = true;
            return false;
        }

    });

    return empty;
}

function focusOnFirstEmptyItem() {
    // Enfoca en el primer item vacío
    $('#items_container .list_item:not(#item_template)').find('input[type="text"]').each(function () {

        if ($(this).val() === '') {
            $(this).focus();
            return false;
        }

    });

}

function actualizeItemNumber() {
    // Actualiza el número de items

    let i = 0;

    $('#items_container').find('.list_item:not(#item_template)').each(function () {
        i++;
    });

    $("#item_number").text(i);
}

async function addCategory(name) {

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

    // Añadir la categoría a la lista
    categories.push(name);
    $('#add_category').val('');

    // Añaadir la categoría al contenedor
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
        toastMessage('error', 'El máximo de categorías es ' + maxCategories);
        return false;

    } else if (name.length >= maxCategoryLength) {
        toastMessage('error', 'El nombre de la categoría no puede ser mayor a ' + maxCategoryLength + ' caracteres');
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

function getCategories() {

    promiseAjax('/api/category/').then(response => {
        allCategories = response.categories.map(function(category) {
            return category.name;
        });

        $("#actual_categories").html('');
        allCategories.forEach(category => {
            $("#actual_categories").append(`<option value="${category}">`);
        });
    });
}

async function acceptSimilarCategory(name) {
    try {
        const response = await promiseAjax(`/api/category/validate/${name}`);

        if (!response.validate) {
            const result = await Swal.fire({ // skipcq: JS-0125
                title: "¿Quieres decir " + response.similar_category.name + "?",
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

function uploadCategory(name) {
    promiseAjax('/api/category/create/', 'POST', {
        name: name,
        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
    }).then(() => {
        allCategories.push(name);
    });
}

function beforeSendForm() {
    // Eliminar el template
    $('#item_template').remove();

    // Agregar los prefijos de los items
    $('#items_prefix').val(items_prefix);

    // Agregar las categorías seleccionadas
    $('#categories').val(categories);
}

$(document).ready(function () {

    initializeFlatpickr("#range_date_highlight", 'range', moment().format('DD-MM-YYYY')); // skipcq: JS-0125

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
            processResults: function (data) {
                return {
                    results: data.types
                };
            }
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
    $('#add_category_button').on('click', function () {
        addCategory($('#add_category').val());
    });

    $("#categories_container").on('click', '.category' ,removeCategory);

    // Añadir los items mínimos
    for (let i = 0; i < minItems; i++) {
        createItem();
    }

    $('button[type=submit]').on('click', beforeSendForm);

    removePageLoader();
});
