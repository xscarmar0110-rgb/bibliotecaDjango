from django.shortcuts import render
from datetime import date
from decimal import Decimal
from .models import Libro, Autor, Editorial

# Create your views here.
def principal(request):
    # Primer registro
    libro = Libro.objects.create(
        titulo="JavaScript para nadie",
        isbn="97801",
        sinopsis="Introducción a JavaScript para gente muy lista.",
        fecha_publicacion=date(2024, 5, 10),
        paginas=280,
        precio=Decimal("24.90"),
        disponible=True,
    )
    print(libro.pk, libro.titulo)

    return render(request, 'catalogo/principal.html')