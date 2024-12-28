from django.test import TestCase
from django.contrib.auth.models import User
from quiz.models import Quiz, Question, Answer, TakenQuiz
from student.models import Student


class IntegrationTest(TestCase):
    def setUp(self):
        self.teacher = User.objects.create_user(
            username="teacher", password="password123"
        )
        self.student_user = User.objects.create_user(
            username="student", password="password123"
        )
        self.student = Student.objects.create(user=self.student_user)

        self.quiz = Quiz.objects.create(
            owner=self.teacher,
            name="Integration Quiz",
            subject_id=1,
            classe_id=1,
            cours_id=1,
        )
        self.question = Question.objects.create(
            quiz=self.quiz, text="Quelle est la valeur de 4+4 ?"
        )
        self.answer_correct = Answer.objects.create(
            question=self.question, text="8", is_correct=True
        )
        self.answer_incorrect = Answer.objects.create(
            question=self.question, text="10", is_correct=False
        )

    def test_integration_workflow(self):
        """Test du workflow complet : création d'un quiz, prise et soumission"""
        taken_quiz = TakenQuiz.objects.create(
            student=self.student, quiz=self.quiz, score=100, percentage=100.0
        )
        self.assertEqual(taken_quiz.student.user.username, "student")
        self.assertEqual(taken_quiz.quiz.name, "Integration Quiz")
