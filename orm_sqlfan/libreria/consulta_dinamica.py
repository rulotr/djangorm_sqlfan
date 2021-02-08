from libreria.models.libros import Libro

def buscar_libro(buscar, con_paginas=False):
    filtro={}
    col_numero = 'isbn'
    col_letras = 'titulo'

    if(con_paginas):
        filtro['paginas__gt'] = 0

    if(buscar.isnumeric()):
        filtro[col_numero] = buscar
    else:
        filtro[f'{col_letras}__contains'] = buscar
    
    libro = Libro.objects.filter(**filtro).values('isbn','titulo','paginas')
    print('Filtro:')
    print(filtro)
    print(libro)

def buscar_libro2(buscar, con_paginas=False):
    from django.db.models import Q

    filtro={}
    col_numero = 'isbn'
    col_letras = ['titulo','categoria']
    query1 = Q()


    if(buscar.isnumeric()):
        filtro[col_numero] = buscar
    else:
        for nom_col in col_letras:
            condicion = {f'{nom_col}__contains': buscar }
            query1 |= Q(**condicion)
    query1.connector = 'OR'

    if(con_paginas):
        query1.add(Q(paginas__gt=0), Q.AND)

        
    libro = Libro.objects.filter(query1).values('isbn','titulo','paginas')
    print('Filtro:')
    print(query1)
    print(libro)






