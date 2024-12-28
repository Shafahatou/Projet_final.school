from django.test import TestCase
from django.contrib.auth.models import User
from chat.models import Salon, Message
from school.models import Classe, Niveau


class ChatValidationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.niveau = Niveau.objects.create(nom="Terminale")
        self.classe = Classe.objects.create(niveau=self.niveau, numeroClasse=1)

    def test_salon_required_fields(self):
        """Test que tous les champs requis pour un Salon sont respectés"""
        with self.assertRaises(Exception):
            Salon.objects.create(classe=None)

    def test_message_required_fields(self):
        """Test que tous les champs requis pour un Message sont respectés"""
        with self.assertRaises(Exception):
            Message.objects.create(auteur=self.user, salon=None, message=None)
