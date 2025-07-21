# Use official Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies (optional, e.g., for psycopg2 or other packages)
# RUN apt-get update && apt-get install -y build-essential

# Copy requirements.txt and install dependencies
COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY backend/ .

# Expose port 8000 for FastAPI
EXPOSE 8000

# Run the FastAPI app with uvicorn
# Assumes the app is in app/main.py and the FastAPI instance is named 'app'
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 