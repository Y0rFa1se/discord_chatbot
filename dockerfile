# Base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy application code and config file into container
COPY app/ /app/

# Install any required Python dependencies (if needed)
RUN pip install -r requirements.txt

# Run the Python application
CMD ["python", "chatbot.py"]
