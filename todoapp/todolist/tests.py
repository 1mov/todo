from django.test import TestCase
from django.contrib.auth.models import User
from .models import Task

class TaskTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        self.task = Task.objects.create(user=self.user, title='Test Task')

    def test_add_task(self):
        response = self.client.post('/add/', {'title': 'New Task'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.count(), 2)

    def test_edit_task(self):
        response = self.client.post(f'/edit/{self.task.id}/', {'title': 'Updated Task'})
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated Task')

    def test_delete_task(self):
        response = self.client.post(f'/delete/{self.task.id}/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.count(), 0)
