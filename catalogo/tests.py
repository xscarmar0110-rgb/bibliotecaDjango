from django.test import TestCase
from django.db import transaction
from django.contrib.auth.models import User
from .models import Libro, Prestamo
from .servicios import prestar_libro, devolver_libro


class PrestamoTests(TestCase):
    def setUp(self):
        self.usuario = User.objects.create_user(username = "lector", password = "prueba")
        self.libro = Libro.objects.create(
            titulo = "Libro de prueba",
            isbn = "0000000000001",
            fecha_publicacion = "2020-01-01",
            paginas = 100,
            precio = 10,
        )

    def test_prestar_libro(self):
        prestar_libro(self.libro.id, self.usuario)
        self.libro.refresh_from_db()
        self.assertFalse(self.libro.disponible)

    def test_no_prestar_libro_no_disponible(self):
        prestar_libro(self.libro.id, self.usuario)
        with self.assertRaises(ValueError):
            prestar_libro(self.libro.id, self.usuario)

    def test_devolver_libro(self):
        prestamo = prestar_libro(self.libro.id, self.usuario)
        devolver_libro(prestamo.id)
        self.libro.refresh_from_db()
        self.assertTrue(self.libro.disponible)

    def test_no_devolver_dos_veces(self):
        prestamo = prestar_libro(self.libro.id, self.usuario)
        devolver_libro(prestamo.id)
        with self.assertRaises(ValueError):
            devolver_libro(prestamo.id)

    def test_rollback(self):
        try:
            with transaction.atomic():
                Prestamo.objects.create(
                    libro = self.libro,
                    usuario = self.usuario,
                )
                raise RuntimeError("Error para probar el rollback")
        except RuntimeError:
            pass

        self.assertEqual(Prestamo.objects.count(), 0)
