from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User, Group
from .models import Menu, Booking, Cart, Order


class MenuAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="testpass")
        self.menu = Menu.objects.create(
            name="Pizza", price=10, description="Cheese Pizza")

    def test_menu_list(self):
        response = self.client.get(reverse('menu-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_menu_create_authenticated(self):
        self.client.force_authenticate(user=self.user)
        data = {'name': 'Pasta', 'price': 12, 'description': 'Creamy pasta'}
        response = self.client.post(reverse('menu-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class BookingAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="bookuser", password="testpass")
        self.client.force_authenticate(user=self.user)

    def test_booking_create(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'guest_number': 2,
            'comment': 'Window seat'
        }
        response = self.client.post(reverse('booking-list-create'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class CartAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="cartuser", password="testpass")
        self.menu_item = Menu.objects.create(
            name="Burger", price=8, description="Beef burger")
        self.client.force_authenticate(user=self.user)

    def test_add_to_cart(self):
        data = {
            'menuitem': self.menu_item.id,
            'quantity': 2,
            'unit_price': 8,
            'price': 16
        }
        response = self.client.post(reverse('cart'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_cart_list(self):
        Cart.objects.create(
            user=self.user, menuitem=self.menu_item, quantity=1, unit_price=8, price=8)
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class OrderAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.customer = User.objects.create_user(
            username="customer", password="pass")
        self.manager = User.objects.create_user(
            username="manager", password="pass")
        self.delivery = User.objects.create_user(
            username="delivery", password="pass")

        # Create groups
        manager_group = Group.objects.create(name='Manager')
        delivery_group = Group.objects.create(name='Delivery crew')
        manager_group.user_set.add(self.manager)
        delivery_group.user_set.add(self.delivery)

        # Create an order for customer
        self.order = Order.objects.create(user=self.customer, total=20)

    def test_customer_can_view_own_order(self):
        self.client.force_authenticate(user=self.customer)
        response = self.client.get(reverse('order-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_manager_can_view_all_orders(self):
        self.client.force_authenticate(user=self.manager)
        response = self.client.get(reverse('order-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)

    def test_delivery_can_view_assigned_orders(self):
        self.client.force_authenticate(user=self.delivery)
        response = self.client.get(reverse('order-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)  # No orders assigned yet


class PermissionTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_superuser(
            username="admin", password="adminpass", email="admin@test.com")
        self.user = User.objects.create_user(
            username="normaluser", password="testpass")
        Group.objects.create(name="Manager")

    def test_assign_manager(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(
            reverse('assign_manager', args=[self.user.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.user.groups.filter(name='Manager').exists())
