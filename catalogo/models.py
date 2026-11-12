from django.db import models

# Create your models here.
class Autor(models.Model):
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=150)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    nacionalidad = models.CharField(max_length=50)
    biografia = models.TextField(blank=True)

    class Meta:
        ordering = ['apellidos', 'nombre']

    def __str__(self):
        return f"{self.nombre} {self.apellidos}"


class Editorial(models.Model):
    nombre = models.CharField(max_length=150, unique=True)
    email = models.EmailField(blank=True)
    sitio_web = models.URLField(blank=True)
    activa = models.BooleanField(default=True)

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
            ordering = ['titulo']
            verbose_name = "Libro"
            verbose_name_plural = "Libros"

    titulo = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True)
    sinopsis = models.TextField(blank=True)
    fecha_publicacion = models.DateField()
    paginas = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    disponible = models.BooleanField(default=True)
    genero = models.CharField(max_length=3, choices=Genero.choices, default=Genero.NOVELA)
    dificultad = models.PositiveSmallIntegerField(choices=Dificultad.choices, default=Dificultad.BASICA)

    def __str__(self):
        return self.titulo