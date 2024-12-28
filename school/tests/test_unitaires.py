# tests/test_unit.py
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from school.models import Matiere, Niveau, Classe, Chapitre, Cours
from datetime import datetime, date
import os


class MatiereModelTest(TestCase):
    def setUp(self):
        self.matiere = Matiere.objects.create(
            nom="Mathématiques", description="Description des mathématiques"
        )

    def test_matiere_creation(self):
        self.assertEqual(self.matiere.nom, "Mathématiques")
        self.assertTrue(self.matiere.status)
        self.assertIsNotNone(self.matiere.slug)

    def test_matiere_slug_generation(self):
        self.assertTrue(self.matiere.slug.startswith("mathematiques-"))

    def test_str_representation(self):
        self.assertEqual(str(self.matiere), "Mathématiques")


class NiveauModelTest(TestCase):
    def setUp(self):
        self.niveau = Niveau.objects.create(nom="Sixième")

    def test_niveau_creation(self):
        self.assertEqual(self.niveau.nom, "Sixième")
        self.assertTrue(self.niveau.status)
        self.assertIsNotNone(self.niveau.slug)

    def test_str_representation(self):
        self.assertEqual(str(self.niveau), "Sixième")


class ClasseModelTest(TestCase):
    def setUp(self):
        self.niveau = Niveau.objects.create(nom="Sixième")
        self.classe = Classe.objects.create(niveau=self.niveau, numeroClasse=1)

    def test_classe_creation(self):
        self.assertEqual(self.classe.numeroClasse, 1)
        self.assertEqual(self.classe.niveau, self.niveau)
        self.assertTrue(self.classe.status)

    def test_str_representation(self):
        self.assertEqual(str(self.classe), "Sixième 1")
