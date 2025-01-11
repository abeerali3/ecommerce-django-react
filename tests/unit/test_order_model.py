
from django.test import TestCase
from django.contrib.auth.models import User
from base.models import Order
from decimal import Decimal
from datetime import datetime

class OrderModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.order = Order.objects.create(
            user=self.user,
            paymentMethod='Credit Card',
            taxPrice=Decimal('5.00'),
            shippingPrice=Decimal('10.00'),
            totalPrice=Decimal('115.00'),
            isPaid=True,
            paidAt=datetime.now(),
            isDeliver=True,
            deliveredAt=datetime.now()
        )

    def test_order_creation(self):
        order = Order.objects.get(user=self.user)
        self.assertEqual(order.paymentMethod, 'Credit Card')
        self.assertEqual(order.taxPrice, Decimal('5.00'))
        self.assertEqual(order.shippingPrice, Decimal('10.00'))
        self.assertEqual(order.totalPrice, Decimal('115.00'))
        self.assertTrue(order.isPaid)
        self.assertIsNotNone(order.paidAt)
        self.assertTrue(order.isDeliver)
        self.assertIsNotNone(order.deliveredAt)
        self.assertEqual(order.user.username, 'testuser')

    def test_order_str(self):
        order = Order.objects.get(user=self.user)
        self.assertEqual(str(order), str(order.createdAt))
