
# Django News Application

📌 **Repository Link:**  
👉 https://github.com/Tselane2/Capstone-Project-Consolidation/tree/main

📌 **Docker Run Link (local):**  
👉 http://localhost:8000/

A full‑featured news publishing platform built with **Django 5**, **Django REST Framework**, and a clean role‑based permission system.  
Supports **Readers**, **Journalists**, and **Editors**, each with distinct capabilities, an editorial approval workflow, newsletters, subscriptions, and automated notifications via Django signals.

The project includes:

- A complete REST API with token authentication  
- A responsive HTML frontend  
- A Sphinx documentation system  
- Dockerized backend  
- 38 unit tests covering permissions, signals, models, and workflows  

---

## 📦 Features

- Role‑based access control  
- Editorial approval workflow  
- Django signals (email + Twitter)  
- Newsletters  
- REST API with token auth  
- Subscriptions + personalised feed  
- Responsive UI  
- Docker containerization  
- Sphinx documentation  
- 38 unit tests  

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Django 5.2, Python 3.11 |
| API | Django REST Framework 3.17 |
| Database (dev) | SQLite |
| Database (prod) | MariaDB/MySQL |
| Auth | DRF Token + Django session |
| Notifications | Django `send_mail`, Twitter API v2 |
| Docs | Sphinx 9.1 |
| Containerization | Docker |

---

## 📥 Clone the Repository

📌 **Repository Link:**  
👉 https://github.com/Tselane2/Capstone-Project-Consolidation/tree/main

```bash
git clone https://github.com/Tselane2/Capstone-Project-Consolidation.git
cd Capstone-Project-Consolidation/django-news
```

---

# 🐳 Dockerized Setup

This project includes a working **Dockerfile** that builds and runs the Django application inside a container.

## 1. Build the Docker image

```bash
docker build -t tselane2/django-news .
```

## 2. Run the container

```bash
docker run -p 8000:8000 tselane2/django-news
```

Your app will be available at:

👉 **http://localhost:8000/**

## 3. Push to Docker Hub

```bash
docker login
docker push tselane2/django-news
```

## 4. Test on Play‑With‑Docker

👉 [https://labs.play-with-docker.com/](https://labs.play-with-docker.com/)

```bash
docker run -p 8000:8000 tselane2/django-news
```

---

# 🧪 Virtual Environment (non‑Docker setup)

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

# 🔐 Environment Variables (.env)

```bash
cp .env.example .env
```

Fill in:

- SECRET_KEY  
- EMAIL_BACKEND  
- DEFAULT_FROM_EMAIL  
- TWITTER_BEARER_TOKEN  

---

# 🗄 Database Setup

SQLite is default — no setup needed.

---

# 🔧 Apply Migrations

```bash
python manage.py makemigrations newsapp
python manage.py migrate
```

---

# ▶️ Run the Server

```bash
python manage.py runserver
```

---

# 🧭 Project Structure

```
django-news/
│
├── news_project/
├── newsapp/
├── docs/                  # Sphinx documentation
├── Dockerfile             # Docker build file
├── requirements.txt
└── README.md
```

---

# 🧑‍💻 User Roles & Permissions

### Reader
- View approved articles  
- View all newsletters  
- Subscribe to publishers/journalists  

### Journalist
- Create/edit/delete **own** articles  
- Create/edit/delete **own** newsletters  

### Editor
- Approve/unapprove articles  
- Manage **all** content  
- Access approval dashboard  

---

# 📰 Article Approval Workflow

1. Journalist creates article  
2. Editor reviews  
3. Editor approves  
4. Signals fire (email + Twitter)  
5. Article becomes public  

---

# 📡 REST API Overview

### Authentication
| Method | Endpoint |
|--------|----------|
| POST | `/api/auth/register/` |
| POST | `/api/auth/login/` |
| POST | `/api/auth/logout/` |

### Articles
| Method | Endpoint | Access |
|--------|----------|--------|
| GET | `/api/articles/` | All roles |
| POST | `/api/articles/` | Journalist |
| PATCH | `/api/articles/<id>/` | Journalist (own) / Editor |
| DELETE | `/api/articles/<id>/` | Journalist (own) / Editor |
| POST | `/api/articles/<id>/approve/` | Editor |
| POST | `/api/articles/<id>/unapprove/` | Editor |

---

# 🧪 Running Tests

```bash
python manage.py test newsapp
```

---

# 📘 Building Sphinx Documentation

```bash
sphinx-build -b html docs/source docs/build
```

---


