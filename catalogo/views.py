from django.shortcuts import render, get_object_or_404
from .models import Libro

# Create your views here.
def lista_libros(request):
    libros = Libro.objects.order_by('titulo')
    return render(request, 'catalogo/lista_libros.html', {'libros': libros})

def detalle_libro(request, libro_id):
    libro = get_object_or_404(Libro, pk=libro_id)
    return render(request, 'catalogo/detalle_libro.html', {'libro': libro})