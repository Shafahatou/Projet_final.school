from django.test import TestCase
from quiz.models import TakenQuiz
from django.core.exceptions import ValidationError


class ValidationTest(TestCase):
    def test_taken_quiz_score_validation(self):
        """Test que le score et le pourcentage respectent les contraintes"""
        with self.assertRaises(ValidationError):
            TakenQuiz.objects.create(student_id=1, quiz_id=1, score=-10, percentage=150)

    def test_unique_constraint(self):
        """Test de la contrainte UNIQUE"""
        TakenQuiz.objects.create(student_id=1, quiz_id=1, score=80, percentage=80.0)
        with self.assertRaises(ValidationError):
            TakenQuiz.objects.create(student_id=1, quiz_id=1, score=90, percentage=90.0)
