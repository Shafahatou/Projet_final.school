# tests/test_integration.py
from django.test import TestCase
from school.models import Matiere, Niveau, Classe, Chapitre, Cours
from datetime import date


class SchoolIntegrationTest(TestCase):
    def setUp(self):
        # Créer les objets nécessaires
        self.matiere = Matiere.objects.create(
            nom="Physique", description="Cours de physique"
        )

        self.niveau = Niveau.objects.create(nom="Cinquième")

        self.classe = Classe.objects.create(niveau=self.niveau, numeroClasse=2)

        self.chapitre = Chapitre.objects.create(
            classe=self.classe,
            matiere=self.matiere,
            titre="Mécanique",
            description="Chapitre sur la mécanique",
            date_debut=date(2024, 1, 1),
            date_fin=date(2024, 2, 1),
            duree_en_heure=10,
        )

    def test_course_hierarchy(self):
        # Créer un cours
        cours = Cours.objects.create(
            titre="Les forces", chapitre=self.chapitre, description="Étude des forces"
        )

        # Vérifier les relations
        self.assertEqual(cours.chapitre.matiere, self.matiere)
        self.assertEqual(cours.chapitre.classe.niveau, self.niveau)
        self.assertEqual(cours.chapitre.classe.numeroClasse, 2)

    def test_related_queries(self):
        # Tester les requêtes avec related_name
        chapitres_matiere = self.matiere.matiere_chapitre.all()
        self.assertIn(self.chapitre, chapitres_matiere)

        chapitres_classe = self.classe.classe_chapitre.all()
        self.assertIn(self.chapitre, chapitres_classe)
