"""
Unit tests for the ``newsapp`` application.

Overview
========
This module contains comprehensive test coverage for authentication,
permissions, newsletters, articles, signals, and model behaviour.

Test Classes
------------
- **AuthenticationTests** – token login, registration, and role‑based article visibility.
- **ReaderTests** – reader access restrictions and subscribed‑feed behaviour.
- **JournalistTests** – journalist CRUD boundaries and newsletter creation.
- **EditorTests** – editor approval powers and full content management.
- **NewsletterTests** – newsletter visibility, creation rules, and article association.
- **SignalTests** – mocked side‑effects for email and Twitter posting.
- **ModelTests** – model property correctness and subscription‑clearing logic.

All external I/O (``send_mail``, ``requests.post``) is patched using
``unittest.mock`` so tests run without network or email dependencies.
"""

from unittest.mock import MagicMock, patch

from django.test import Client, TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from django.contrib.auth import get_user_model

from .models import Article, Newsletter, Publisher

User = get_user_model()


# ---------------------------------------------------------------------------
# Test helpers
# ---------------------------------------------------------------------------

def make_user(username: str, role: str, password: str = "testpass123") -> User:
    """
    Create and return a ``User`` with the given role and hashed password.
    """
    return User.objects.create_user(
        username=username, password=password, role=role
    )


def get_token(user: User) -> str:
    """
    Return (creating if necessary) the DRF authentication token for ``user``.
    """
    token, _ = Token.objects.get_or_create(user=user)
    return token.key


def auth_client(user: User) -> APIClient:
    """
    Return a DRF ``APIClient`` preconfigured with the user's token.
    """
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Token {get_token(user)}")
    return client


# ---------------------------------------------------------------------------
# Authentication tests
# ---------------------------------------------------------------------------

