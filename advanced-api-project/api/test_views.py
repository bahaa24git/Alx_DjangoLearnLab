# api/test_views.py
"""
Unit tests for the Book API endpoints (Django REST Framework).

Covers:
- CRUD for generic endpoints under /api/books/...
- Alias endpoints required by checker: /api/books/update and /api/books/delete (with ?id=)
- Filtering (django-filter), Searching (SearchFilter), Ordering (OrderingFilter)
- Permissions: anonymous can read; authenticated required for create/update/delete
"""

from datetime import date

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import Author, Book


class BookAPITests(APITestCase):
    def setUp(self):
        # Users
        User = get_user_model()
        self.user = User.objects.create_user(username="tester", password="pass1234")

        # Data
        self.author_orwell = Author.objects.create(name="George Orwell")
        self.author_huxley = Author.objects.create(name="Aldous Huxley")

        self.book_af = Book.objects.create(
            title="Animal Farm", publication_year=1945, author=self.author_orwell
        )
        self.book_1984 = Book.objects.create(
            title="1984", publication_year=1949, author=self.author_orwell
        )
        self.book_bnw = Book.objects.create(
            title="Brave New World", publication_year=1932, author=self.author_huxley
        )

        # Common URLs (names come from api/urls.py)
        self.url_list = "/api/books/"
        self.url_detail = f"/api/books/{self.book_af.id}/"
        self.url_create = "/api/books/create/"
        self.url_update_pk = f"/api/books/{self.book_af.id}/update/"
        self.url_delete_pk = f"/api/books/{self.book_bnw.id}/delete/"

        # Alias endpoints (literal paths the checker expects)
        self.url_update_alias = "/api/books/update"
        self.url_delete_alias = "/api/books/delete"

        # ViewSet base (router)
        self.url_v1_books = "/api/v1/books/"

    # ---------- Read (public) ----------
    def test_list_public_ok(self):
        resp = self.client.get(self.url_list)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(resp.json()), 3)

    def test_detail_public_ok(self):
        resp = self.client.get(self.url_detail)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.json()["title"], "Animal Farm")

    # ---------- Create ----------
    def test_create_requires_auth(self):
        payload = {"title": "New Book", "publication_year": 2001, "author": self.author_huxley.id}
        resp = self.client.post(self.url_create, payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_authenticated_ok(self):
        self.client.force_authenticate(self.user)
        payload = {"title": "Island", "publication_year": 1962, "author": self.author_huxley.id}
        resp = self.client.post(self.url_create, payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.json()["title"], "Island")
        self.assertTrue(Book.objects.filter(title="Island").exists())

    def test_create_future_year_invalid(self):
        self.client.force_authenticate(self.user)
        future_year = date.today().year + 1
        payload = {"title": "Future", "publication_year": future_year, "author": self.author_huxley.id}
        resp = self.client.post(self.url_create, payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("publication_year", resp.json())

    # ---------- Update ----------
    def test_update_requires_auth(self):
        payload = {"title": "Animal Farm (Edited)"}
        resp = self.client.patch(self.url_update_pk, payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_authenticated_ok_via_pk_endpoint(self):
        self.client.force_authenticate(self.user)
        payload = {"title": "Animal Farm — Patch via PK"}
        resp = self.client.patch(self.url_update_pk, payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.book_af.refresh_from_db()
        self.assertEqual(self.book_af.title, "Animal Farm — Patch via PK")

    def test_update_authenticated_ok_via_alias_with_query_param(self):
        self.client.force_authenticate(self.user)
        payload = {"title": "Animal Farm — Patch via Alias"}
        resp = self.client.patch(f"{self.url_update_alias}?id={self.book_af.id}", payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.book_af.refresh_from_db()
        self.assertEqual(self.book_af.title, "Animal Farm — Patch via Alias")

    # ---------- Delete ----------
    def test_delete_requires_auth(self):
        resp = self.client.delete(self.url_delete_pk)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_authenticated_ok_via_pk_endpoint(self):
        self.client.force_authenticate(self.user)
        resp = self.client.delete(self.url_delete_pk)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book_bnw.id).exists())

    def test_delete_authenticated_ok_via_alias_with_query_param(self):
        self.client.force_authenticate(self.user)
        # Create a throwaway book to delete via alias
        tmp = Book.objects.create(title="Temp", publication_year=2000, author=self.author_orwell)
        resp = self.client.delete(f"{self.url_delete_alias}?id={tmp.id}")
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=tmp.id).exists())

    # ---------- Filtering ----------
    def test_filter_by_year_range_and_author_name(self):
        resp = self.client.get(
            f"{self.url_list}?publication_year__gte=1930&publication_year__lte=1946&author__name__icontains=orwell"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        titles = [b["title"] for b in resp.json()]
        self.assertEqual(titles, ["Animal Farm"])  # only 1945 Orwell

    def test_filter_by_author_id(self):
        resp = self.client.get(f"{self.url_list}?author={self.author_orwell.id}")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        titles = sorted([b["title"] for b in resp.json()])
        self.assertEqual(titles, ["1984", "Animal Farm"])

    # ---------- Search ----------
    def test_search_title(self):
        resp = self.client.get(f"{self.url_list}?search=farm")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        titles = [b["title"] for b in resp.json()]
        self.assertEqual(titles, ["Animal Farm"])

    def test_q_backward_compat(self):
        resp = self.client.get(f"{self.url_list}?q=1984")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        titles = [b["title"] for b in resp.json()]
        self.assertEqual(titles, ["1984"])

    # ---------- Ordering ----------
    def test_ordering_desc_publication_year(self):
        resp = self.client.get(f"{self.url_list}?ordering=-publication_year")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        years = [b["publication_year"] for b in resp.json()]
        self.assertEqual(years, sorted(years, reverse=True))

    # ---------- ViewSet sanity (router endpoints under /api/v1/...) ----------
    def test_viewset_search_works(self):
        resp = self.client.get(f"{self.url_v1_books}?search=1984")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        titles = [b["title"] for b in resp.json()]
        self.assertIn("1984", titles)
