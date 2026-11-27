# Evidencias: CRUD, consultas ORM, préstamos y rollback

Salida real de `python manage.py shell` usando las funciones de `catalogo/servicios.py`
(los datos de ejemplo se crearon dentro de una transacción que se deshizo al final).

```text

## CRUD
>>> Editorial.objects.create(nombre="Editorial Demo", ...); Autor.objects.create(...) x2
Editorial Demo | Ana Ruiz | Luis Mora

>>> Libro.objects.create(...) x3; l1.autores.add(a1); l2.autores.add(a1, a2); l3.autores.add(a2)
[('Demo Uno', ['Ana Ruiz']), ('Demo Dos', ['Luis Mora', 'Ana Ruiz']), ('Demo Tres', ['Luis Mora'])]

>>> Libro.objects.get(isbn="9990000000002")
Demo Dos

>>> l2.precio = Decimal("18.50"); l2.save(); Libro.objects.get(pk=l2.pk).precio
18.50

>>> l3.prestamos.exists(); l3.delete()
False -> (2, {'catalogo.Libro_autores': 1, 'catalogo.Libro': 1})

## Consultas ORM
>>> libros_disponibles()
['Demo Dos', 'Demo Uno', 'Java', 'Python', 'Samu']

>>> buscar("demo")
['Demo Dos', 'Demo Uno']

>>> libros_de_editorial("Editorial Demo")
['Demo Dos', 'Demo Uno']

>>> libros_de_autor(a2)
['Demo Dos']

>>> precio_medio()
{'media': Decimal('31.7000000000000')}

>>> libros_por_editorial()
[('Dirusette', 3), ('Editorial Demo', 2), ('JI', 0)]

## Préstamos
>>> p = prestar_libro(l1.id, u); l1.disponible
Préstamo 1: Demo Uno | disponible=False

>>> prestamos_activos()
[<Prestamo: Préstamo 1: Demo Uno>]

>>> prestar_libro(l1.id, u)  # otra vez
ValueError: El libro no esta disponible

>>> devolver_libro(p.id); l1.disponible
disponible=True

>>> devolver_libro(p.id)  # otra vez
ValueError: El préstamo ya fue devuelto

## Rollback
>>> with transaction.atomic(): Prestamo.objects.create(...); raise RuntimeError  -> count antes/después
1 / 1

```

## Tests (`python manage.py test catalogo`)

```text
Found 5 test(s).
System check identified no issues (0 silenced).
Creating test database for alias 'default'...
.....
----------------------------------------------------------------------
Ran 5 tests in 2.355s

OK
Destroying test database for alias 'default'...
```
