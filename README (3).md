
---

# 📝 **README.md**

# **Django News Application (Dockerized)**

A simple news management web application built with **Django**, featuring user roles (Reader, Journalist, Editor), article management, authentication, and a clean Dockerized setup for easy deployment and testing.

This project was created as part of the **Capstone Project**, demonstrating full‑stack development, containerization, and deployment readiness.

---

## 🚀 **Features**

### **👤 User Roles**
- **Reader** – Can view published articles  
- **Journalist** – Can create and manage their own articles  
- **Editor** – Can approve, reject, or publish articles  

### **📰 Article Management**
- Create, edit, delete articles  
- Role‑based permissions  
- Article approval workflow  
- Homepage displaying published articles  

### **🔐 Authentication**
- User registration  
- Login / Logout  
- Role‑based access control  

### **🐳 Dockerized Application**
- Fully containerized Django app  
- Runs with a single Docker command  
- No need to install Python or Django locally  

---

## 🛠 **Tech Stack**

| Component | Technology |
|----------|------------|
| Backend | Django 5.2 |
| Database | SQLite (inside Docker) |
| Containerization | Docker |
| Language | Python 3.12 |
| Frontend | Django Templates (HTML, CSS) |

---

## 📦 **Project Structure**

```
django-news/
│
├── news_project/        # Main Django project
├── newsapp/             # Application with models, views, templates
├── templates/           # HTML templates
├── Dockerfile           # Docker configuration
├── requirements.txt     # Python dependencies
└── manage.py
```

---

## 🐳 **Running the Project with Docker**

### **1️⃣ Build the Docker image**
```
docker build -t django_app .
```

### **2️⃣ Run the container**
Use any free port (example: 6001):

```
docker run -p 6001:8000 django_app
```

### **3️⃣ Apply migrations inside Docker**
If you see “no such table” errors, run:

```
docker run -p 6001:8000 django_app sh -c "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"
```

### **4️⃣ Open the website**
```
http://localhost:6001
```

---

## 🧪 **Running the Project Without Docker (Optional)**

### **1. Create virtual environment**
```
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

### **2. Install dependencies**
```
pip install -r requirements.txt
```

### **3. Apply migrations**
```
python manage.py migrate
```

### **4. Run the server**
```
python manage.py runserver
```

---

## 🖼 **Screenshots**

(Add your screenshots here)

Example:

```
![Homepage](screenshots/homepage.png)
![Docker Running](screenshots/docker.png)
```

---

## 🧩 **Challenges & Solutions**

### **Port Conflicts**
Windows blocked ports like 8000 and 8080.  
**Solution:** Used alternative ports (5050, 6001, 9999).

### **Missing Database Tables**
Django raised:
```
OperationalError: no such table: newsapp_article
```
**Solution:** Run migrations inside Docker.

### **Container Exiting Immediately**
Caused by missing migrations.  
**Solution:** Combined migrate + runserver in one Docker command.

---

## 👤 **Author**

**Name:** Khumo  
**Project:** Capstone – Django News Application  
**Year:** 2026  

---

## ✅ **Status**
✔ Fully functional  
✔ Dockerized  
✔ Ready for submission  

---

