
from django.test import TestCase
from django.contrib.auth.models import User
from base.models import Order, ShippingAddress
from decimal import Decimal

class ShippingAddressModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.order = Order.objects.create(
            user=self.user,
            paymentMethod='Credit Card',
            taxPrice=Decimal('5.00'),
            shippingPrice=Decimal('10.00'),
            totalPrice=Decimal('115.00'),
            isPaid=True,
            paidAt=None,
            isDeliver=True,
            deliveredAt=None
        )
        self.shipping_address = ShippingAddress.objects.create(
            order=self.order,
            address='123 Test Street',
            city='Test City',
            postalCode='12345',
            country='Test Country',
            shippingPrice=Decimal('10.00')
        )

    def test_shipping_address_creation(self):
        shipping_address = ShippingAddress.objects.get(order=self.order)
        self.assertEqual(shipping_address.address, '123 Test Street')
        self.assertEqual(shipping_address.city, 'Test City')
        self.assertEqual(shipping_address.postalCode, '12345')
        self.assertEqual(shipping_address.country, 'Test Country')
        self.assertEqual(shipping_address.shippingPrice, Decimal('10.00'))
        self.assertEqual(shipping_address.order.user.username, 'testuser')

    def test_shipping_address_str(self):
        shipping_address = ShippingAddress.objects.get(order=self.order)
        self.assertEqual(str(shipping_address), '123 Test Street')
