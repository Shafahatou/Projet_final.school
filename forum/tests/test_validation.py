from django.test import TestCase
from django.contrib.auth.models import User
from forum.models import Sujet, Reponse


class ForumValidationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.sujet = Sujet.objects.create(
            user=self.user, titre="Test Sujet", question="Ceci est une question de test"
        )

    def test_sujet_unique_slug(self):
        """Test que le slug est unique pour chaque sujet"""
        Sujet.objects.create(
            user=self.user, titre="Test Sujet", question="Une autre question"
        )
        with self.assertRaises(Exception):
            Sujet.objects.create(
                user=self.user, titre="Test Sujet", question="Encore une autre question"
            )

    def test_reponse_required_fields(self):
        """Test que tous les champs requis de Reponse doivent être fournis"""
        with self.assertRaises(Exception):
            Reponse.objects.create(user=self.user, sujet=None, reponse=None)
