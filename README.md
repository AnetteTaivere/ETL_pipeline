# ETL Pipeline

## Overview

This project is an ETL (Extract, Transform, Load) pipeline that retrieves data from 2 websites. 

## Features

- **Data Extraction:** Scrapes data from https://www.ft.com/ and https://www.theguardian.com/europe.
- **Data Transformation:** Counts occurrences of `election, war, economy` keywords in the extracted data.
- **Data Loading:** Inserts the processed data into a PostgreSQL database.
- **Containerization:** The project uses Docker for containerization.
- **Scheduling:** Uses Apache Airflow to schedule and manage the pipeline runs.

## Project Structure


## Installation

- Docker
- Docker Compose

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/AnetteTaivere/ETL_pipeline.git
   cd etl_pipeline

2. Buid and start Docker containers:
     ```bash
    docker compose up -d

3. Verify that the containers are running:
    ```bash
    docker compose ps -a


### Configuration


1. Generate FERNET_KEY value using
`python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"`
2. Add key to AIRFLOW__CORE__FERNET_KEY

3. You also need to create airflow user. For this, take the webserver's docker container id, and go into the container.
`docker exec -it <CONTAINER_ID> /bin/bash` 
In the container create new user with following command.
`airflow users create --username admin --password admin --firstname First --lastname Last --role Admin --email admin@example.com`


### Usage

Airflow - http://localhost:8080
1. Login with created user
2. Check for two running DAGs. Depending on the day, main.py is scheduled to run at the next available hour or the hour after.

Grafana - http://localhost:3000
1. default login: admin/admin
2. If new password is asked then skip 
3. Open Dashboards -> `keywords_dashboard`
4. See data (only there is one of the dags have run)
