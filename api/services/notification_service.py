from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import OuterRef, Exists, Q

from api.models import Notification, NotificationRead
from api.services import PAGINATION_ITEMS_PER_PAGE
from api.services.list_service import get_pagination_data
from api.services.query_service import execute_query
from api.services.social_service import get_following
from core import format_elapsed_time


# def get_notifications(user, page_number=1):
#     """Obtiene las notificaciones de un usuario"""
#     own_notifications = Notification.objects.filter(
#         user=user, target=Notification.TARGET_CHOICES[0][0]
#     ).annotate(
#         read=Exists(
#             NotificationRead.objects.filter(user=user, notification=OuterRef('pk'))
#         )
#     )
#
#     for notification in own_notifications:
#         notification.ellapsed_time = format_elapsed_time(notification.date)
#
#     # Obtener los usuarios que sigue el usuario
#     temp = get_following(user)
#     following_users = [user_follow.user_followed for user_follow in temp]
#
#     following_notifications = Notification.objects.filter(
#         user__in=following_users,
#         target=Notification.TARGET_CHOICES[1][0]
#     ).annotate(
#         read=Exists(
#             NotificationRead.objects.filter(user=user, notification=OuterRef('pk'))
#         )
#     )
#
#     for notification in following_notifications:
#         notification.ellapsed_time = format_elapsed_time(notification.date)
#
#     all_notifications = own_notifications.union(following_notifications).order_by('-date')
#
#     paginator = Paginator(all_notifications, PAGINATION_ITEMS_PER_PAGE/2)
#
#     try:
#         notifications_page = paginator.page(page_number)
#     except PageNotAnInteger:
#         # If page is not an integer, deliver first page.
#         notifications_page = paginator.page(1)
#     except EmptyPage:
#         # If page is out of range (e.g. 9999), deliver last page of results.
#         notifications_page = paginator.page(paginator.num_pages)
#
#     return notifications_page


def get_notifications(user, page_number=1):
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

    target_own = Notification.TARGET_CHOICES[0][0]
    target_following = Notification.TARGET_CHOICES[1][0]
    offset = int((page_number - 1) * PAGINATION_ITEMS_PER_PAGE/2)
    params = [user.id, user.id, target_own, user.id, user.id, target_following, int(PAGINATION_ITEMS_PER_PAGE/2), offset]

    notifications = execute_query(query, params)

    # Apply format_elapsed_time to each notification
    for notification in notifications:
        notification['ellapsed_time'] = format_elapsed_time(notification['date'])

    return notifications


def get_notifications_pagination(user, page_number):
    """Servicio que devuelve la cantidad de notificaciones"""
    query = Q(user=user, target=Notification.TARGET_CHOICES[0][0]) | Q(
        user__in=get_following(user), target=Notification.TARGET_CHOICES[1][0]
    )

    notifications = Notification.objects.filter(query).count()

    return get_pagination_data(notifications, page_number)


def read_notification(user, notification_id):
    """Servicio que marca una notificación como leída"""
    if NotificationRead.objects.filter(user=user, notification_id=notification_id).exists():
        return

    notification = Notification.objects.get(id=notification_id)
    notification_read = NotificationRead.objects.create(user=user, notification=notification)
    notification_read.save()
