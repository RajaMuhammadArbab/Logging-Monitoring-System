from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase

class SmokeTest(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user('admin', password='pass', is_staff=True)
        self.user = User.objects.create_user('bob', password='pass')

    def auth(self, username='bob', password='pass'):
        url = reverse('login')
        resp = self.client.post(url, {'username': username, 'password': password}, format='json')
        self.assertEqual(resp.status_code, 200)
        token = resp.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_activity_flow(self):
        self.auth()
        
        resp = self.client.patch(reverse('me-profile'), {'first_name': 'B'}, format='json')
        self.assertIn(resp.status_code, [200, 204])
       
        resp = self.client.post('/api/items/', {'name': 'N', 'description': 'D'}, format='json')
        self.assertEqual(resp.status_code, 201)

    def test_admin_logs(self):
        self.auth('admin', 'pass')
        resp = self.client.get(reverse('activity-logs'))
        self.assertIn(resp.status_code, [200, 204])
