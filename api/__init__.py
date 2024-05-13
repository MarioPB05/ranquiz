import datetime


def sec_to_time(seconds):
    # Calcular las horas, minutos y segundos
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)

    # Crear un objeto timedelta con los valores calculados
    delta_time = datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)

    # Convertir el objeto timedelta a un objeto datetime
    base_time = datetime.datetime(1, 1, 1)
    time = base_time + delta_time

    return time.time().__str__()
