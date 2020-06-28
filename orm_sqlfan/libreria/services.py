from libreria.models.autores import Autor
from libreria.models.libros import Libro


def consulta_libro_y_autor():
    libro = Libro.objects.values('isbn','titulo').get(isbn='1617291269')
    autor = Autor.objects.values('id','nombre').get(pk=273)
    print(F"Libro: {libro}")
    print(F"Autor: {autor}")

def actualizar_libro_y_autor():
    autor = Autor.objects.get(pk=273)
    libro = Libro.objects.get(isbn='1617291269')
    autor.nombre = "Autor de cobol"
    libro.titulo = "cobol"
    autor.save()
    libro.save()

def libro_y_autor_originales():
    autor = Autor.objects.get(pk=273)
    libro = Libro.objects.get(isbn='1617291269')

    autor.nombre = 'Bear P. Cahill'
    libro.titulo = 'iOS in Practice'
    autor.save()
    libro.save()

