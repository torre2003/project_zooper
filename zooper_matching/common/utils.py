from django.core.paginator import Paginator



def paginacion_comun (items, elementos_por_pagina=20, pagina=1):
    paginacion = {
        'elementos_por_pagina':20,
        'total_elementos':None,
        'numero_paginas':None,
        'pagina_anterior':None,
        'pagina_actual':None,
        'pagina_siguiente':None,
    }
    # articulos = ManagerArticuloJumbo.obtenerArticulos().order_by('id');

    paginacion['elementos_por_pagina'] = elementos_por_pagina
    p = Paginator(items, elementos_por_pagina)
    paginacion['total_elementos'] = p.count
    paginacion['numero_paginas'] = p.num_pages
    numero_pagina_actual = 1
    # print '---'
    # print datos
    # if 'pagina' in datos:
    numero_pagina_actual = pagina
    if numero_pagina_actual < 1:
        numero_pagina_actual= 1
    if numero_pagina_actual > p.num_pages:
        numero_pagina_actual = p.num_pages

    paginacion['pagina_actual'] = numero_pagina_actual
    pagina_actual = p.page(numero_pagina_actual)

    if pagina_actual.has_previous():
        paginacion['pagina_anterior'] = numero_pagina_actual - 1
    if pagina_actual.has_next():
        paginacion['pagina_siguiente'] = numero_pagina_actual + 1
    elementos_pagina = pagina_actual.object_list
    return elementos_pagina, paginacion