FROM python:3.12.3-slim

# Set the working directory
WORKDIR /app

# Install required packages for PostgreSQL and other dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy and install dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt \
    && rm -rf /tmp

# Copy the entire application code
COPY . .

# Set the environment variable for the port
ENV PORT 5000

# Expose the port
EXPOSE $PORT

# Run the application
CMD gunicorn hbnb:app -w 2 -b 0.0.0.0:$PORT

