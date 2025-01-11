
from django.test import TestCase
from django.contrib.auth.models import User
from base .models import Product
from decimal import Decimal

class ProductModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.product = Product.objects.create(
            user=self.user,
            name='Test Product',
            image='images/test.png',
            brand='Test Brand',
            category='Test Category',
            description='Test Description',
            rating=4.5,
            numReviews=10,
            price=Decimal('99.99'),
            countInStock=50  
        )

    def test_product_creation(self):
        product = Product.objects.get(name='Test Product')
        print(f"Product countInStock: {product.countInStock}")  
        self.assertEqual(product.name, 'Test Product')
        self.assertEqual(product.image, 'images/test.png')
        self.assertEqual(product.brand, 'Test Brand')
        self.assertEqual(product.category, 'Test Category')
        self.assertEqual(product.description, 'Test Description')
        self.assertEqual(product.rating, 4.5)
        self.assertEqual(product.numReviews, 10)
        self.assertEqual(product.price, Decimal('99.99'))
        self.assertEqual(product.countInStock, 50) 
        self.assertEqual(product.user, self.user)

    def test_product_str(self):
        product = Product.objects.get(name='Test Product')
        self.assertEqual(str(product), 'Test Product | Test Brand | 99.99')
