from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_register_email(client):
    """Envía un correo electrónico al usuario registrado."""
    html_content = render_to_string('emails/register_email.html', {'client_name': client.name})
    text_content = strip_tags(html_content)

    msg = EmailMultiAlternatives('¡Bienvenido a Ranquiz!', text_content, 'ranquiz.team@gmail.com', [client.email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
