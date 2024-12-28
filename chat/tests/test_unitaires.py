from django.test import TestCase
from django.contrib.auth.models import User
from chat.models import Salon, Message
from school.models import Classe, Niveau


class SalonModelTest(TestCase):
    def setUp(self):
        self.niveau = Niveau.objects.create(nom="Terminale")
        self.classe = Classe.objects.create(niveau=self.niveau, numeroClasse=1)

    def test_salon_creation(self):
        """Test automatique de création d'un Salon lorsqu'une Classe est créée"""
        salon = Salon.objects.get(classe=self.classe)
        self.assertEqual(salon.classe, self.classe)
        self.assertIsNotNone(salon.date_add)


class MessageModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.niveau = Niveau.objects.create(nom="Terminale")
        self.classe = Classe.objects.create(niveau=self.niveau, numeroClasse=1)
        self.salon = Salon.objects.create(classe=self.classe, nom="Chat Terminale")

    def test_message_creation(self):
        """Test de création d'un message dans un Salon"""
        message = Message.objects.create(
            auteur=self.user, salon=self.salon, message="Ceci est un message de test"
        )
        self.assertEqual(message.auteur, self.user)
        self.assertEqual(message.salon, self.salon)
        self.assertEqual(message.message, "Ceci est un message de test")
