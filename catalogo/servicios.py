from django.db import transaction
from django.db.models import Avg, Count
from django.utils import timezone
from .models import Libro, Prestamo, Editorial

def libros_disponibles():
    return Libro.objects.filter(disponible=True).order_by("titulo")

def buscar(texto):
    return Libro.objects.filter(titulo__icontains=texto)

def libros_de_editorial(nombre):
    return Libro.objects.filter(editorial__nombre=nombre)

def libros_de_autor(autor):
    return autor.libros.all()

def precio_medio():
    return Libro.objects.aggregate(media=Avg("precio"))

def libros_por_editorial():
    return Editorial.objects.annotate(n=Count("libros"))

def prestamos_activos():
    return Prestamo.objects.filter(fecha_devolucion__isnull=True)


def prestar_libro(libro_id, usuario):
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


def devolver_libro(prestamo_id):
    with transaction.atomic():
        prestamo = Prestamo.objects.select_for_update().get(pk=prestamo_id)
        if prestamo.fecha_devolucion is not None:
            raise ValueError("El préstamo ya fue devuelto")

        prestamo.fecha_devolucion = timezone.now()
        prestamo.save(update_fields=["fecha_devolucion"])
        prestamo.libro.disponible = True
        prestamo.libro.save(update_fields=["disponible"])
        return prestamo