class AuthenticationTests(TestCase):
    """
    Verify token‑based authentication and role‑based article visibility.

    Covers:
    - login success/failure
    - registration
    - unauthenticated access
    - per‑role queryset filtering on ``GET /api/articles/``
    """

    def setUp(self) -> None:
        self.reader = make_user("reader1", "reader")
        self.journalist = make_user("journalist1", "journalist")
        self.editor = make_user("editor1", "editor")

    def test_api_login_success(self) -> None:
        """A valid credential pair returns HTTP 200 and a token."""
        client = APIClient()
        response = client.post(
            "/api/auth/login/",
            {"username": "reader1", "password": "testpass123"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

    def test_api_login_wrong_password(self) -> None:
        """An incorrect password returns HTTP 401."""
        client = APIClient()
        response = client.post(
            "/api/auth/login/",
            {"username": "reader1", "password": "wrongpass"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_api_register(self) -> None:
        """A valid registration payload returns HTTP 201 with a token."""
        client = APIClient()
        response = client.post(
            "/api/auth/register/",
            {"username": "newuser", "password": "testpass123", "role": "reader"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("token", response.data)

    def test_unauthenticated_cannot_list_articles(self) -> None:
        """Unauthenticated requests to ``/api/articles/`` return HTTP 401."""
        client = APIClient()
        response = client.get("/api/articles/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_reader_can_list_approved_articles(self) -> None:
        """Readers may list approved articles."""
        publisher = Publisher.objects.create(name="Test Pub")
        Article.objects.create(
            title="Approved Article",
            content="Content",
            author=self.journalist,
            publisher=publisher,
            approved=True,
        )
        client = auth_client(self.reader)
        response = client.get("/api/articles/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_journalist_sees_own_unapproved_articles(self) -> None:
        """A journalist can see their own unapproved drafts."""
        Article.objects.create(
            title="My Draft",
            content="Draft content",
            author=self.journalist,
            approved=False,
        )
        client = auth_client(self.journalist)
        response = client.get("/api/articles/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [a["title"] for a in response.data["results"]]
        self.assertIn("My Draft", titles)

    def test_reader_cannot_see_unapproved_articles(self) -> None:
        """Readers must not see unapproved articles."""
        Article.objects.create(
            title="Hidden Draft",
            content="Draft",
            author=self.journalist,
            approved=False,
        )
        client = auth_client(self.reader)
        response = client.get("/api/articles/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [a["title"] for a in response.data["results"]]
        self.assertNotIn("Hidden Draft", titles)


# ---------------------------------------------------------------------------
# Reader tests
# ---------------------------------------------------------------------------

class ReaderTests(TestCase):
    """
    Verify reader‑specific restrictions and the subscribed‑feed endpoint.

    Covers:
    - POST/DELETE prohibition
    - ``GET /api/articles/subscribed/`` returning only subscribed content
    """

    def setUp(self) -> None:
        self.reader = make_user("reader2", "reader")
        self.journalist = make_user("journalist2", "journalist")
        self.publisher = Publisher.objects.create(name="Sub Publisher")
        self.approved_article = Article.objects.create(
            title="Sub Article",
            content="Content",
            author=self.journalist,
            publisher=self.publisher,
            approved=True,
        )
        self.reader.subscribed_publishers.add(self.publisher)
        self.reader.subscribed_journalists.add(self.journalist)

    def test_reader_cannot_post_article(self) -> None:
        """Readers must receive HTTP 403 when attempting to POST an article."""
        client = auth_client(self.reader)
        response = client.post(
            "/api/articles/",
            {"title": "Illegal", "content": "No", "author": self.reader.pk},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_reader_can_get_subscribed_articles(self) -> None:
        """The subscribed‑feed endpoint returns HTTP 200 for readers."""
        client = auth_client(self.reader)
        response = client.get("/api/articles/subscribed/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reader_cannot_delete_article(self) -> None:
        """Readers must receive 403 or 405 when attempting to DELETE."""
        client = auth_client(self.reader)
        response = client.delete(f"/api/articles/{self.approved_article.pk}/")
        self.assertIn(
            response.status_code,
            [status.HTTP_403_FORBIDDEN, status.HTTP_405_METHOD_NOT_ALLOWED],
        )


# ---------------------------------------------------------------------------
# Journalist tests
# ---------------------------------------------------------------------------

class JournalistTests(TestCase):
    """
    Verify journalist article and newsletter permissions.

    Covers:
    - create/update own article
    - cannot modify others' articles
    - cannot approve articles
    - can create newsletters
    - editors cannot POST articles
    """

    def setUp(self) -> None:
        self.journalist = make_user("journalist3", "journalist")
        self.editor = make_user("editor3", "editor")
        self.other_journalist = make_user("other_journalist", "journalist")

    def test_journalist_can_create_article(self) -> None:
        """A journalist POST returns HTTP 201."""
        client = auth_client(self.journalist)
        response = client.post(
            "/api/articles/",
            {
                "title": "My Article",
                "content": "Great content",
                "author": self.journalist.pk,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertFalse(response.data["approved"])

    def test_journalist_can_update_own_article(self) -> None:
        """A journalist may PATCH their own article."""
        article = Article.objects.create(
            title="Original", content="Content", author=self.journalist
        )
        client = auth_client(self.journalist)
        response = client.patch(
            f"/api/articles/{article.pk}/",
            {"title": "Updated Title"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Updated Title")

    def test_journalist_cannot_update_other_article(self) -> None:
        """A journalist must not PATCH another journalist's article."""
        article = Article.objects.create(
            title="Others Article",
            content="Content",
            author=self.other_journalist,
        )
        client = auth_client(self.journalist)
        response = client.patch(
            f"/api/articles/{article.pk}/",
            {"title": "Hijack"},
            format="json",
        )
        self.assertIn(
            response.status_code,
            [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND],
        )

    def test_journalist_cannot_approve_article(self) -> None:
        """A journalist POSTing to ``/approve/`` must receive HTTP 403."""
        article = Article.objects.create(
            title="Pending", content="Content", author=self.journalist
        )
        client = auth_client(self.journalist)
        response = client.post(f"/api/articles/{article.pk}/approve/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_editor_cannot_create_article(self) -> None:
        """Editors cannot POST articles."""
        client = auth_client(self.editor)
        response = client.post(
            "/api/articles/",
            {
                "title": "Editor Article",
                "content": "Content",
                "author": self.editor.pk,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_journalist_can_create_newsletter(self) -> None:
        """A journalist may POST a newsletter."""
        client = auth_client(self.journalist)
        response = client.post(
            "/api/newsletters/",
            {
                "title": "My Newsletter",
                "description": "Weekly digest",
                "author": self.journalist.pk,
                "articles": [],
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


# ---------------------------------------------------------------------------
# Editor tests
# ---------------------------------------------------------------------------

class EditorTests(TestCase):
    """
    Verify editor approval powers and full content management.

    Covers:
    - approve/unapprove
    - update/delete any article
    - update any newsletter
    - approval dashboard access rules
    """

    def setUp(self) -> None:
        self.journalist = make_user("journalist4", "journalist")
        self.editor = make_user("editor4", "editor")
        self.article = Article.objects.create(
            title="For Approval",
            content="Content",
            author=self.journalist,
            approved=False,
        )

    def test_editor_can_approve_article(self) -> None:
        """Editors POSTing to ``/approve/`` set approved=True."""
        client = auth_client(self.editor)
        response = client.post(f"/api/articles/{self.article.pk}/approve/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.article.refresh_from_db()
        self.assertTrue(self.article.approved)
        self.assertEqual(self.article.approved_by, self.editor)

    def test_editor_can_delete_any_article(self) -> None:
        """Editors may DELETE any article."""
        client = auth_client(self.editor)
        response = client.delete(f"/api/articles/{self.article.pk}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_editor_can_update_any_article(self) -> None:
        """Editors may PATCH any article."""
        client = auth_client(self.editor)
        response = client.patch(
            f"/api/articles/{self.article.pk}/",
            {"title": "Editor Updated"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_editor_can_unapprove_article(self) -> None:
        """Editors POSTing to ``/unapprove/`` set approved=False."""
        self.article.approved = True
        self.article.approved_by = self.editor
        self.article.save()
        client = auth_client(self.editor)
        response = client.post(f"/api/articles/{self.article.pk}/unapprove/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.article.refresh_from_db()
        self.assertFalse(self.article.approved)

    def test_editor_can_access_approval_template_view(self) -> None:
        """Editors receive HTTP 200 on the approval dashboard."""
        dj_client = Client()
        dj_client.login(username="editor4", password="testpass123")
        response = dj_client.get("/articles/approval/")
        self.assertEqual(response.status_code, 200)

    def test_non_editor_cannot_access_approval_page(self) -> None:
        """Non‑editors are redirected from the approval dashboard."""
        dj_client = Client()
        dj_client.login(username="journalist4", password="testpass123")
        response = dj_client.get("/articles/approval/")
        self.assertEqual(response.status_code, 302)

    def test_editor_can_update_any_newsletter(self) -> None:
        """Editors may PATCH any newsletter."""
        newsletter = Newsletter.objects.create(
            title="Journalist NL",
            description="...",
            author=self.journalist,
        )
        client = auth_client(self.editor)
        response = client.patch(
            f"/api/newsletters/{newsletter.pk}/",
            {"title": "Editor Updated NL"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Editor Updated NL")


# ---------------------------------------------------------------------------
# Newsletter tests
# ---------------------------------------------------------------------------

class NewsletterTests(TestCase):
    """
    Verify newsletter visibility, creation rules, and article association.

    Covers:
    - all roles can list newsletters
    - readers see all newsletters
    - readers cannot POST
    - editors can POST
    - journalists can associate articles
    """

    def setUp(self) -> None:
        self.journalist = make_user("journalist5", "journalist")
        self.editor = make_user("editor5", "editor")
        self.reader = make_user("reader5", "reader")
        self.newsletter = Newsletter.objects.create(
            title="Weekly Tech",
            description="Top tech news",
            author=self.journalist,
        )

    def test_any_authenticated_user_can_list_newsletters(self) -> None:
        """All authenticated roles may list newsletters."""
        for user in [self.journalist, self.editor, self.reader]:
            client = auth_client(user)
            response = client.get("/api/newsletters/")
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reader_sees_all_newsletters(self) -> None:
        """Readers see all newsletters, not filtered by subscription."""
        other_journalist = make_user("other_j5", "journalist")
        Newsletter.objects.create(
            title="Other Newsletter",
            description="From another journalist",
            author=other_journalist,
        )
        client = auth_client(self.reader)
        response = client.get("/api/newsletters/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [n["title"] for n in response.data["results"]]
        self.assertIn("Other Newsletter", titles)

    def test_reader_cannot_create_newsletter(self) -> None:
        """Readers must receive HTTP 403 when attempting to POST."""
        client = auth_client(self.reader)
        response = client.post(
            "/api/newsletters/",
            {"title": "Illegal", "description": "No", "author": self.reader.pk},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_editor_can_create_newsletter(self) -> None:
        """Editors may POST newsletters."""
        client = auth_client(self.editor)
        response = client.post(
            "/api/newsletters/",
            {
                "title": "Editor Newsletter",
                "description": "Curated by editor",
                "author": self.editor.pk,
                "articles": [],
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_journalist_can_add_articles_to_newsletter(self) -> None:
        """Journalists may associate articles with their newsletters."""
        article = Article.objects.create(
            title="Tech Article",
            content="Content",
            author=self.journalist,
            approved=True,
        )
        self.newsletter.articles.add(article)
        self.assertEqual(self.newsletter.articles.count(), 1)


# ---------------------------------------------------------------------------
# Signal tests
# ---------------------------------------------------------------------------

class SignalTests(TestCase):
    """
    Verify that article approval triggers the correct signal side‑effects.

    All external I/O is patched using ``unittest.mock`` so tests run without
    network or email dependencies.

    Covers:
    - both signals fire on approval
    - neither fires on unapproval
    - email sent to correct subscriber
    - tweet posted to correct URL
    - network errors handled gracefully
    - tweet skipped when bearer token missing
    """

    def setUp(self) -> None:
        self.journalist = make_user("journalist6", "journalist")
        self.editor = make_user("editor6", "editor")
        self.publisher = Publisher.objects.create(name="Signal Pub")
        self.article = Article.objects.create(
            title="Signal Article",
            content="Content
