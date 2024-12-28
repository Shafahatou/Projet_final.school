from django.test import TestCase, Client
from django.contrib.auth.models import User
from chat.models import Salon, Message
from school.models import Classe, Niveau


class ChatFunctionalTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.niveau = Niveau.objects.create(nom="Terminale")
        self.classe = Classe.objects.create(niveau=self.niveau, numeroClasse=1)
        self.salon = Salon.objects.create(classe=self.classe, nom="Chat Terminale")

    def test_access_salon(self):
        """Test que l'utilisateur peut accéder au salon"""
        self.client.login(username="testuser", password="password123")
        response = self.client.get(
            f"/chat/{self.salon.id}/"
        )  # Remplacez par la route correcte
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.salon.nom)

    def test_send_message(self):
        """Test de l'envoi d'un message dans un Salon"""
        self.client.login(username="testuser", password="password123")
        response = self.client.post(
            f"/chat/{self.salon.id}/send/", {"message": "Ceci est un message de test"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            Message.objects.filter(message="Ceci est un message de test").exists()
        )
