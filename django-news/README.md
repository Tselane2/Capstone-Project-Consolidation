# Django News Application

A full-featured news platform built with Django 5 and Django REST Framework. Supports three user roles (Reader, Journalist, Editor) with role-based access control, an editorial article approval workflow, REST API with token authentication, Django signals for email and Twitter/X notifications, and a responsive HTML frontend.

---

## Table of Contents

1. [Features](#features)
2. [Tech Stack](#tech-stack)
3. [Project Structure](#project-structure)
4. [Setup & Installation](#setup--installation)
5. [Environment Variables](#environment-variables)
6. [Running the App](#running-the-app)
7. [Demo Accounts](#demo-accounts)
8. [User Roles & Permissions](#user-roles--permissions)
9. [Article Approval Workflow](#article-approval-workflow)
10. [Django Signals](#django-signals)
11. [REST API Reference](#rest-api-reference)
12. [Frontend Routes](#frontend-routes)
13. [Running Tests](#running-tests)
14. [Database](#database)

---

## Features

- **Role-based access control** — Reader, Journalist, and Editor roles with distinct Django groups and permissions
- **Article approval workflow** — editors review, approve, and unapprove articles through a dedicated dashboard
- **Django signals** — article approval triggers subscriber email notifications and an X (Twitter) post
- **REST API** — full CRUD API with DRF token authentication, role-scoped querysets, and search/ordering
- **Subscriptions** — readers subscribe to publishers and journalists; a personalised feed surfaces only subscribed content
- **Newsletters** — journalists and editors curate collections of approved articles
- **Responsive UI** — sticky header with role-aware navigation, featured article hero, card grid homepage
- **38 unit tests** — covering all roles, permissions, signals (mocked), and model behaviour

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.11, Django 5.2 |
| REST API | Django REST Framework 3.17 |
| Database | PostgreSQL (via `DATABASE_URL`) / SQLite (fallback) |
| Auth | Django session auth (frontend) + DRF Token auth (API) |
| HTTP client | `requests` (Twitter/X integration) |
| Email | Django `send_mail` (console backend by default) |

---

## Project Structure

```
django-news/
├── news_project/               # Django project configuration
│   ├── settings.py             # Database, installed apps, DRF, email, Twitter config
│   ├── urls.py                 # Root URL routing
│   └── wsgi.py
│
├── newsapp/                    # Main application
│   ├── models.py               # User (custom), Publisher, Article, Newsletter
│   ├── views.py                # API ViewSets + template views
│   ├── serializers.py          # DRF serializers for all models
│   ├── permissions.py          # Custom DRF permission classes
│   ├── signals.py              # Group bootstrap, user→group assignment, approval signals
│   ├── forms.py                # SignUpForm, ArticleForm
│   ├── admin.py                # Admin configuration with bulk approve/unapprove
│   ├── apps.py                 # AppConfig (connects signals on startup)
│   ├── urls.py                 # REST API routes (/api/*)
│   ├── frontend_urls.py        # Template-based HTML routes
│   ├── tests.py                # 38 unit tests
│   ├── templates/newsapp/      # HTML templates
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── signup.html
│   │   ├── login.html
│   │   ├── article_list.html
│   │   ├── article_detail.html
│   │   ├── article_form.html
│   │   ├── article_approval.html
│   │   ├── newsletter_list.html
│   │   ├── my_feed.html
│   │   └── my_articles.html
│   └── management/commands/
│       └── seed_data.py        # Loads 20 demo articles + 4 demo accounts
│
├── requirements.txt
├── manage.py
└── .env.example
```

---

## Setup & Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd django-news
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy the example file and fill in your values:

```bash
cp .env.example .env
```

See [Environment Variables](#environment-variables) for details.

### 5. Apply migrations

```bash
python manage.py migrate
```

This also auto-creates the Reader, Journalist, and Editor permission groups via the `post_migrate` signal.

### 6. (Optional) Load demo data

```bash
python manage.py seed_data
```

Creates 4 demo accounts, 2 publishers, 20 approved articles, and 2 newsletters.

### 7. (Optional) Create a superuser

```bash
python manage.py createsuperuser
```

---

## Environment Variables

Create a `.env` file in the `django-news/` directory (next to `manage.py`):

```env
# Required for PostgreSQL. Remove to fall back to SQLite.
DATABASE_URL=postgresql://user:password@localhost:5432/newsdb

# Django secret key (generate a strong random value for production)
SECRET_KEY=your-secret-key-here

# Set to False in production
DEBUG=True

# Email backend (use console backend for development)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

# Required for article approval → email notifications
DEFAULT_FROM_EMAIL=noreply@newsapp.example.com

# Optional: X (Twitter) API v2 Bearer Token for approval tweets
# Leave blank to skip Twitter posting silently.
TWITTER_BEARER_TOKEN=
```

---

## Running the App

```bash
python manage.py runserver 0.0.0.0:8000
```

The app will be available at `http://localhost:8000`.

---

## Demo Accounts

Run `python manage.py seed_data` to create these accounts:

| Username | Password | Role |
|---|---|---|
| `reader_demo` | `demo1234` | Reader |
| `journalist_demo` | `demo1234` | Journalist |
| `journalist2_demo` | `demo1234` | Journalist |
| `editor_demo` | `demo1234` | Editor |

---

## User Roles & Permissions

### Reader
- View approved articles and all newsletters
- Subscribe to publishers and journalists
- Access a personalised "My Feed" of subscribed content
- **Cannot** create, edit, or delete any content

### Journalist
- Create, edit, and delete **their own** articles (new articles start unapproved)
- Create, edit, and delete **their own** newsletters
- View their own unapproved drafts
- **Cannot** approve articles

### Editor
- View, edit, and delete **any** article
- Approve and unapprove articles (triggers email + Twitter notifications)
- View, edit, and delete **any** newsletter
- Access the editorial approval dashboard
- **Cannot** create articles via the REST API (spec requirement)

### Group Assignment

Users are automatically assigned to the correct Django group on every save via a `post_save` signal. Switching roles (e.g. reader → journalist) updates the group assignment immediately and clears reader-only subscription data.

---

## Article Approval Workflow

1. A **journalist** creates an article — it starts with `approved = False`
2. The article appears in the journalist's "My Articles" dashboard but is hidden from readers
3. An **editor** visits `/articles/approval/` to see all pending articles
4. The editor clicks **Approve** — this sets `approved = True`, records `approved_by` and `approved_at`, and saves the article
5. The `post_save` signal fires two side-effects:
   - **Email** is sent to all readers subscribed to the article's publisher or author
   - **Tweet** is posted to X (Twitter) via the v2 API (if `TWITTER_BEARER_TOKEN` is set)
6. The article is now visible to all readers and appears on the homepage

---

## Django Signals

All signals are registered in `newsapp/signals.py` and connected in `NewsappConfig.ready()`.

| Signal | Sender | Purpose |
|---|---|---|
| `post_migrate` | Any | Creates Reader, Journalist, Editor groups with correct permissions |
| `post_save` | `User` | Assigns the saved user to the Django group matching their role |
| `post_save` | `Article` | On approval: sends subscriber emails + posts to Twitter/X |

### Signal functions (standalone for easy mocking in tests)

```python
send_approval_emails(article)  # Emails all subscribed readers
post_to_twitter(article)       # POSTs to https://api.twitter.com/2/tweets
```

---

## REST API Reference

All API endpoints require token authentication unless marked **Public**.

**Header format:**
```
Authorization: Token <your-token>
```

### Authentication

| Method | Endpoint | Access | Description |
|---|---|---|---|
| POST | `/api/auth/register/` | Public | Create account, returns token |
| POST | `/api/auth/login/` | Public | Authenticate, returns token |
| POST | `/api/auth/logout/` | Authenticated | Invalidate current token |

### Articles

| Method | Endpoint | Access | Description |
|---|---|---|---|
| GET | `/api/articles/` | All roles | List articles (role-filtered) |
| POST | `/api/articles/` | Journalist | Create a new article |
| GET | `/api/articles/<id>/` | All roles | Retrieve a single article |
| PUT / PATCH | `/api/articles/<id>/` | Journalist (own) / Editor | Update an article |
| DELETE | `/api/articles/<id>/` | Journalist (own) / Editor | Delete an article |
| GET | `/api/articles/subscribed/` | Reader | Articles from subscribed publishers/journalists |
| POST | `/api/articles/<id>/approve/` | Editor | Approve an article |
| POST | `/api/articles/<id>/unapprove/` | Editor | Retract approval |

**Query parameters (article list):**

| Parameter | Example | Description |
|---|---|---|
| `search` | `?search=django` | Search title, content, or author username |
| `ordering` | `?ordering=-created_at` | Sort by `created_at` or `title` |

### Newsletters

| Method | Endpoint | Access | Description |
|---|---|---|---|
| GET | `/api/newsletters/` | All roles | List all newsletters |
| POST | `/api/newsletters/` | Journalist / Editor | Create a newsletter |
| GET | `/api/newsletters/<id>/` | All roles | Retrieve a newsletter |
| PUT / PATCH | `/api/newsletters/<id>/` | Journalist (own) / Editor | Update a newsletter |
| DELETE | `/api/newsletters/<id>/` | Journalist (own) / Editor | Delete a newsletter |

### Publishers & Users

| Method | Endpoint | Access | Description |
|---|---|---|---|
| GET | `/api/publishers/` | Authenticated | List all publishers |
| GET | `/api/users/` | Journalist / Editor | List users |

### Example: Register and create an article

```bash
# Register
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "password": "secret123", "role": "journalist"}'

# Returns: { "token": "abc123...", "user": { ... } }

# Create an article
curl -X POST http://localhost:8000/api/articles/ \
  -H "Authorization: Token abc123..." \
  -H "Content-Type: application/json" \
  -d '{"title": "My First Article", "content": "Article body here."}'
```

---

## Frontend Routes

| URL | Description | Access |
|---|---|---|
| `/` | Homepage — latest 20 approved articles | Public |
| `/signup/` | Account creation with role selection | Public |
| `/login/` | Session login | Public |
| `/logout/` | Session logout | Authenticated |
| `/articles/` | Full article listing | Public |
| `/articles/new/` | Create article form | Journalist / Editor |
| `/articles/<id>/` | Article detail | Public (unapproved: author/editor only) |
| `/articles/<id>/edit/` | Edit article | Author / Editor |
| `/articles/<id>/delete/` | Delete article (POST) | Author / Editor |
| `/articles/approval/` | Editorial approval dashboard | Editor only |
| `/articles/<id>/approve/` | Approve article (POST) | Editor only |
| `/articles/<id>/unapprove/` | Unapprove article (POST) | Editor only |
| `/newsletters/` | Newsletter listing | Public |
| `/my-feed/` | Personalised reader feed | Reader only |
| `/subscribe/publisher/<id>/` | Toggle publisher subscription | Reader only |
| `/subscribe/journalist/<id>/` | Toggle journalist subscription | Reader only |
| `/my-articles/` | Article management table | Journalist / Editor |
| `/admin/` | Django admin site | Staff / Superuser |

---

## Running Tests

```bash
python manage.py test newsapp
```

For verbose output (shows each test's docstring):

```bash
python manage.py test newsapp --verbosity=2
```

**Test coverage (38 tests):**

| Class | Tests | Coverage |
|---|---|---|
| `AuthenticationTests` | 7 | Login, registration, role-based article visibility |
| `ReaderTests` | 3 | Read-only enforcement, subscribed feed endpoint |
| `JournalistTests` | 6 | Create/edit own articles, cannot edit others, cannot approve |
| `EditorTests` | 7 | Approve/unapprove, full content management, approval template |
| `NewsletterTests` | 5 | Visibility, creation permissions, article association |
| `SignalTests` | 6 | Email dispatch, Twitter posting, failure handling (all mocked) |
| `ModelTests` | 4 | Role properties, subscription clearing, `is_independent` |

---

## Database

The app uses **PostgreSQL** when `DATABASE_URL` is set, and falls back to **SQLite** for local development without a database server.

```bash
# Apply migrations
python manage.py migrate

# Create new migrations after model changes
python manage.py makemigrations newsapp
```

To use MySQL/MariaDB instead, update the `DATABASES` engine in `settings.py`:

```python
"ENGINE": "django.db.backends.mysql"
```
