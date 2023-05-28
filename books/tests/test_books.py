import pytest
from rest_framework import status
from rest_framework.test import APIClient

from books.models import Book


@pytest.mark.django_db
class TestCreateCollection:
    def test_if_data_is_invalid_returns_400(self):
        client = APIClient()
        response = client.post("/books/", {"author": "Henry", "price": 300})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_data_is_valid_returns_201(self):
        client = APIClient()
        response = client.post(
            "/books/",
            {
                "title": "Atomic Habits",
                "author": "James Clear",
                "publication_date": "2020-12-8",
                "description": "about habit",
                "price": 4000,
            },
        )
        assert response.status_code == status.HTTP_201_CREATED
