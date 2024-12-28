# tests/test_validation.py
from django.test import TestCase
from django.core.exceptions import ValidationError
from school.models import Matiere, Niveau, Classe, Chapitre, Cours
from datetime import date


class SchoolValidationTest(TestCase):
    def setUp(self):
        self.matiere = Matiere.objects.create(
            nom="SVT", description="Sciences de la vie et de la terre"
        )
        self.niveau = Niveau.objects.create(nom="Troisième")
        self.classe = Classe.objects.create(niveau=self.niveau, numeroClasse=4)

    def test_date_validation(self):
        # Test de validation des dates
        with self.assertRaises(ValidationError):
            chapitre = Chapitre.objects.create(
                classe=self.classe,
                matiere=self.matiere,
                titre="Test",
                date_debut=date(2024, 2, 1),
                date_fin=date(2024, 1, 1),  # Date de fin avant date de début
            )
            chapitre.full_clean()

    def test_duree_validation(self):
        # Test de validation de la durée
        with self.assertRaises(ValidationError):
            chapitre = Chapitre.objects.create(
                classe=self.classe,
                matiere=self.matiere,
                titre="Test",
                duree_en_heure=-1,  # Durée négative
            )
            chapitre.full_clean()

    def test_required_fields(self):
        # Test des champs obligatoires
        with self.assertRaises(ValidationError):
            matiere = Matiere(description="Description sans nom")
            matiere.full_clean()

        with self.assertRaises(ValidationError):
            niveau = Niveau()
            niveau.full_clean()

    def test_unique_constraints(self):
        # Test d'unicité du slug
        matiere1 = Matiere.objects.create(
            nom="Test matière", description="Description 1"
        )

        matiere2 = Matiere.objects.create(
            nom="Test matière", description="Description 2"
        )

        self.assertNotEqual(matiere1.slug, matiere2.slug)
