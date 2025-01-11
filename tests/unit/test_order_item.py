
from django.test import TestCase
from django.contrib.auth.models import User
from base.models import Product, Order, OrderItem
from decimal import Decimal

class OrderItemModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.product = Product.objects.create(
            user=self.user,
            name='Test Product',
            image='images/test.png',
            brand='Test Brand',
            category='Test Category',
            description='Test Description',
            rating=Decimal('4.5'),
            numReviews=10,
            price=Decimal('99.99'),
            countInStock=50
        )
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
        self.order_item = OrderItem.objects.create(
            product=self.product,
            order=self.order,
            name='Test Order Item',
            qty=2,
            price=Decimal('99.99'),
            image='images/test.png'
        )

    def test_order_item_creation(self):
        order_item = OrderItem.objects.get(name='Test Order Item')
        self.assertEqual(order_item.product.name, 'Test Product')
        self.assertEqual(order_item.order.user.username, 'testuser')
        self.assertEqual(order_item.name, 'Test Order Item')
        self.assertEqual(order_item.qty, 2)
        self.assertEqual(order_item.price, Decimal('99.99'))
        self.assertEqual(order_item.image, 'images/test.png')

    def test_order_item_str(self):
        order_item = OrderItem.objects.get(name='Test Order Item')
        self.assertEqual(str(order_item), 'Test Order Item')
