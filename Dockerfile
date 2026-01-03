# Use Python 3.10 slim image (good balance of size/compatibility)
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install required system dependencies for OpenCV and image processing
# libgl1-mesa-glx: Required for opencv (used by rembg/transparent-background)
# libglib2.0-0: Required for opencv
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
# --no-cache-dir reduces image size
RUN pip install --no-cache-dir -r requirements.txt

# Create a home directory for model downloads (so they persist if verified, but mainly for permission)
ENV HOME=/app

# Copy the rest of the application code
COPY . .

# Expose the port Flask runs on
EXPOSE 5000

# Run with Gunicorn
# timeout 120: AI models can take time to process, so we increase the timeout
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--timeout", "120", "main:app"]
