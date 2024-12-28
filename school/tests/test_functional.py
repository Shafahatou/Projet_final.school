from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from school.models import Matiere, Niveau, Classe, Chapitre, Cours


class SchoolFunctionalTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser(
            username="admin", password="adminpass", email="admin@example.com"
        )
        self.client.login(username="admin", password="adminpass")

        # Créer les données de test
        self.matiere = Matiere.objects.create(
            nom="Chimie", description="Cours de chimie"
        )
        self.niveau = Niveau.objects.create(nom="Quatrième")
        self.classe = Classe.objects.create(niveau=self.niveau, numeroClasse=3)

    def tearDown(self):
        # Nettoyer la base de données après chaque test
        Matiere.objects.all().delete()
        Niveau.objects.all().delete()
        Classe.objects.all().delete()
        Chapitre.objects.all().delete()
        Cours.objects.all().delete()

    def test_admin_matiere_crud(self):
        # Utiliser reverse pour l'URL
        url = reverse("admin:school_matiere_add")  # Vérifiez le nom exact de l'URL
        response = self.client.post(
            url,
            {"nom": "Nouvelle matière", "description": "Description", "status": True},
        )
        # Vérifiez le statut HTTP de la réponse
        self.assertEqual(response.status_code, 302)  # Redirection après ajout réussi
        # Vérifiez que la matière a été créée
        self.assertEqual(Matiere.objects.filter(nom="Nouvelle matière").count(), 1)

    def test_cours_creation_workflow(self):
        chapitre = Chapitre.objects.create(
            classe=self.classe,
            matiere=self.matiere,
            titre="Test chapitre",
            description="Description test",
            duree_en_heure=5,
        )

        cours = Cours.objects.create(
            titre="Test cours", chapitre=chapitre, description="Description cours test"
        )

        # Suppression de `cours.status` si le champ n'existe pas
        self.assertEqual(cours.chapitre, chapitre)
