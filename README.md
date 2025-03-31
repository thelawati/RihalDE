# Rihal Crime Data Analytics Pipeline
Data Engineering Codestacker Ramadhan Challenge 1446 2025
This project provides a complete data analytics pipeline including ETL (Extract, Transform, Load), PostgreSQL database storage, and an interactive Streamlit dashboard for visualizing crime data.

## Project Structure
pgsql
Copy
Edit
project-root/
├── db/
│   └── init.sql
├── etl/
│   ├── etl.py
│   ├── crime_records.json
│   ├── district_info.pdf
│   └── requirements.txt
├── app/
│   ├── dashboard.py
│   └── requirements.txt
├── docker-compose.yml
├── etl.Dockerfile
└── app.Dockerfile

## Dockerized Components
PostgreSQL database: Stores cleaned and integrated crime data.

ETL Container: Extracts, cleans, transforms, and loads data into PostgreSQL.

Dashboard Container (Streamlit): Visualizes insights derived from the database.

## Quick Start
1. Ensure Docker Compose is installed

docker compose version

2. Launch the pipeline
Navigate to the project root and run:

docker compose up --build

This command does the following:

  a. Builds and starts all services (PostgreSQL, ETL, and dashboard).
  
  b. Loads data into the PostgreSQL database via ETL.
  
  c. Runs the Streamlit dashboard at http://localhost:8501

3. Access the Dashboard
Open your browser and visit:
http://localhost:8501


## Dashboard Features
Basic visuals and adnswers to project questions.


## Troubleshooting
If you encounter connection errors, verify your database URL is correctly set:

DB_URL: postgresql://admin:admin@db:5432/rihal_de
Ensure no local services conflict with Docker ports (5432, 8501). Adjust docker-compose.yml as needed.

