def create_item(item_form):
    """Función para crear un item"""

    if item_form.is_valid():
        # Guardamos el item y lo devolvemos
        return item_form.save(commit=False)
    else:
        return None
