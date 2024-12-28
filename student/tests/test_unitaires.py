# tests/test_unit.py

from django.test import TestCase
from django.contrib.auth.models import User
from student.models import Student
from school.models import Classe
from quiz.models import Quiz, Question, Answer


class StudentUnitTests(TestCase):
    """Tests unitaires pour le modèle Student"""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="12345", email="test@test.com"
        )
        self.classe = Classe.objects.create(nom="Classe Test")
        self.student = Student.objects.create(
            user=self.user, classe=self.classe, bio="Test bio", ville="Abobo"
        )

    def test_student_attributes(self):
        """Test les attributs individuels d'un étudiant"""
        self.assertEqual(self.student.user.username, "testuser")
        self.assertEqual(self.student.bio, "Test bio")
        self.assertEqual(self.student.ville, "Abobo")
        self.assertTrue(self.student.status)
        self.assertIsNotNone(self.student.slug)

    def test_student_score_default(self):
        """Test la valeur par défaut du score"""
        self.assertEqual(self.student.score, 0)

    def test_student_str_method(self):
        """Test la méthode __str__"""
        self.assertEqual(str(self.student), "testuser")

    def test_get_u_type_method(self):
        """Test la méthode get_u_type"""
        self.assertTrue(self.student.get_u_type)


class QuizUnitTests(TestCase):
    """Tests unitaires pour les fonctionnalités de quiz"""

    def setUp(self):
        self.classe = Classe.objects.create(nom="Classe Test")
        self.quiz = Quiz.objects.create(
            titre="Test Quiz", classe=self.classe, status=True
        )
        self.question = Question.objects.create(quiz=self.quiz, text="Question test")

    def test_quiz_creation(self):
        """Test la création d'un quiz"""
        self.assertEqual(self.quiz.titre, "Test Quiz")
        self.assertTrue(self.quiz.status)

    def test_question_creation(self):
        """Test la création d'une question"""
        self.assertEqual(self.question.text, "Question test")
        self.assertEqual(self.question.quiz, self.quiz)


class AnswerUnitTests(TestCase):
    """Tests unitaires pour les réponses"""

    def setUp(self):
        self.classe = Classe.objects.create(nom="Classe Test")
        self.quiz = Quiz.objects.create(titre="Test Quiz", classe=self.classe)
        self.question = Question.objects.create(quiz=self.quiz, text="Question test")
        self.answer = Answer.objects.create(
            question=self.question, text="Réponse test", is_correct=True
        )

    def test_answer_creation(self):
        """Test la création d'une réponse"""
        self.assertEqual(self.answer.text, "Réponse test")
        self.assertTrue(self.answer.is_correct)
        self.assertEqual(self.answer.question, self.question)
