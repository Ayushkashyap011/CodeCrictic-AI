FROM python:3.11-slim

# Install Java, g++ for C++, and other tools
RUN apt-get update && apt-get install -y \
    default-jdk \
    g++ \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV PORT=8000

# Run the application
CMD ["python", "run.py"]
