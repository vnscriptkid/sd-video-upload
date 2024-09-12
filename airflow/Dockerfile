# Use the official Apache Airflow image as a base
FROM apache/airflow:2.10.1

# Switch to root user to install system packages
USER root

# Update and install system packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Switch back to the airflow user
USER airflow

# Install dependencies from requirements.txt
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt



# ... rest of your Dockerfile ...