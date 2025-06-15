# Use official Python image
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

COPY data.csv /app/data.csv

# Default command
CMD ["gunicorn", "hotel_project.wsgi:application", "--bind", "0.0.0.0:8000"]

RUN python manage.py collectstatic --noinput
