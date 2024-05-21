from datetime import datetime


def format_elapsed_time(date_time):
    """Formatea el tiempo transcurrido desde una fecha dada en un formato legible para el usuario"""
    current_date = datetime.now()
    elapsed_time = current_date - date_time
    elapsed_seconds = int(elapsed_time.total_seconds())

    if elapsed_seconds < 60:
        return f"Hace {elapsed_seconds} s"

    elapsed_minutes = elapsed_seconds // 60
    if elapsed_minutes < 60:
        return f"Hace {elapsed_minutes} min"

    elapsed_hours = elapsed_minutes // 60
    if elapsed_hours < 24:
        return f"Hace {elapsed_hours} h"

    elapsed_days = elapsed_hours // 24
    if elapsed_days < 30:
        return f"Hace {elapsed_days} d"

    # If it has been more than a month, return the original date
    return date_time.strftime("%d/%m/%Y")
