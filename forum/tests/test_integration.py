from django.test import TestCase
from django.contrib.auth.models import User
from forum.models import Sujet, Reponse


class ForumIntegrationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.sujet = Sujet.objects.create(
            user=self.user, titre="Test Sujet", question="Ceci est une question de test"
        )

    def test_sujet_and_reponse_relationship(self):
        """Test de la relation entre Sujet et Reponse"""
        reponse = Reponse.objects.create(
            user=self.user, sujet=self.sujet, reponse="Ceci est une réponse de test"
        )
        self.assertEqual(self.sujet.sujet_reponse.count(), 1)
        self.assertEqual(
            self.sujet.sujet_reponse.first().reponse, "Ceci est une réponse de test"
        )
