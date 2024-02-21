# Use Python 3.11 base image from Alpine Linux
FROM python:3.11-alpine AS builder

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /root

# Copy the project's requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Install system dependencies
RUN apk update && apk add --no-cache \
    curl \
    gcc \
    libc-dev \
    linux-headers

# Final image
FROM python:3.11-alpine

WORKDIR /opt/app

# Install Unit and necessary packages
RUN apk add --no-cache unit unit-python3 curl

# Copy installed Python packages from the builder stage
COPY --chown=unit --from=builder /root/.local /opt/.local
ENV PATH=/opt/.local/bin:$PATH
ENV PYTHONPATH=/opt/.local/lib/python3.11/site-packages:$PYTHONPATH

# Copy the application code to the container
COPY --chown=unit ./app .
COPY ./django.unit.json ./django-entrypoint.sh /docker-entrypoint.d/
COPY ./unit-docker-entrypoint.sh /usr/local/bin/

# Make entrypoint scripts executable
RUN chmod +x /usr/local/bin/unit-docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.d/django-entrypoint.sh

# Set the entrypoint to the Unit startup script
ENTRYPOINT ["/usr/local/bin/unit-docker-entrypoint.sh"]

# Expose the port the app runs on
EXPOSE 8300

# Start Unit in non-daemon mode with specified control socket
CMD ["unitd", "--no-daemon", "--control", "unix:/var/run/control.unit.sock"]
