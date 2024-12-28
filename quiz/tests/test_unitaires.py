from django.test import TestCase
from quiz.models import Subject, Quiz, Question, Answer


class SubjectModelTest(TestCase):
    def test_subject_creation(self):
        """Test création d'un Subject avec ses attributs"""
        subject = Subject.objects.create(name="Mathématiques", color="#ff0000")
        self.assertEqual(subject.name, "Mathématiques")
        self.assertEqual(subject.color, "#ff0000")
        self.assertEqual(str(subject), "Mathématiques")

    def test_get_html_badge(self):
        """Test de la méthode get_html_badge"""
        subject = Subject.objects.create(name="Mathématiques", color="#ff0000")
        expected_html = '<span class="badge badge-primary" style="background-color: #ff0000">Mathématiques</span>'
        self.assertEqual(subject.get_html_badge(), expected_html)


class QuizModelTest(TestCase):
    def test_quiz_creation(self):
        """Test de création d'un Quiz"""
        quiz = Quiz.objects.create(
            name="Quiz sur les fractions",
            owner_id=1,
            subject_id=1,
            classe_id=1,
            cours_id=1,
        )
        self.assertEqual(quiz.name, "Quiz sur les fractions")
        self.assertTrue(quiz.status)
