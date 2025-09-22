FROM python:3.11-slim

WORKDIR /app

# Copy all files
COPY . .

# Install dependencies directly (avoiding requirements.txt issues)
RUN pip install --no-cache-dir Flask==2.3.3 Werkzeug==2.3.7 requests==2.31.0 gunicorn==21.2.0

# Create uploads directory
RUN mkdir -p uploads

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Expose port
EXPOSE 5000

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
