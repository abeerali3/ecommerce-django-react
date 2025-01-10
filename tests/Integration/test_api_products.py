from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from base.models import Product, Review
import os

class ProductViewsTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.admin_user = User.objects.create_superuser(username='admin', password='admin123')
        self.client.force_authenticate(user=self.admin_user)
        self.product = Product.objects.create(
            name='Product 1',
            price=50,
            countInStock=10,
            user=self.admin_user,
            brand='Brand A',
            category='Category A'
        )

    def test_get_products(self):
        response = self.client.get(reverse('products'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['products']), 1)

    def test_get_top_products(self):
        response = self.client.get(reverse('top-products'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_product(self):
        response = self.client.get(reverse('product', args=[self.product._id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_product(self):
        payload = {
            'name': 'New Product',
            'price': 100,
            'countInStock': 20,
            'brand': 'Brand B',
            'category': 'Category B',
            'description': 'New product description'
        }
        response = self.client.post(reverse('create_product'), payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)  

    def test_update_product(self):
        payload = {
            'name': 'Updated Product',
            'price': 150,
            'countInStock': 30,
            'brand': 'Brand C',
            'category': 'Category C',
            'description': 'Updated product description'
        }
        response = self.client.put(reverse('update_product', args=[self.product._id]), payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_product(self):
        response = self.client.delete(reverse('delete_product', args=[self.product._id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_upload_image(self):
        image_path = 'media/images/test.jpg'  
        with open(image_path, 'rb') as image:
            response = self.client.post(reverse('upload_image'), {'product_id': self.product._id, 'image': image}, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_product_review(self):
        self.client.force_authenticate(user=self.user)
        payload = {'rating': 5, 'comment': 'Great product!'}
        response = self.client.post(reverse('create-review', args=[self.product._id]), payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Expecting 200 OK

    
        response = self.client.post(reverse('create-review', args=[self.product._id]), payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

      
        payload = {'rating': 0, 'comment': 'No rating'}
        response = self.client.post(reverse('create-review', args=[self.product._id]), payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
