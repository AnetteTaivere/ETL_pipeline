FROM apache/airflow:2.7.2-python3.10

ENV PYTHONPATH=/opt/airflow

WORKDIR /app

COPY requirements.txt .
COPY app/* /app
COPY dags/ /opt/airflow/dags/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Env vars
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# For Postgresql 
EXPOSE 5432

# For Airflow
EXPOSE 8080


# Command to run
CMD ["airflow", "webserver"]