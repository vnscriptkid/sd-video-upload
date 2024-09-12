# FROM apache/airflow:2.0.1
# COPY requirements.txt /requirements.txt
# RUN pip install --user --upgrade pip
# RUN pip install --no-cache-dir --user -r /requirements.txt

# Use the official Apache Airflow image as a base
FROM apache/airflow:2.10.1

# Install dependencies from requirements.txt
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt