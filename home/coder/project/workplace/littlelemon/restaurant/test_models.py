from django.test import TestCase
from restaurant.models import Menu, Booking


class MenuModelTest(TestCase):
    def test_menu_str(self):
        menu = Menu.objects.create(
            name="Pasta", price=15, description="Delicious pasta")
        self.assertEqual(str(menu), "Pasta")


class BookingModelTest(TestCase):
    def test_booking_str(self):
        booking = Booking.objects.create(
            first_name="John", last_name="Doe", guest_number=2, comment="Window seat")
        self.assertEqual(str(booking), "John Doe")
