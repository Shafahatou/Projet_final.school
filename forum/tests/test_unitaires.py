from django.test import TestCase
from django.contrib.auth.models import User
from forum.models import Sujet, Reponse


class SujetModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )

    def test_sujet_creation(self):
        """Test de création d'un sujet avec un slug généré automatiquement"""
        sujet = Sujet.objects.create(
            user=self.user, titre="Test Sujet", question="Ceci est une question de test"
        )
        self.assertEqual(sujet.titre, "Test Sujet")
        self.assertIsNotNone(sujet.slug)
        self.assertIn("test-sujet", sujet.slug)


class ReponseModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.sujet = Sujet.objects.create(
            user=self.user, titre="Test Sujet", question="Ceci est une question de test"
        )

    def test_reponse_creation(self):
        """Test de création d'une réponse avec un slug généré automatiquement"""
        reponse = Reponse.objects.create(
            user=self.user, sujet=self.sujet, reponse="Ceci est une réponse de test"
        )
        self.assertEqual(reponse.reponse, "Ceci est une réponse de test")
        self.assertIsNotNone(reponse.slug)
        self.assertIn("test-sujet", reponse.slug)
