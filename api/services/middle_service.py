from api.services.notification_service import create_notification, get_notification_type


def call_create_notification(target, notification_type_id, user, share_code):
    """Llama al servicio de notificaciones para crear una notificación"""
    notification_type = get_notification_type(notification_type_id)
    return create_notification(target, notification_type, user, share_code)
