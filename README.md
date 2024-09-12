# ETL Pipeline

## Overview

This project is an ETL (Extract, Transform, Load) pipeline that retrieves data from specified websites, processes it, and stores it into a PostgreSQL database. The project uses Docker for containerization and Apache Airflow for orchestration.

## Features

- **Data Extraction:** Scrapes data from specified URLs.
- **Data Transformation:** Counts occurrences of specified keywords in the extracted data.
- **Data Loading:** Inserts the processed data into a PostgreSQL database.
- **Containerization:** Uses Docker to manage environments.
- **Orchestration:** Uses Apache Airflow to schedule and manage the pipeline runs.

## Project Structure


## Installation

### Prerequisites

- Docker
- Docker Compose

### Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd etl_pipeline

2. Buid and start Docker containers:
     ```bash

    docker compose up -d

3. Verify that the containers are running:
    ```bash
    docker compose ps -a


### Configuration



### Usage

Airflow - http://localhost:8080
1.

Grafana - http://localhost:3000
1. default login: admin/admin
2. If new password is asked then skip 
3. Open Dashboards -> `keywords_dashboard`
