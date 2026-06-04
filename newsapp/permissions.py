"""
Custom DRF permission classes for the ``newsapp`` application.

Permission Matrix
=================
The following table summarises which roles may perform which actions:

=====================  ======  ======  ===========  ======  =========
Role                   GET     POST    PUT/PATCH    DELETE  APPROVE
=====================  ======  ======  ===========  ======  =========
Reader                 yes     no      no           no      no
Journalist (own)       yes     yes     yes          yes     no
Editor (any)           yes     no      yes          yes     yes
=====================  ======  ======  ===========  ======  =========

Classes
-------
- **IsReader** – allows access only to users with role ``reader``.
- **IsJournalist** – allows access only to users with role ``journalist``.
- **IsEditor** – allows access only to users with role ``editor``.
- **IsJournalistOrEditor** – allows access to journalists and editors.
- **ArticlePermission** – full CRUD rule set for articles.
- **ApproveArticlePermission** – editor‑only guard for approval actions.
- **NewsletterPermission** – CRUD rule set for newsletters.
"""

from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsReader(BasePermission):
    """
    Allow access only to authenticated users whose role is ``reader``.
    """

    def has_permission(self, request, view) -> bool:
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_reader
        )


class IsJournalist(BasePermission):
    """
    Allow access only to authenticated users whose role is ``journalist``.
    """

    def has_permission(self, request, view) -> bool:
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_journalist
        )


class IsEditor(BasePermission):
    """
    Allow access only to authenticated users whose role is ``editor``.
    """

    def has_permission(self, request, view) -> bool:
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_editor
        )


class IsJournalistOrEditor(BasePermission):
    """
    Allow access to authenticated users whose role is ``journalist`` or
    ``editor``.
    """

    def has_permission(self, request, view) -> bool:
        if not (request.user and request.user.is_authenticated):
            return False
        return request.user.is_journalist or request.user.is_editor


class ArticlePermission(BasePermission):
    """
    Role‑based permission logic for article endpoints.

    View‑level rules (``has_permission``)
    -------------------------------------
    - **Safe methods** (GET, HEAD, OPTIONS): allowed for any authenticated user.
    - **POST**: journalists only.
    - **PUT / PATCH / DELETE**: journalists or editors (object‑level rules
      further restrict journalists to their own articles).

    Object‑level rules (``has_object_permission``)
    ----------------------------------------------
    - **Safe methods**: always allowed.
    - **Editors**: full access to any article.
    - **Journalists**: allowed only if they authored the article.
    """

    def has_permission(self, request, view) -> bool:
        if not (request.user and request.user.is_authenticated):
            return False

        if request.method in SAFE_METHODS:
            return True

        if request.method == "POST":
            return request.user.is_journalist

        return request.user.is_journalist or request.user.is_editor

    def has_object_permission(self, request, view, obj) -> bool:
        if request.method in SAFE_METHODS:
            return True

        if request.user.is_editor:
            return True

        if request.user.is_journalist:
            return obj.author == request.user

        return False


class ApproveArticlePermission(BasePermission):
    """
    Permission guard for article approval actions.

    Only editors may approve or unapprove an article.
    """

    def has_permission(self, request, view) -> bool:
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_editor
        )


class NewsletterPermission(BasePermission):
    """
    Role‑based permission logic for newsletter endpoints.

    View‑level rules
    ----------------
    - **Safe methods**: allowed for any authenticated user.
    - **POST / PUT / PATCH / DELETE**: journalists or editors.

    Object‑level rules
    ------------------
    - **Safe methods**: always allowed.
    - **Editors**: full access to any newsletter.
    - **Journalists**: allowed only for newsletters they authored.
    """

    def has_permission(self, request, view) -> bool:
        if not (request.user and request.user.is_authenticated):
            return False

        if request.method in SAFE_METHODS:
            return True

        return request.user.is_journalist or request.user.is_editor

    def has_object_permission(self, request, view, obj) -> bool:
        if request.method in SAFE_METHODS:
            return True

        if request.user.is_editor:
            return True

        if request.user.is_journalist:
            return obj.author == request.user

        return False

