import { removePageLoader } from "/static/assets/js/ranquiz/utils.js";

const avatarTemplate = $("#avatar_template");
const avatarBlockUI = new KTBlockUI($("#avatar_container").parent()[0], {
    message: '<div class="blockui-message"><span class="spinner-border text-primary"></span> Cargando avatares...</div>',
});

let avatars = [];
const exampleAvatar = {
    "id": 1,
    "name": "Tom",
    "image": "http://res.cloudinary.com/dhewpzvg9/image/upload/v1712514744/avatars/kidcithbb1ogolsssdma.png",
    "price": 15,
    "rarity": "Inicial",
    "bought": true,
    "equipped": false,
}
const rarityColors = {
    "Inicial": "badge-light-success",
    "Común": "badge-light-info",
    "Épico": "badge-light-primary",
    "Legendario": "badge-light-warning",
}

function getAvatars(mode="rarity") {
    // TODO: Obtener los avatares de base de datos
    avatarBlockUI.block();
    $("#avatar_container").empty();

    avatarBlockUI.release();
    avatars = [exampleAvatar];

    $.each(avatars, (index, avatar) => {
        const newAvatar = avatarTemplate.clone();

        newAvatar.removeAttr("id");
        newAvatar.removeClass("d-none").addClass("d-flex");
        newAvatar.find(".avatar_image").attr("src", avatar.image);
        newAvatar.find(".avatar_name").text(avatar.name);
        newAvatar.find(".avatar_price").text(avatar.price);
        newAvatar.find(".avatar_rarity").text(avatar.rarity);
        newAvatar.find(".avatar_rarity").addClass(rarityColors[avatar.rarity]);

        if (avatar.bought && avatar.equipped) {
            newAvatar.find(".buy_avatar").empty();
            newAvatar.find(".buy_avatar").removeClass(".buy_avatar").addClass("equipped_avatar");
            newAvatar.find(".equipped_avatar").html(`<i class='bi bi-person-square'></i> Equipado`).addClass("btn-success").removeClass("btn-info");

        }else if (avatar.bought) {
            newAvatar.find(".buy_avatar").empty();
            newAvatar.find(".buy_avatar").removeClass(".buy_avatar").addClass("equip_avatar");
            newAvatar.find(".equip_avatar").html("Equipar").addClass("btn-primary").removeClass("btn-info");
        }

        newAvatar.appendTo("#avatar_container");
    });
}

/**
 * Función que se ejecuta cuando el documento está listo
 */
function onDocumentReady() {
  getAvatars();

  removePageLoader();
}

$(document).ready(onDocumentReady);