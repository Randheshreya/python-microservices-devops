# Use slim Python base image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Install dependencies first (layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the frontend code
COPY . .

# Set environment
ENV PYTHONUNBUFFERED=1

# Expose port 8080
EXPOSE 8080

# Run with Gunicorn for production
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
