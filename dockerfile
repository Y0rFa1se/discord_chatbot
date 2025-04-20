# Base image
FROM python:3.13-alpine

# Set working directory
WORKDIR /app

# Copy application code and config file into container
COPY . /app

# Install any required Python dependencies (if needed)
RUN pip install --no-cache-dir -r requirements.txt

# Run the Python application
CMD ["python", "chatbot.py"]
