"""
Database models for the ``newsapp`` application.

Overview
========
This module defines the core data structures used throughout the news
publishing workflow:

- **Publisher** – a news organisation that employs journalists and editors.
- **User** – a custom user model extending ``AbstractUser`` with a ``role``
  field and reader‑specific subscription relations.
- **Article** – a piece of content written by a journalist or editor and
  subject to an editorial approval workflow.
- **Newsletter** – a curated collection of approved articles published by a
  journalist or editor.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class Publisher(models.Model):
    """
    A news publishing organisation.

    Each publisher maintains separate many‑to‑many relations for editors and
    journalists. ``limit_choices_to`` ensures that admin dropdowns only show
    users with the appropriate role.
    """

    name = models.CharField(
        max_length=255,
        unique=True,
        help_text="Display name of the publishing organisation.",
    )
    editors = models.ManyToManyField(
        "User",
        related_name="publishing_as_editor",
        blank=True,
        limit_choices_to={"role": "editor"},
        help_text="Editors affiliated with this publisher.",
    )
    journalists = models.ManyToManyField(
        "User",
        related_name="publishing_as_journalist",
        blank=True,
        limit_choices_to={"role": "journalist"},
        help_text="Journalists affiliated with this publisher.",
    )

    def __str__(self) -> str:
        return self.name


class User(AbstractUser):
    """
    Custom user model extending Django's ``AbstractUser`` with a ``role`` field
    and optional reader subscription relations.

    Roles
    -----
    - **reader** – can view approved content and subscribe to publishers or
      journalists.
    - **journalist** – can create, edit, and delete their own articles and
      newsletters.
    - **editor** – can view, edit, delete, and approve any article; can create
      and manage any newsletter.

    Reader‑only subscription fields are automatically cleared when a user
    becomes a journalist.
    """

    ROLE_CHOICES = [
        ("reader", "Reader"),
        ("journalist", "Journalist"),
        ("editor", "Editor"),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="reader",
        help_text="Determines site‑wide permissions for this user.",
    )

    subscribed_publishers = models.ManyToManyField(
        "Publisher",
        related_name="subscribers",
        blank=True,
        help_text="Publishers this reader follows.",
    )
    subscribed_journalists = models.ManyToManyField(
        "self",
        symmetrical=False,
        related_name="journalist_subscribers",
        blank=True,
        help_text="Journalists this reader follows.",
    )

    def save(self, *args, **kwargs) -> None:
        """
        Save the user and clear reader‑only subscription data if the role
        changes to ``journalist``.
        """
        super().save(*args, **kwargs)
        if self.role == "journalist":
            self.subscribed_publishers.clear()
            self.subscribed_journalists.clear()

    def __str__(self) -> str:
        return f"{self.username} ({self.role})"

    @property
    def is_reader(self) -> bool:
        """Return True if the user's role is ``reader``."""
        return self.role == "reader"

    @property
    def is_journalist(self) -> bool:
        """Return True if the user's role is ``journalist``."""
        return self.role == "journalist"

    @property
    def is_editor(self) -> bool:
        """Return True if the user's role is ``editor``."""
        return self.role == "editor"


class Article(models.Model):
    """
    A news article authored by a journalist or editor.

    Articles begin unapproved and become publicly visible only after an editor
    sets ``approved=True``. Approval records the approving editor and timestamp.
    A ``post_save`` signal in ``signals.py`` triggers email and Twitter/X
    notifications upon approval.
    """

    title = models.CharField(
        max_length=500,
        help_text="Headline of the article.",
    )
    content = models.TextField(
        help_text="Full body text of the article.",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="articles",
        limit_choices_to={"role__in": ["journalist", "editor"]},
        help_text="Journalist or editor who wrote the article.",
    )
    publisher = models.ForeignKey(
        "Publisher",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="articles",
        help_text="Affiliated publisher, or null for an independent article.",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    approved = models.BooleanField(
        default=False,
        help_text="Whether an editor has approved this article.",
    )
    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_articles",
        limit_choices_to={"role": "editor"},
        help_text="Editor who approved the article.",
    )
    approved_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Timestamp of editorial approval.",
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.title

    @property
    def is_independent(self) -> bool:
        """Return True if the article has no affiliated publisher."""
        return self.publisher is None


class Newsletter(models.Model):
    """
    A curated collection of approved articles.

    Newsletters may be created by journalists (for their own content) or
    editors (for any content). Readers can view all newsletters regardless of
    subscription settings.
    """

    title = models.CharField(
        max_length=500,
        help_text="Name of the newsletter edition.",
    )
    description = models.TextField(
        help_text="Short summary shown in newsletter listings.",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="newsletters",
        limit_choices_to={"role__in": ["journalist", "editor"]},
        help_text="Journalist or editor responsible for this newsletter.",
    )
    articles = models.ManyToManyField(
        Article,
        related_name="newsletters",
        blank=True,
        help_text="Articles included in this newsletter edition.",
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.title
