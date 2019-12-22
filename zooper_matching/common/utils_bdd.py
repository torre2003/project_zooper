from django.db import connection


def ejecutar_consulta(query):
    consulta = query
    with connection.cursor() as cursor:
        cursor.execute(consulta)
        return dictfetchall(cursor)


def dictfetchall(cursor):
    #"Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def extraer_data_comunicacion_scrapy(codigo):
    try:
        query = """SELECT * FROM comunicacion_scrapy WHERE codigo='{}'"""
        query = query.format(codigo)
        resultados = ejecutar_consulta(query)
        if len(resultados) > 0:
            return resultados[0]['data']
        return data
    except Exception, e:
        return None