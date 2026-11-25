from django.db import models
from django.conf import settings
from django.db.models import Q

# Create your models here.
class Autor(models.Model):
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=150)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    nacionalidad = models.CharField(max_length=50)
    biografia = models.TextField(blank=True)

    class Meta:
        ordering = ['apellidos', 'nombre']
        verbose_name = "Autor"
        verbose_name_plural = "Autores"

    def __str__(self):
        return f"{self.nombre} {self.apellidos}"


class Editorial(models.Model):
    nombre = models.CharField(max_length=150, unique=True)
    email = models.EmailField(blank=True)
    sitio_web = models.URLField(blank=True)
    activa = models.BooleanField(default=True)

    class Meta:
            ordering = ['nombre']
            verbose_name = "Editorial"
            verbose_name_plural = "Editoriales"

    def __str__(self):
        return self.nombre


class Libro(models.Model):
    class Genero(models.TextChoices):
        NOVELA = "NOV", "Novela"
        POESIA = "POE", "Poesía"
        TEATRO = "TEA", "Teatro"
        ENSAYO = "ENS", "Ensayo"
        COMIC = "COM", "Cómic"

    class Dificultad(models.IntegerChoices):
        BASICA = 1, "Básica"
        INTERMEDIA = 2, "Intermedia"
        AVANZADA = 3, "Avanzada"


    class Meta:
        ordering = ["titulo"]
        constraints = [
            models.CheckConstraint(
            condition=Q(precio__gte=0),
            name="libro_precio_no_negativo",
            ),
        ]

    titulo = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True)
    sinopsis = models.TextField(blank=True)
    fecha_publicacion = models.DateField()
    paginas = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    disponible = models.BooleanField(default=True)
    genero = models.CharField(max_length=3, choices=Genero.choices, default=Genero.NOVELA)
    dificultad = models.PositiveSmallIntegerField(choices=Dificultad.choices, default=Dificultad.BASICA)
    # El related names hace que en este caso desde la editorial pueda acceder a los datos del libro 
    editorial = models.ForeignKey("Editorial", on_delete=models.PROTECT, related_name='libros', null=True, blank=True)
    autores = models.ManyToManyField("Autor", related_name='libros', blank=True)

    def __str__(self):
        return self.titulo


class Participacion(models.Model):

    class Funcion(models.TextChoices):
        PRINCIPAL = "PRI", "Autor principal"
        COAUTOR = "COA", "Coautor"
        COLABORADOR = "COL", "Colaborador"
     
    libro = models.ForeignKey("Libro", on_delete=models.CASCADE, related_name="participaciones")
    autor = models.ForeignKey("Autor", on_delete=models.CASCADE, related_name="participaciones")
    funcion = models.CharField(max_length=3, choices=Funcion.choices, default=Funcion.COAUTOR)
    fecha_incorporacion = models.DateField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["libro", "autor"], name="participacion_unica_libro_autor"
            )
        ]

    def __str__(self):
        return f"{self.autor} - {self.libro} ({self.get_funcion_display()})"


class Prestamo(models.Model):
    libro = models.ForeignKey(
        "Libro", on_delete=models.PROTECT,
        related_name="prestamos"
    )
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="prestamos_biblioteca"
    )
    fecha_prestamo = models.DateTimeField(auto_now_add=True)
    fecha_devolucion = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Préstamo {self.pk}: {self.libro}"
# Practica, hosting gratuito para subir mi codigo 

# El codigo de biblioteca a github y subir todos los cambios al hosting gratuito