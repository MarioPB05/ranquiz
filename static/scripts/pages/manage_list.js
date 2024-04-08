import {removePageLoader, initializeFlatpickr, promiseAjax} from "/static/assets/js/ranquiz/utils.js";

const minItems = 5;
let items_prefix = [];
let item_last_prefix = 0;

function changedListImage() {
    $('label[for="id_image"]').hide();
}

function removeListImage() {
    $('label[for="id_image"]').show();
}

function createItem() {
    // Clonar la plantilla de un item
    const item = $('#item_template').clone();

    // Remover el ID de la plantilla
    item.removeAttr('id');

    // Obtener el prefijo del item
    const prefix = 'id_' + (item_last_prefix + 1) + '-';

    // Actualizar los datos del prefijo
    item_last_prefix++;
    items_prefix.push(item_last_prefix);

    // Guardar el prefijo en el item
    item.attr('data-prefix', item_last_prefix);

    // Cambiar el ID y name del input de la imagen
    const imageInput = item.find('#id_template-image');
    imageInput.attr('id', prefix + 'image');
    imageInput.attr('name', prefix + 'image');

    // Actualizar el atributo for del label
    item.find('label[for="id_template-image"]').attr('for', prefix + 'image');

    // Cambiar el ID y name del input del nombre
    const nameInput = item.find('#id_template-name');
    nameInput.attr('id', prefix + 'name');
    nameInput.attr('name', prefix + 'name');

    // Actualizar el atributo for del label
    item.find('label[for="id_template-name"]').attr('for', prefix + 'name');

    // Mostrar el item
    item.removeClass('d-none').addClass('d-flex');

    // Añadir el item al contenedor
    $('#items_container').append(item);
}

function removeItem(event) {
    // Comprobar que haya más de 4 items
    if (items_prefix.length <= minItems) {
        // TODO: Mostrar un mensaje de error (Como mínimo minItems items)
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

    console.log(target);

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

    console.log(input)

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
                console.error(error);
            });
    }
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

$(document).ready(function () {

    initializeFlatpickr("#range_date_highlight", 'range', moment().format('DD-MM-YYYY'));

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

    const imageInput = KTImageInput.getInstance($('#kt_image_input')[0]);
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

    // Añadir los items mínimos
    for (let i = 0; i < minItems; i++) {
        createItem();
    }

    removePageLoader();
});
