
from django.test import TestCase
from django.contrib.auth.models import User
from base.models import Product, Review
from decimal import Decimal

class ReviewModelTests(TestCase):

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
        self.review = Review.objects.create(
            product=self.product,
            user=self.user,
            name='Test Review',
            rating=5,
            comment='This is a test review'
        )

    def test_review_creation(self):
        review = Review.objects.get(name='Test Review')
        self.assertEqual(review.product.name, 'Test Product')
        self.assertEqual(review.user.username, 'testuser')
        self.assertEqual(review.name, 'Test Review')
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.comment, 'This is a test review')

    def test_review_str(self):
        review = Review.objects.get(name='Test Review')
        self.assertEqual(str(review), '5')
