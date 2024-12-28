from django.test import TestCase, Client
from django.contrib.auth.models import User
from forum.models import Sujet


class ForumFunctionalTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )

        # Créer plusieurs sujets pour tester la pagination
        for i in range(15):
            Sujet.objects.create(
                user=self.user,
                titre=f"Sujet {i + 1}",
                question="Ceci est une question de test",
            )

    def test_forum_page_pagination(self):
        """Test de la pagination sur la page forum"""
        self.client.login(username="testuser", password="password123")
        response = self.client.get("/forum/?page_g=1")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sujet 1")
        self.assertContains(response, "Sujet 5")

        response = self.client.get("/forum/?page_g=2")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sujet 6")
        self.assertContains(response, "Sujet 10")
