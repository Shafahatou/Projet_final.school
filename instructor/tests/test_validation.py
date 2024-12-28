from django.test import TestCase
from django.contrib.auth.models import User
from instructor.models import Instructor
from school.models import Classe


class ValidationInstructorTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="instructor", password="password123"
        )
        self.classe = Classe.objects.create(numeroClasse=1, niveau_id=1)

    def test_unique_slug(self):
        """Test que le slug est unique pour chaque instructeur"""
        Instructor.objects.create(
            user=self.user,
            contact="123456789",
            adresse="Rue de l'École",
            classe=self.classe,
        )
        with self.assertRaises(Exception):
            Instructor.objects.create(
                user=self.user,
                contact="987654321",
                adresse="Autre Rue",
                classe=self.classe,
            )
