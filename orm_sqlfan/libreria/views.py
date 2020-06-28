from django.db import transaction
from django.shortcuts import render
from libreria.services import actualizar_libro_y_autor

# Create your views here.
@transaction.non_atomic_requests
def get_actualizar_libro_autor(request):
            actualizar_libro_y_autor()
            return render(request, "Libro y autor")
