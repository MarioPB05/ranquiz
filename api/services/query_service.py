from django.db import connection


def execute_query(query, params):
    """Función que ejecuta una query"""
    with connection.cursor() as cursor:
        cursor.execute(query, params)

        return [dict(zip([col[0] for col in cursor.description], row)) for row in cursor.fetchall()]
