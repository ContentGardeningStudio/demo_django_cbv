from django.test import TestCase
from django.urls import reverse
from django import test
import pytest


@pytest.mark.django_db
class TestViews(TestCase):
    def setUp(self):
        self.client = test.Client()

    def test_order_list_view_status_code(self):
        url = reverse("order-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_order_list_response_content(self):
        url = reverse("order-list")
        response = self.client.get(url)
        self.assertIn(b"Orders", response.content)