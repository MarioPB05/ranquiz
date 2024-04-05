from api.models import Category


def create_category(category_form):
    """Función para crear una categoría"""

    if category_form.is_valid():
        # Guardamos la categoría y la devolvemos
        return category_form.save(commit=False)
    else:
        return None


def get_all_categories():
    """Función para obtener todas las categorías"""

    # Obtenemos todas las categorías
    categories = Category.objects.all()

    return categories
