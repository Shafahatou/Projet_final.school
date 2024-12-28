# tests/test_functional.py

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.contrib.auth.models import User
from student.models import Student
from school.models import Classe
import time


class StudentFunctionalTests(LiveServerTestCase):
    """Tests fonctionnels utilisant Selenium pour tester l'interface utilisateur"""

    def setUp(self):
        self.driver = webdriver.Firefox()  # ou Chrome()
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.classe = Classe.objects.create(nom="Classe Test")
        self.student = Student.objects.create(user=self.user, classe=self.classe)

    def tearDown(self):
        self.driver.quit()

    def test_student_login(self):
        """Test le processus de connexion complet"""
        self.driver.get(f"{self.live_server_url}/login/")

        # Remplir le formulaire de connexion
        username_input = self.driver.find_element(By.NAME, "username")
        password_input = self.driver.find_element(By.NAME, "password")
        username_input.send_keys("testuser")
        password_input.send_keys("12345")

        # Soumettre le formulaire
        submit_button = self.driver.find_element(
            By.CSS_SELECTOR, 'input[type="submit"]'
        )
        submit_button.click()

        # Vérifier la redirection
        WebDriverWait(self.driver, 10).until(
            EC.url_to_be(f"{self.live_server_url}/dashboard/")
        )

    def test_take_quiz(self):
        """Test le processus complet de participation à un quiz"""
        # Login d'abord
        self.client.login(username="testuser", password="12345")
        cookie = self.client.cookies["sessionid"]
        self.driver.get(f"{self.live_server_url}/")
        self.driver.add_cookie(
            {"name": "sessionid", "value": cookie.value, "secure": False, "path": "/"}
        )

        # Aller à la page de quiz
        self.driver.get(f"{self.live_server_url}/quiz/1/")

        # Répondre aux questions
        answer_radio = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "answer"))
        )
        answer_radio.click()

        # Soumettre le quiz
        submit_button = self.driver.find_element(
            By.CSS_SELECTOR, 'button[type="submit"]'
        )
        submit_button.click()

        # Vérifier les résultats
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "quiz-results"))
        )

    def test_update_profile(self):
        """Test la mise à jour du profil via l'interface utilisateur"""
        # Login
        self.client.login(username="testuser", password="12345")
        cookie = self.client.cookies["sessionid"]
        self.driver.get(f"{self.live_server_url}/")
        self.driver.add_cookie(
            {"name": "sessionid", "value": cookie.value, "secure": False, "path": "/"}
        )

        # Aller à la page de profil
        self.driver.get(f"{self.live_server_url}/profile/edit/")

        # Mettre à jour les informations
        bio_input = self.driver.find_element(By.NAME, "bio")
        bio_input.clear()
        bio_input.send_keys("Nouvelle bio")

        # Sauvegarder
        submit_button = self.driver.find_element(
            By.CSS_SELECTOR, 'button[type="submit"]'
        )
        submit_button.click()

        # Vérifier la mise à jour
        time.sleep(2)  # Attendre la mise à jour
        self.student.refresh_from_db()
        self.assertEqual(self.student.bio, "Nouvelle bio")
