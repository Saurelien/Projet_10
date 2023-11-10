from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Project

User = get_user_model()


class ProjectCreateTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = APIClient()

    def test_create_project(self):
        self.client.force_authenticate(user=self.user)  # Authentifiez l'utilisateur
        url = '/api/create_project/'  # L'URL de votre vue de création de projet
        data = {
            'title': 'Test Project',
            'description': 'This is a test project',
            'type': 'back-end'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(), 1)
