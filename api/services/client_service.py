from api.forms.client_form import CreateClientForm


def get_client_form(request):
    """Obtiene el formulario para la creación de un cliente"""
    return CreateClientForm(request.POST) if request.method == 'POST' else CreateClientForm()


def create_client(client_form):
    """Función que crea un cliente en la aplicación"""
    if client_form.is_valid():
        # Guardamos el cliente y lo devolvemos
        return client_form.save(commit=False)
    else:
        return None
