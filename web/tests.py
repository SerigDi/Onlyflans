from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import ContactForm, Flan


def crear_flan(nombre, slug, privado=False, precio=3000):
    return Flan.objects.create(
        flan_uuid="ab3d2b55-09e1-4679-9dd1-e7a421f89c6b" if not privado else "867d6b60-6cc0-4fb0-b08a-61ff496a013b",
        name=nombre,
        description="Descripción de prueba",
        image_url="https://example.com/flan.jpg",
        slug=slug,
        is_private=privado,
        price=precio,
    )


class VistasPublicasTests(TestCase):
    def setUp(self):
        crear_flan("Flan Clásico", "flan-clasico")
        crear_flan("Flan Secreto", "flan-secreto", privado=True)

    def test_index_muestra_solo_flanes_publicos(self):
        resp = self.client.get(reverse("index"))
        self.assertContains(resp, "Flan Clásico")
        self.assertNotContains(resp, "Flan Secreto")

    def test_detalle_por_slug(self):
        resp = self.client.get(reverse("flan_detalle", args=["flan-clasico"]))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Flan Clásico")

    def test_detalle_inexistente_da_404(self):
        resp = self.client.get(reverse("flan_detalle", args=["no-existe"]))
        self.assertEqual(resp.status_code, 404)


class AutenticacionTests(TestCase):
    def setUp(self):
        crear_flan("Flan Secreto", "flan-secreto", privado=True)
        self.user = User.objects.create_user("demo", password="clave-de-prueba-123")

    def test_bienvenido_requiere_login(self):
        resp = self.client.get(reverse("welcome"))
        self.assertEqual(resp.status_code, 302)
        self.assertIn("/accounts/login", resp["Location"])

    def test_bienvenido_con_login_muestra_flanes_privados(self):
        self.client.login(username="demo", password="clave-de-prueba-123")
        resp = self.client.get(reverse("welcome"))
        self.assertContains(resp, "Flan Secreto")


class ContactoTests(TestCase):
    def test_formulario_valido_crea_registro_y_redirige(self):
        resp = self.client.post(reverse("contacto"), {
            "customer_email": "cliente@example.com",
            "customer_name": "Cliente",
            "message": "Hola",
        })
        self.assertRedirects(resp, "/exito")
        self.assertEqual(ContactForm.objects.count(), 1)

    def test_formulario_invalido_no_crea_registro(self):
        self.client.post(reverse("contacto"), {"customer_email": "no-es-correo", "customer_name": "", "message": ""})
        self.assertEqual(ContactForm.objects.count(), 0)
