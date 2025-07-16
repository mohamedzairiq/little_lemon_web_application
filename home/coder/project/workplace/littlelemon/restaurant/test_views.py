from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from restaurant.models import Menu


class MenuViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser', password='testpass')
        self.menu = Menu.objects.create(
            name="Burger", price=10, description="Tasty burger")

    def test_get_menu_list(self):
        # router auto-generates 'menu-list'
        response = self.client.get(reverse('menu-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
