FROM python:3.11-slim

# Install MongoDB
FROM mongo:7.0


WORKDIR /app

# Copy files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Make data directory
RUN mkdir -p /data/db

# Expose MongoDB port
EXPOSE 27017

# Start Python script (starts MongoDB internally)
CMD ["python", "main.py"]
