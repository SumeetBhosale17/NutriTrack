# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app
COPY . .

# Expose port
EXPOSE 5000

# Use Flask’s debug mode for hot-reload during development
ENV FLASK_APP=manage.py
ENV FLASK_ENV=development

# Default command: run migrations then start Gunicorn
CMD bash -c "flask db upgrade && gunicorn wsgi:app --bind 0.0.0.0:5000 --workers 3"
