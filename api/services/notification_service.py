from api.models import Notification, NotificationRead
from api.services import PAGINATION_ITEMS_PER_PAGE
from api.services.list_service import get_pagination_data
from api.services.query_service import execute_query
from core import format_elapsed_time


def get_notifications(user, page_number=1, show_all=False):
    """Servicio que devuelve las notificaciones de un usuario paginadas"""
    query = ""

    if show_all:
        query = """
        WITH own_notifications AS (
            SELECT n.*, EXISTS(
                SELECT 1 FROM api_notificationread r
                WHERE r.user_id = %s AND r.notification_id = n.id
            ) AS userRead
            FROM api_notification n
            WHERE n.user_id = %s AND n.target = %s
        ),
        following_notifications AS (
            SELECT n.*, EXISTS(
                SELECT 1 FROM api_notificationread r
                WHERE r.user_id = %s AND r.notification_id = n.id
            ) AS userRead
            FROM api_notification n
            WHERE n.user_id IN (
                SELECT user_followed_id FROM ranquiz.api_userfollow WHERE user_id = %s
            ) AND n.target = %s
        )
        SELECT *, nt.id as type_id, own.id as notification_id FROM own_notifications own
        JOIN api_notificationtype nt ON own.type_id = nt.id
        UNION ALL
        SELECT *, nt.id as type_id, flw.id as notification_id FROM following_notifications flw
        JOIN api_notificationtype nt ON flw.type_id = nt.id
        ORDER BY date DESC
        LIMIT %s OFFSET %s;
        """
    else:
        query = """
        WITH own_notifications AS (
            SELECT n.*, EXISTS(
                SELECT 1 FROM api_notificationread r
                WHERE r.user_id = %s AND r.notification_id = n.id
            ) AS userRead
            FROM api_notification n
            WHERE n.user_id = %s AND n.target = %s
        ),
        following_notifications AS (
            SELECT n.*, EXISTS(
                SELECT 1 FROM api_notificationread r
                WHERE r.user_id = %s AND r.notification_id = n.id
            ) AS userRead
            FROM api_notification n
            WHERE n.user_id IN (
                SELECT user_followed_id FROM ranquiz.api_userfollow WHERE user_id = %s
            ) AND n.target = %s
        )
        SELECT own.*, nt.id as type_id, nt.*, own.id as notification_id FROM own_notifications own
        JOIN api_notificationtype nt ON own.type_id = nt.id
        LEFT JOIN api_notificationread r1 ON own.id = r1.notification_id
        WHERE r1.user_id IS NULL
        UNION ALL
        SELECT flw.*, nt.id as type_id, nt.*, flw.id as notification_id FROM following_notifications flw
        JOIN api_notificationtype nt ON flw.type_id = nt.id
        LEFT JOIN api_notificationread r2 ON flw.id = r2.notification_id
        WHERE r2.user_id IS NULL
        ORDER BY date DESC
        LIMIT %s OFFSET %s;
        """

    target_own = Notification.TARGET_CHOICES[0][0]
    target_following = Notification.TARGET_CHOICES[1][0]
    offset = int((page_number - 1) * PAGINATION_ITEMS_PER_PAGE/2)
    params = [user.id, user.id, target_own, user.id, user.id, target_following, int(PAGINATION_ITEMS_PER_PAGE/2),
              offset]

    notifications = execute_query(query, params)

    # Apply format_elapsed_time to each notification
    for notification in notifications:
        notification['ellapsed_time'] = format_elapsed_time(notification['date'])

    return notifications


def get_notifications_pagination(user, page_number, show_all=False):
    """Servicio que devuelve la cantidad de notificaciones"""
    notifications = None

    if show_all:
        notifications = Notification.objects.filter(user=user).count()
    else:
        notifications = Notification.objects.filter(user=user).exclude(notificationread__user=user).count()

    return get_pagination_data(notifications, page_number)


def read_notification(user, notification_id):
    """Servicio que marca una notificación como leída"""
    if NotificationRead.objects.filter(user=user, notification_id=notification_id).exists():
        return

    notification = Notification.objects.get(id=notification_id)
    notification_read = NotificationRead.objects.create(user=user, notification=notification)
    notification_read.save()


def count_unread_notifications(user):
    """Servicio que devuelve la cantidad de notificaciones no leídas"""
    query = """
        WITH own_notifications AS (
            SELECT n.*, EXISTS(
                SELECT 1 FROM api_notificationread r
                WHERE r.user_id = %s AND r.notification_id = n.id
            ) AS userRead
            FROM api_notification n
            WHERE n.user_id = %s AND n.target = %s
        ),
        following_notifications AS (
            SELECT n.*, EXISTS(
                SELECT 1 FROM api_notificationread r
                WHERE r.user_id = %s AND r.notification_id = n.id
            ) AS userRead
            FROM api_notification n
            WHERE n.user_id IN (
                SELECT user_followed_id FROM ranquiz.api_userfollow WHERE user_id = %s
            ) AND n.target = %s
        )
        SELECT COUNT(*) as count FROM own_notifications own
        JOIN api_notificationtype nt ON own.type_id = nt.id
        LEFT JOIN api_notificationread r1 ON own.id = r1.notification_id
        WHERE r1.user_id IS NULL
        UNION ALL
        SELECT COUNT(*) as count FROM following_notifications flw
        JOIN api_notificationtype nt ON flw.type_id = nt.id
        LEFT JOIN api_notificationread r2 ON flw.id = r2.notification_id
        WHERE r2.user_id IS NULL
            """

    target_own = Notification.TARGET_CHOICES[0][0]
    target_following = Notification.TARGET_CHOICES[1][0]
    params = [user.id, user.id, target_own, user.id, user.id, target_following]

    notifications = execute_query(query, params)

    return notifications[0]['count'] + notifications[1]['count']


def clear_notifications(user):
    """Servicio que marca todas las notificaciones como leídas"""
    NotificationRead.objects.filter(user=user).delete()
    Notification.objects.filter(user=user).delete()


def read_notifications(user, notification_ids):
    """Servicio que marca varias notificaciones como leídas"""
    notifications = Notification.objects.filter(id__in=notification_ids)

    for notification in notifications:
        read_notification(user, notification.id)
