from django.test import TestCase, Client
from django.contrib.auth.models import User
from instructor.models import Instructor
from school.models import Classe, Chapitre


class IntegrationInstructorTest(TestCase):
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
        self.chapitre = Chapitre.objects.create(
            titre="Chapitre 1",
            description="Introduction",
            classe=self.classe,
            duree_en_heure=10,
        )

    def test_courses_page(self):
        """Test de la liste des chapitres pour un instructeur"""
        self.client.login(username="instructor", password="password123")
        response = self.client.get("/courses/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.chapitre.titre)
