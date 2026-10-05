from decimal import Decimal
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Product
from rest_framework_simplejwt.tokens import RefreshToken


class ProductAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        self.product = Product.objects.create(
            name="Laptop",
            description="High performance laptop",
            price=Decimal("999.99"),
            stock_quantity=15,
            category="Electronics",
        )
        self.list_url = reverse('product-list')
        self.detail_url = reverse('product-detail', kwargs={'pk': self.product.pk})

    def test_create_valid_product(self):
        data = {
            "name": "Keyboard",
            "description": "Mechanical keyboard",
            "price": "79.99",
            "stock_quantity": 25,
            "category": "Electronics",
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], "Keyboard")

    def test_fetch_product_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_fetch_product_details(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.product.name)

    def test_update_product(self):
        data = {
            "name": "Updated Laptop",
            "description": "Updated description",
            "price": "899.99",
            "stock_quantity": 10,
            "category": "Electronics",
        }
        response = self.client.put(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, "Updated Laptop")

    def test_delete_product(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(pk=self.product.pk).exists())

    def test_invalid_product_creation_negative_price(self):
        data = {
            "name": "Invalid Product",
            "description": "Test",
            "price": "-10.00",
            "stock_quantity": 10,
            "category": "Electronics",
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('price', response.data)

    def test_invalid_product_creation_negative_stock(self):
        data = {
            "name": "Invalid Stock Product",
            "description": "Test",
            "price": "50.00",
            "stock_quantity": -5,
            "category": "Electronics",
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('stock_quantity', response.data)

    def test_unauthenticated_request_rejected(self):
        self.client.credentials()  # Remove token
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_access(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

