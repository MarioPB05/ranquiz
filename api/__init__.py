import datetime
import math

from api.services import PAGINATION_ITEMS_PER_PAGE


def sec_to_time(seconds):
    """Convierte segundos a formato HH:MM:SS"""
    # Calcular las horas, minutos y segundos
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)

    # Crear un objeto timedelta con los valores calculados
    delta_time = datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)

    # Convertir el objeto timedelta a un objeto datetime
    base_time = datetime.datetime(1, 1, 1)
    time = base_time + delta_time

    return time.time().__str__()


def get_page_range(current_page, total_pages, display_range=10):
    """Función que devuelve el rango de páginas a mostrar en la paginación"""
    # Ensure current_page is within bounds
    current_page = max(1, min(current_page, total_pages))

    # Calculate the start and end of the range
    half_range = display_range // 2
    start = max(1, current_page - half_range)
    end = min(total_pages, current_page + half_range)

    # Adjust start or end if the range is less than display_range
    if end - start < display_range - 1:
        if start == 1:
            end = min(total_pages, start + display_range - 1)
        elif end == total_pages:
            start = max(1, end - display_range + 1)

    return list(range(start, end + 1))


def get_pagination_data(count, page_number):
    """Función que devuelve los datos de paginación"""
    pages = math.ceil(count / (PAGINATION_ITEMS_PER_PAGE / 2))
    return {
        'total': count,
        'pages': pages,
        'number': page_number,
        'page_range': get_page_range(page_number, pages, 6),
        'has_previous': page_number > 1,
        'has_next': page_number < pages,
        'has_other_pages': pages > 1,
        'previous_page_number': page_number - 1,
        'next_page_number': page_number + 1,
    }
