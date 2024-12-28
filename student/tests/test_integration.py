# tests/test_integration.py

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from student.models import Student
from school.models import Classe
from quiz.models import Quiz, Question, Answer, TakenQuiz
from forum.models import Sujet, Reponse


class StudentIntegrationTests(TestCase):
    """Tests d'intégration pour les interactions entre composants"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.classe = Classe.objects.create(nom="Classe Test")
        self.student = Student.objects.create(user=self.user, classe=self.classe)
        self.quiz = Quiz.objects.create(
            titre="Test Quiz", classe=self.classe, status=True
        )

    def test_quiz_workflow(self):
        """Test l'intégration complète du workflow d'un quiz"""
        self.client.login(username="testuser", password="12345")

        # Création d'une question et réponses
        question = Question.objects.create(quiz=self.quiz, text="Test Question")
        answer1 = Answer.objects.create(
            question=question, text="Correct", is_correct=True
        )
        answer2 = Answer.objects.create(
            question=question, text="Incorrect", is_correct=False
        )

        # Accès à la page du quiz
        response = self.client.get(reverse("take_quiz", kwargs={"pk": self.quiz.pk}))
        self.assertEqual(response.status_code, 200)

        # Soumission d'une réponse
        response = self.client.post(
            reverse("take_quiz", kwargs={"pk": self.quiz.pk}),
            {str(question.id): answer1.id},
        )

        # Vérification du résultat
        taken_quiz = TakenQuiz.objects.filter(
            student=self.student, quiz=self.quiz
        ).first()
        self.assertIsNotNone(taken_quiz)
        self.assertEqual(taken_quiz.score, 1)

    def test_forum_integration(self):
        """Test l'intégration du forum avec le système d'étudiants"""
        self.client.login(username="testuser", password="12345")

        # Création d'un sujet
        sujet = Sujet.objects.create(
            titre="Test Sujet", question="Test Question", user=self.user
        )

        # Création d'une réponse
        response = self.client.post(
            reverse("post_forum_reponse", kwargs={"slug": sujet.slug}),
            {"reponse": "Test Réponse"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Reponse.objects.filter(sujet=sujet, user=self.user).exists())

    def test_profile_update_integration(self):
        """Test l'intégration de la mise à jour de profil"""
        self.client.login(username="testuser", password="12345")

        # Test de mise à jour du profil
        update_data = {
            "nom": "Nouveau Nom",
            "prenom": "Nouveau Prenom",
            "email": "nouveau@email.com",
            "bio": "Nouvelle bio",
        }

        response = self.client.post(reverse("update_profil"), update_data)
        self.assertEqual(response.status_code, 200)

        # Vérification des mises à jour
        self.user.refresh_from_db()
        self.student.refresh_from_db()
        self.assertEqual(self.user.last_name, "Nouveau Nom")
        self.assertEqual(self.user.email, "nouveau@email.com")
