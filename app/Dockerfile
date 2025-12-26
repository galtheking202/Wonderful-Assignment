FROM python:3.11-slim

WORKDIR /app

# Install pip packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose app port if needed (for example, if you have a web UI)
EXPOSE 8888

# Start the Python app
CMD ["python3", "main.py"]
