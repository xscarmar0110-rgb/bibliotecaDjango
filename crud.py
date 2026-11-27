from datetime import date
from catalogo.models import Editorial, Autor, Libro

editorial = Editorial.objects.create(nombre = "Editorial Prueba", email = "info@prueba.test")
autor1 = Autor.objects.create(nombre = "Ana", apellidos = "Ruiz", nacionalidad = "Española")
autor2 = Autor.objects.create(nombre = "Luis", apellidos = "Mora", nacionalidad = "Española")
print(editorial, autor1, autor2)

libro1 = Libro.objects.create(titulo = "Libro Uno", isbn = "1110000000001", precio = 15, paginas = 120, fecha_publicacion = date(2020, 1, 1), editorial = editorial)
libro2 = Libro.objects.create(titulo = "Libro Dos", isbn = "1110000000002", precio = 20, paginas = 200, fecha_publicacion = date(2021, 1, 1), editorial = editorial)
libro3 = Libro.objects.create(titulo = "Libro Tres", isbn = "1110000000003", precio = 9.50, paginas = 90, fecha_publicacion = date(2022, 1, 1), editorial = editorial)

libro1.autores.add(autor1)
libro2.autores.add(autor1, autor2)
libro3.autores.add(autor2)
print(libro1, libro2, libro3)

libro = Libro.objects.get(isbn = "1110000000002")
print(libro)

libro.precio = 18.50
libro.save()
print(Libro.objects.get(isbn = "1110000000002").precio)

print(libro3.prestamos.exists())
print(libro3.delete())
