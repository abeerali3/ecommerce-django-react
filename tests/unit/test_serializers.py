from django.test import TestCase
from django.contrib.auth.models import User
from base.models import Order, OrderItem, ShippingAddress, Review, Product
from base.serializers import OrderSerializer, UserSerializer, ProductSerializer

class UserSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword', email='test@example.com')

    def test_user_serializer(self):
        serializer = UserSerializer(self.user)
        data = serializer.data
        self.assertEqual(data['username'], self.user.username)
        self.assertEqual(data['email'], self.user.email)

class OrderSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.order = Order.objects.create(user=self.user, totalPrice=100.0)

    def test_order_serializer(self):
        serializer = OrderSerializer(self.order)
        data = serializer.data
        print(data)  
        self.assertEqual(data['totalPrice'], '100.00')  
        self.assertEqual(data['user'], self.user.id)  



class ProductSerializerTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name='Test Product', price=10.0)

    def test_product_serializer(self):
        serializer = ProductSerializer(self.product)
        data = serializer.data
        self.assertEqual(data['name'], self.product.name)
        self.assertEqual(data['price'], '10.00')

# You can add more tests for other serializers as well
