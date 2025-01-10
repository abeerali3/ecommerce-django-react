from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from base.models import Product, Order, OrderItem, ShippingAddress

class OrderViewsTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.force_authenticate(user=self.user)
        self.admin_user = User.objects.create_superuser(username='admin', password='admin123')

    def test_add_order_items(self):
        product = Product.objects.create(name='Product 1', price=50, countInStock=10, user=self.user)
        payload = {
            'orderItems': [{'product': product._id, 'qty': 1, 'price': 50}],
            'paymentMethod': 'PayPal',
            'taxPrice': 5.0,
            'shippingPrice': 5.0,
            'totalPrice': 60.0,
            'shippingAddress': {'address': '123 Street', 'city': 'City', 'postalCode': '12345', 'country': 'Country'}
        }
        response = self.client.post(reverse('orders-add'), payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_my_orders(self):
        order = Order.objects.create(user=self.user, totalPrice=100)
        response = self.client.get(reverse('myorders'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_orders_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        Order.objects.create(user=self.user, totalPrice=100)
        response = self.client.get(reverse('allorders'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_order_by_id(self):
        order = Order.objects.create(user=self.user, totalPrice=100)
        response = self.client.get(reverse('user-order', args=[order._id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_order_to_paid(self):
        order = Order.objects.create(user=self.user, totalPrice=100)
        response = self.client.put(reverse('pay', args=[order._id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        order.refresh_from_db()
        self.assertTrue(order.isPaid)

    def test_update_order_to_delivered(self):
        self.client.force_authenticate(user=self.admin_user)
        order = Order.objects.create(user=self.user, totalPrice=100)
        response = self.client.put(reverse('delivered', args=[order._id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        order.refresh_from_db()
        self.assertTrue(order.isDeliver)
