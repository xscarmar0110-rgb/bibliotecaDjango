from django.shortcuts import render
from .models import Libro, Autor, Editorial

# Create your views here.
def principal(request):
    libro = Libro.objects.all().first().update(titulo="Nuevo título", idioma="Español")

    libro.titulo = libro.tiutulo.upper()
    libro.titulo = libro.titulo.replace("A", "4")
    libro.save()
    
    return render(request, 'catalogo/principal.html')