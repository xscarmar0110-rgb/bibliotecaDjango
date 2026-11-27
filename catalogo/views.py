from django.shortcuts import render, get_object_or_404
from datetime import date
from decimal import Decimal
from .models import Libro, Autor, Editorial, Prestamo
# Añado por ejemplo el sum para utilizarlo con el aggregate
from django.db.models import Q, Sum, Avg, Count, Max
from django.db.models import Prefetch
from django.db import transaction
from django.utils import timezone

# Create your views here.
def principal(request):
    # Primer registro
    consulta = Libro.objects.filter(Q(precio__lt=Decimal("10")) | Q(paginas__lt=150))
    for libro in consulta:
        print(libro.titulo)


    # Creamos el agregate como un diccionario y lo mostramos.
    estadisticas = Libro.objects.aggregate(
    precio_medio = Avg("precio"),
    total_paginas=Sum("paginas"),
    total_libros=Count("id"),
    mas_caro=Max("precio"),
    )
    print(estadisticas)

    # EL annotate, lo que es devolver una lista de filas, como en un 
    # group by en SQL,
    # LO calcula por cada libro o grupo de libros

    por_genero = Libro.objects.values("genero").annotate(
    cantidad=Count("id"),
    precio_medio=Avg("precio"),
    )
    print(por_genero)

    # Por ultimo tenemos que meterlo en el return para tenerlo en la pagina
    return render(request, 'catalogo/principal.html', {
    'libros': consulta,
    'estadisticas': estadisticas,
    'por_genero': por_genero,
    })

#aggregate() hace un cálculo sobre todo el conjunto 
# de resultados de una consulta y devuelve un diccionario con el resultado, 
# no una lista de libros. Es como hacer SUM, AVG, COUNT, etc. en SQL.


def editorial(request, pk):
    # Buscamos la editorial del pk de la URL y, con el Prefetch, le añadimos
    # la lista "libros_disponibles" que recorre la plantilla
    editorial = get_object_or_404(
        Editorial.objects.prefetch_related(
            Prefetch(
                "libros",
                queryset=Libro.objects.filter(disponible=True).order_by("titulo"),
                to_attr="libros_disponibles",
            )
        ),
        pk=pk,
    )

    return render(request, 'catalogo/editorial.html', {'editorial': editorial})

def libro(request, pk):
    # select_related para la editorial (una) y prefetch_related para los autores (varios).
    # get_object_or_404 da un 404 si el libro no existe, en vez de un error 500
    libro = get_object_or_404(
        Libro.objects.select_related("editorial").prefetch_related("autores"),
        pk=pk,
    )

    return render(request, 'catalogo/libro.html', {'libro': libro})

def autor(request, pk):
    autor = get_object_or_404(Autor, pk = pk)
    return render(request, 'catalogo/autor.html', {'autor': autor})


# EL prefetch: sirve para cuando tengo que traer varios de uno 

# El select related sirve para cuando solo me tengo que traer un dato de la consulta

# EL related_name le ponemos el nombre de la clase en plural


def prestar_libro(request, libro_id, usuario):
    with transaction.atomic():
        libro = Libro.objects.select_for_update().get(pk=libro_id)
        if not libro.disponible:
            raise ValueError("El libro no esta disponible")

        prestamo = Prestamo.objects.create(
            libro = libro,
            usuario = usuario,
        )
        libro.disponible = False
        libro.save(update_fields=["disponible"])
        return prestamo

    
def devolver_libro(request, prestamo_id):
    with transaction.atomic():
        prestamo = Prestamo.objects.select_for_update().get(pk=prestamo_id)
        if prestamo.fecha_devolucion is not None:
            raise ValueError("El préstamo ya fue devuelto")

        prestamo.fecha_devolucion = timezone.now()
        prestamo.save(update_fields=["fecha_devolucion"])
        prestamo.libro.disponible = True
        prestamo.libro.save(update_fields=["disponible"])