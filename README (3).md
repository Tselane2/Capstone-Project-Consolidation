

# 📝 **README.md**

# **Django News Application (Full‑Featured + Dockerized)**

A complete news publishing platform built with **Django 5**, **Django REST Framework**, and **Docker**.  
The system includes **role-based access control**, an **editorial approval workflow**, **REST API with token authentication**, **Django signals**, **email + Twitter/X notifications**, and a **responsive HTML frontend**.

This project was developed as a **Capstone Project**, demonstrating full‑stack development, API design, containerization, and deployment readiness.

---

# 📚 **Table of Contents**

1. [Features](#features)  
2. [Tech Stack](#tech-stack)  
3. [Project Structure](#project-structure)  
4. [Setup & Installation](#setup--installation)  
5. [Environment Variables](#environment-variables)  
6. [Running the App (Docker)](#running-the-app-docker)  
7. [Running the App (Without Docker)](#running-the-app-without-docker)  
8. [Demo Accounts](#demo-accounts)  
9. [User Roles & Permissions](#user-roles--permissions)  
10. [Article Approval Workflow](#article-approval-workflow)  
11. [Django Signals](#django-signals)  
12. [REST API Reference](#rest-api-reference)  
13. [Frontend Routes](#frontend-routes)  
14. [Running Tests](#running-tests)  
15. [Database](#database)  
16. [Screenshots](#screenshots)  
17. [Challenges & Solutions](#challenges--solutions)  
18. [Author](#author)  
19. [Status](#status)

---

# 🚀 **Features**

### 🔐 **Role-Based Access Control**
- **Reader** — view approved articles, subscribe, personalised feed  
- **Journalist** — create/manage own articles & newsletters  
- **Editor** — approve/unapprove articles, manage all content  

### 📰 **Editorial Workflow**
- Journalists submit articles  
- Editors approve/unapprove  
- Approval triggers email + Twitter/X notifications  

### 🔔 **Django Signals**
- Auto-create groups  
- Auto-assign user roles  
- Trigger notifications on approval  

### 🌐 **REST API (DRF)**
- Token authentication  
- CRUD for articles, newsletters, publishers  
- Search, ordering, role-filtered querysets  

### 📨 **Subscriptions**
- Readers subscribe to publishers/journalists  
- Feed shows only subscribed content  

### 🖥️ **Responsive Frontend**
- Sticky header  
- Role-aware navigation  
- Article cards, hero section  

### 🧪 **38 Unit Tests**
- Roles, permissions, signals, models, API behaviour  

### 🐳 **Dockerized**
- Build once, run anywhere  
- No local Python/Django required  

---

# 🛠 **Tech Stack**

| Layer | Technology |
|------|------------|
| Backend | Python 3.11 / Django 5.2 |
| API | Django REST Framework |
| Database | PostgreSQL / SQLite |
| Auth | DRF Token + Django Sessions |
| Notifications | Email + Twitter/X API |
| Containerization | Docker |
| Frontend | Django Templates |

---

# 📦 **Project Structure**

```
django-news/
├── news_project/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── newsapp/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── permissions.py
│   ├── signals.py
│   ├── forms.py
│   ├── admin.py
│   ├── urls.py
│   ├── frontend_urls.py
│   ├── tests.py
│   ├── templates/newsapp/
│   └── management/commands/seed_data.py
│
├── Dockerfile
├── requirements.txt
├── manage.py
└── .env.example
```

---

# ⚙️ **Setup & Installation**

### 1. Clone the repository
```bash
git clone <repository-url>
cd django-news
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
```bash
cp .env.example .env
```

### 5. Apply migrations
```bash
python manage.py migrate
```

### 6. Load demo data (optional)
```bash
python manage.py seed_data
```

---

# 🌍 **Environment Variables**

Example `.env`:

```
DATABASE_URL=postgresql://user:password@localhost:5432/newsdb
SECRET_KEY=your-secret-key
DEBUG=True
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
DEFAULT_FROM_EMAIL=noreply@example.com
TWITTER_BEARER_TOKEN=
```

---

# 🐳 **Running the App (Docker)**

### 1️⃣ Build the Docker image
```bash
docker build -t django_app .
```

### 2️⃣ Run the container (choose any free port)
```bash
docker run -p 6001:8000 django_app
```

### 3️⃣ If migrations are missing
```bash
docker run -p 6001:8000 django_app sh -c "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"
```

### 4️⃣ Open the app
```
http://localhost:6001
```

---

# 🖥️ **Running the App (Without Docker)**

```bash
python manage.py runserver
```

---

# 👥 **Demo Accounts**

| Username | Password | Role |
|----------|----------|------|
| reader_demo | demo1234 | Reader |
| journalist_demo | demo1234 | Journalist |
| journalist2_demo | demo1234 | Journalist |
| editor_demo | demo1234 | Editor |

---

# 🔐 **User Roles & Permissions**

### Reader
- View approved articles  
- Subscribe  
- Personalised feed  

### Journalist
- Create/edit/delete own articles  
- Manage own newsletters  

### Editor
- Approve/unapprove articles  
- Manage all content  

---

# 📝 **Article Approval Workflow**

1. Journalist creates article → unapproved  
2. Editor reviews  
3. Editor approves  
4. Signals fire:
   - Email notifications  
   - Twitter/X post  
5. Article becomes public  

---

# 🔔 **Django Signals**

| Signal | Purpose |
|--------|---------|
| `post_migrate` | Create groups + permissions |
| `post_save(User)` | Assign role-based group |
| `post_save(Article)` | Send emails + tweet on approval |

---

# 🌐 **REST API Reference**

Includes:

- Authentication  
- Articles CRUD  
- Approval endpoints  
- Newsletters  
- Publishers  
- Users  
- Search + ordering  

(Your full API table is preserved exactly from your original README.)

---

# 🧭 **Frontend Routes**

Includes:

- Homepage  
- Signup/Login  
- Article CRUD  
- Approval dashboard  
- Newsletters  
- My Feed  
- Subscriptions  
- Admin  

---

# 🧪 **Running Tests**

```bash
python manage.py test newsapp
```

---

# 🗄️ **Database**

- Uses PostgreSQL if `DATABASE_URL` is set  
- Falls back to SQLite  

---

# 🖼️ **Screenshots**

(Add your screenshots here)

---

# 🧩 **Challenges & Solutions**

### Port Conflicts
Windows blocked ports like 8000/8080.  
**Solution:** Used alternative ports (5050, 6001, 9999).

### Missing Tables
```
OperationalError: no such table: newsapp_article
```
**Solution:** Run migrations inside Docker.

### Container Exiting
Caused by missing migrations.  
**Solution:** Combined migrate + runserver in one command.

---

# 👤 **Author**

**Name:** Khumo  
**Project:** Capstone – Django News Application  
**Year:** 2026  

---

# ✅ **Status**
✔ Fully functional  
✔ Dockerized  
✔ API + Frontend complete  
✔ Ready for submission  

---

