import { removePageLoader, toastMessage } from "/static/assets/js/ranquiz/utils.js";

const avatarTemplate = $("#avatar_template");
const avatarBlockUI = new KTBlockUI($("#avatar_container").parent()[0], {
    message: '<div class="blockui-message"><span class="spinner-border text-primary"></span> Cargando avatares...</div>',
});

const rarityColors = {
    "Inicial": "badge-light-success",
    "Común": "badge-light-info",
    "Épico": "badge-light-primary",
    "Legendario": "badge-light-warning",
}

let avatars = [];
const exampleAvatar = {
    "id": 1,
    "name": "Tom",
    "image": "http://res.cloudinary.com/dhewpzvg9/image/upload/v1712514744/avatars/kidcithbb1ogolsssdma.png",
    "price": 15,
    "rarity": "Inicial",
    "bought": false,
    "equipped": false,
}

const exampleAvatar2 = {
    "id": 2,
    "name": "Carlos",
    "image": "http://res.cloudinary.com/dhewpzvg9/image/upload/v1712514744/avatars/kidcithbb1ogolsssdma.png",
    "price": 15,
    "rarity": "Inicial",
    "bought": false,
    "equipped": false,
}

/**
 * Función que cambia el botón a equipado
 * @param avatar
 */
function changeButtonToEquipped(avatar) {
    avatar.find("button").empty();
    avatar.find("button").removeClass("buy_avatar").removeClass("equip_avatar").addClass("equipped_avatar");
    avatar.find("button").html(`<i class='bi bi-person-square'></i> Equipado`);
    avatar.find("button").addClass("btn-success").removeClass("btn-info").removeClass("btn-primary");
}

/**
 * Función que cambia el botón a equipar
 * @param avatar
 */
function changeButtonToBought(avatar) {
    avatar.find("button").empty();
    avatar.find("button").removeClass("buy_avatar").removeClass("equipped_avatar").addClass("equip_avatar");
    avatar.find("button").html("Equipar");
    avatar.find("button").addClass("btn-primary").removeClass("btn-info").removeClass("btn-success");
}

/**
 * Función que obtiene los avatares de la base de datos y los muestra en la página
 * @param mode
 */
function getAvatars(mode="rarity") {
    // TODO: Obtener los avatares de base de datos
    avatarBlockUI.block();
    $("#avatar_container").empty();

    avatarBlockUI.release();
    avatars = [exampleAvatar, exampleAvatar2];

    $.each(avatars, (index, avatar) => {
        const newAvatar = avatarTemplate.clone();

        newAvatar.removeAttr("id");
        newAvatar.removeClass("d-none").addClass("d-flex");
        newAvatar.attr("data-id", avatar.id);
        newAvatar.find(".avatar_image").attr("src", avatar.image);
        newAvatar.find(".avatar_name").text(avatar.name);
        newAvatar.find(".avatar_price").text(avatar.price);
        newAvatar.find(".avatar_rarity").text(avatar.rarity);
        newAvatar.find(".avatar_rarity").addClass(rarityColors[avatar.rarity]);

        if (avatar.bought && avatar.equipped) {
            changeButtonToEquipped(newAvatar);

        }else if (avatar.bought) {
            changeButtonToBought(newAvatar);
        }

        newAvatar.appendTo("#avatar_container");
    });
}

/**
 * Función que compra un avatar
 * @param avatarId
 */
function buyAvatar(avatarId) {
    // TODO: Comprar el avatar en base de datos
    changeButtonToBought($(`div[data-id=${avatarId}]`));
    toastMessage("success", "Avatar comprado");
}

/**
 * Función que equipa un avatar
 * @param avatarId
 */
function equipAvatar(avatarId) {
    // TODO: Equpar el avatar en base de datos
    changeButtonToBought($(".equipped_avatar").parent().parent());
    changeButtonToEquipped($(`div[data-id=${avatarId}]`));
    toastMessage("success", "Avatar equipado");
}

/**
 * Función que se ejecuta cuando el documento está listo
 */
function onDocumentReady() {
  getAvatars();

  $("#avatar_container").on("click", ".buy_avatar", (event) => {
      buyAvatar($(event.target).parent().parent().attr("data-id"));
  });

  $("#avatar_container").on("click", ".equip_avatar", (event) => {
      equipAvatar($(event.target).parent().parent().attr("data-id"));
  });

  $("#avatar_order").on("change", () => {
      getAvatars($("#avatar_order").val());
  });

  removePageLoader();
}

$(document).ready(onDocumentReady);