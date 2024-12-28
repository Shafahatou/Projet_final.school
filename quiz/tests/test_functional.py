from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from quiz.models import Subject, Quiz, Question, Answer, TakenQuiz
from student.models import Student
from school.models import Classe, Cours, Chapitre


class FunctionalQuizTest(TestCase):
    def setUp(self):
        self.client = Client()

        # Créer un enseignant
        self.teacher = User.objects.create_user(
            username="teacher", password="password123"
        )

        # Créer un étudiant
        self.student_user = User.objects.create_user(
            username="student", password="password123"
        )
        self.student = Student.objects.create(user=self.student_user)

        # Créer un sujet
        self.subject = Subject.objects.create(name="Mathématiques", color="#ff0000")

        # Créer une classe
        self.classe = Classe.objects.create(numeroClasse=1, niveau_id=1)

        # Créer un chapitre
        self.chapitre = Chapitre.objects.create(
            classe=self.classe,
            titre="Chapitre 1",
            description="Introduction",
            duree_en_heure=10,
        )

        # Créer un cours lié au chapitre
        self.cours = Cours.objects.create(
            titre="Algèbre", chapitre=self.chapitre, description="Cours d'algèbre"
        )

    def test_create_quiz(self):
        """Test qu'un enseignant peut créer un quiz et des questions"""
        self.client.login(username="teacher", password="password123")

        # Créer un quiz
        quiz = Quiz.objects.create(
            owner=self.teacher,
            name="Quiz Math",
            subject=self.subject,
            classe=self.classe,
            cours=self.cours,
        )

        # Ajouter une question et une réponse
        question = Question.objects.create(
            quiz=quiz, text="Quelle est la valeur de 2+2 ?"
        )
        Answer.objects.create(question=question, text="4", is_correct=True)

        # Vérifier l'accès au détail du quiz
        url = reverse(
            "quiz_detail", args=[quiz.id]
        )  # Remplacez "quiz_detail" par le nom exact de votre route
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_take_quiz(self):
        """Test qu'un étudiant peut prendre un quiz et soumettre des réponses"""
        self.client.login(username="student", password="password123")

        # Créer un quiz
        quiz = Quiz.objects.create(
            owner=self.teacher,
            name="Quiz Science",
            subject=self.subject,
            classe=self.classe,
            cours=self.cours,
        )

        # Ajouter une question et une réponse correcte
        question = Question.objects.create(
            quiz=quiz, text="Quelle est la valeur de 3+3 ?"
        )
        answer = Answer.objects.create(question=question, text="6", is_correct=True)

        # Soumettre le quiz
        url = reverse(
            "quiz_submit", args=[quiz.id]
        )  # Remplacez "quiz_submit" par le nom exact de votre route
        response = self.client.post(url, {"answers": [answer.id]})
        self.assertEqual(response.status_code, 200)

        # Vérifier que le quiz est enregistré comme complété
        self.assertTrue(
            TakenQuiz.objects.filter(student=self.student, quiz=quiz).exists()
        )
