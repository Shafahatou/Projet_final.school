# tests/test_validation.py

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from student.models import Student
from school.models import Classe
from quiz.models import Quiz, Question, Answer
import os


class StudentValidationTests(TestCase):
    """Tests de validation vérifiant que le système respecte les exigences"""

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.classe = Classe.objects.create(nom="Classe Test")

    def test_photo_upload_validation(self):
        """Test la validation des photos de profil"""
        # Créer un faux fichier image
        image_path = os.path.join(os.path.dirname(__file__), "test_files", "test.jpg")
        with open(image_path, "rb") as image_file:
            photo = SimpleUploadedFile(
                name="test.jpg", content=image_file.read(), content_type="image/jpeg"
            )

        # Tester avec une image valide
        student = Student.objects.create(
            user=self.user, classe=self.classe, photo=photo
        )
        self.assertTrue(student.photo)

        # Nettoyer
        os.remove(student.photo.path)

    def test_quiz_score_validation(self):
        """Test la validation des scores de quiz"""
        student = Student.objects.create(user=self.user, classe=self.classe)
        quiz = Quiz.objects.create(titre="Test Quiz", classe=self.classe)

        # Test score négatif
        with self.assertRaises(ValidationError):
            student.score = -1
            student.full_clean()

        # Test score valide
        student.score = 100
        student.full_clean()  # Ne devrait pas lever d'exception

    def test_business_rules_validation(self):
        """Test la validation des règles métier"""
        student = Student.objects.create(user=self.user, classe=self.classe)
        quiz = Quiz.objects.create(titre="Test Quiz", classe=self.classe)

        # Un étudiant ne peut pas prendre un quiz d'une autre classe
        autre_classe = Classe.objects.create(nom="Autre Classe")
        quiz_autre_classe = Quiz.objects.create(
            titre="Quiz Autre Classe", classe=autre_classe
        )

        # Vérifier que l'étudiant ne peut voir que les quiz de sa classe
        quiz_accessibles = Quiz.objects.filter(classe=student.classe)
        self.assertIn(quiz, quiz_accessibles)
        self.assertNotIn(quiz_autre_classe, quiz_accessibles)

    def test_data_integrity_validation(self):
        """Test la validation de l'intégrité des données"""
        student = Student.objects.create(user=self.user, classe=self.classe)

        # Test unicité du slug
        student2 = Student.objects.create(
            user=User.objects.create_user(username="testuser2", password="12345"),
            classe=self.classe,
        )
        self.assertNotEqual(student.slug, student2.slug)

        # Test contraintes de longueur
        with self.assertRaises(ValidationError):
            student.ville = "a" * 256  # Dépasse la longueur max
            student.full_clean()
