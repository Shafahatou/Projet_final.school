from django.test import TestCase
from django.contrib.auth.models import User
from chat.models import Salon, Message
from school.models import Classe, Niveau


class ChatIntegrationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.niveau = Niveau.objects.create(nom="Terminale")
        self.classe = Classe.objects.create(niveau=self.niveau, numeroClasse=1)
        self.salon = Salon.objects.create(classe=self.classe, nom="Chat Terminale")

    def test_salon_message_relationship(self):
        """Test de la relation entre Salon et Message"""
        message = Message.objects.create(
            auteur=self.user, salon=self.salon, message="Message de test"
        )
        self.assertEqual(self.salon.salon.count(), 1)
        self.assertEqual(self.salon.salon.first().message, "Message de test")
