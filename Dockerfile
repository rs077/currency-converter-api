# Use official Python image
FROM python:3.13-slim

# Set work directory
WORKDIR /app

# Copy requirements (you can freeze manually with pip freeze > requirements.txt)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project
COPY . .

# Expose default port
EXPOSE 8000

# Run server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
