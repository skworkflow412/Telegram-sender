# Use official Python image
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port for Koyeb
EXPOSE 8080

# Start Flask app with Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
