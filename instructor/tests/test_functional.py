from django.test import TestCase, Client
from django.contrib.auth.models import User
from instructor.models import Instructor
from school.models import Classe


class FunctionalInstructorTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="instructor", password="password123"
        )
        self.classe = Classe.objects.create(numeroClasse=1, niveau_id=1)
        self.instructor = Instructor.objects.create(
            user=self.user,
            contact="123456789",
            adresse="Rue de l'École",
            classe=self.classe,
        )

    def test_profile_page(self):
        """Test de la page profil"""
        self.client.login(username="instructor", password="password123")
        response = self.client.get("/profile/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.instructor.user.username)

    def test_dashboard_page(self):
        """Test de la page dashboard"""
        self.client.login(username="instructor", password="password123")
        response = self.client.get("/dashboard/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Dashboard")
