from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from base .models import Product, Review, Order, OrderItem, ShippingAddress


class ModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_create_product(self):
        product = Product.objects.create(
            user=self.user,
            name="Sample Product",
            brand="Brand A",
            category="Category A",
            description="Description of Sample Product",
            price=99.99
        )
        self.assertEqual(product.name, "Sample Product")
        self.assertEqual(str(product), "Sample Product | Brand A | 99.99")

    def test_product_max_length(self):
        product = Product.objects.create(
            user=self.user,
            name="Sample Product" * 20,
        )
        self.assertGreater(len(product.name), 200)
        self.assertRaises(ValidationError, product.full_clean)

    def test_product_foreign_key(self):
        product = Product.objects.create(user=self.user, name="Sample Product")
        self.assertEqual(product.user.username, 'testuser')

    def test_create_review(self):
        product = Product.objects.create(user=self.user, name="Sample Product")
        review = Review.objects.create(
            product=product,
            user=self.user,
            rating=4,
            comment="Great product!"
        )
        self.assertEqual(review.rating, 4)
        self.assertEqual(str(review), "4")

    def test_review_foreign_key(self):
        product = Product.objects.create(user=self.user, name="Sample Product")
        review = Review.objects.create(
            product=product,
            user=self.user,
            rating=4,
            comment="Great product!"
        )
        self.assertEqual(review.product.name, "Sample Product")
        self.assertEqual(review.user.username, 'testuser')

    def test_create_order(self):
        order = Order.objects.create(
            user=self.user,
            totalPrice=200.00,
            isPaid=True
        )
        self.assertEqual(order.totalPrice, 200.00)
        self.assertEqual(str(order), str(order.createdAt))

    def test_order_foreign_key(self):
        order = Order.objects.create(
            user=self.user,
            totalPrice=200.00,
            isPaid=True
        )
        self.assertEqual(order.user.username, 'testuser')

    def test_create_order_item(self):
        product = Product.objects.create(user=self.user, name="Sample Product")
        order = Order.objects.create(user=self.user)
        order_item = OrderItem.objects.create(
            product=product,
            order=order,
            qty=2,
            price=99.99,
            name="Sample Product"
        )
        self.assertEqual(order_item.qty, 2)
        self.assertEqual(str(order_item), "Sample Product")

    def test_order_item_foreign_key(self):
        product = Product.objects.create(user=self.user, name="Sample Product")
        order = Order.objects.create(user=self.user)
        order_item = OrderItem.objects.create(
            product=product,
            order=order,
            qty=2,
            price=99.99,
            name="Sample Product"
        )
        self.assertEqual(order_item.product.name, "Sample Product")
        self.assertEqual(order_item.order.user.username, 'testuser')

    def test_create_shipping_address(self):
        order = Order.objects.create(user=self.user)
        shipping_address = ShippingAddress.objects.create(
            order=order,
            address="123 Sample Street",
            city="Sample City",
            postalCode="12345",
            country="Sample Country"
        )
        self.assertEqual(shipping_address.address, "123 Sample Street")
        self.assertEqual(str(shipping_address), "123 Sample Street")

    def test_shipping_address_foreign_key(self):
        order = Order.objects.create(user=self.user)
        shipping_address = ShippingAddress.objects.create(
            order=order,
            address="123 Sample Street",
            city="Sample City",
            postalCode="12345",
            country="Sample Country"
        )
        self.assertEqual(shipping_address.order.user.username, 'testuser')
