from django.test import TestCase
from django.contrib.auth.models import User
from instructor.models import Instructor
from school.models import Classe


class InstructorModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="instructor", password="password123"
        )
        self.classe = Classe.objects.create(numeroClasse=1, niveau_id=1)

    def test_instructor_creation(self):
        """Test de création d'un instructeur"""
        instructor = Instructor.objects.create(
            user=self.user,
            contact="123456789",
            adresse="Rue de l'École",
            classe=self.classe,
        )
        self.assertEqual(instructor.user.username, "instructor")
        self.assertEqual(instructor.contact, "123456789")
        self.assertEqual(instructor.classe, self.classe)

    def test_instructor_slug(self):
        """Test de génération automatique du slug"""
        instructor = Instructor.objects.create(
            user=self.user,
            contact="123456789",
            adresse="Rue de l'École",
            classe=self.classe,
        )
        self.assertIsNotNone(instructor.slug)
        self.assertIn("instructor", instructor.slug)
