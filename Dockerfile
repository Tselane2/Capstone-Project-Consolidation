# Use a lightweight official Python image
FROM python:3.10-slim

# Prevent Python from writing .pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Copy dependency list first (better caching)
COPY requirements.txt /app/

# Upgrade pip and install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the rest of the project files
COPY . /app/

# Expose port 8000 for Django
EXPOSE 8000

# Run migrations and start the Django development server
# Note: MariaDB must be running and accessible (either locally or via Docker Compose)
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
