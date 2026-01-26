# Data Engineering Zoomcamp

This project ingests NYC green taxi trips data (November 2025) and taxi zones into a PostgreSQL database. It uses Docker containers for PostgreSQL and pgAdmin, with a Python script for data ingestion.

## Project Structure

```
data-engineering-zoomcamp/
├── docker-compose.yml
├── Dockerfile
├── src/
│   ├── ingest.py
│   └── utils.py
├── requirements.txt
├── pyproject.toml
├── .gitignore
└── README.md
```

## Prerequisites

- Docker installed and running.
- Python 3.9+ (for local venv).

## Setup and Execution Steps

1. **Clone and Navigate**:
   ```bash
   git clone <repository-url>
   cd data-engineering-zoomcamp
   ```

2. **Create Docker Network** (for container communication):
   ```bash
   docker network create mynetwork
   ```

3. **Start PostgreSQL Container**:
   ```bash
   docker run -d --name postgres --network mynetwork \
     -e POSTGRES_USER=postgres \
     -e POSTGRES_PASSWORD=postgres \
     -e POSTGRES_DB=ny_taxi \
     -p 5433:5432 \
     postgres:latest
   ```

4. **Start pgAdmin Container**:
   ```bash
   docker run -d --name pgadmin --network mynetwork \
     -e PGADMIN_DEFAULT_EMAIL=admin@admin.com \
     -e PGADMIN_DEFAULT_PASSWORD=admin \
     -p 8080:80 \
     dpage/pgadmin4:latest
   ```

5. **Set Up Python Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

6. **Run Data Ingestion**:
   ```bash
   python src/ingest.py
   ```
   This downloads and loads ~46,912 green taxi rows and ~265 zone rows into PostgreSQL.

7. **Access pgAdmin**:
   - Open `http://localhost:8080` in browser.
   - Login: `admin@admin.com` / `admin`.
   - Add Server:
     - Name: `ny_taxi_db`
     - Host: `postgres`
     - Port: `5432`
     - Username: `postgres`
     - Password: `postgres`
     - Database: `ny_taxi`
   - Connect and query tables (e.g., `SELECT COUNT(*) FROM green_taxi_trips;`).

## Verification

- Check containers: `docker ps`
- View data: `docker exec postgres psql -U postgres -d ny_taxi -c "SELECT COUNT(*) FROM green_taxi_trips;"`
- Logs: `docker logs postgres` or `docker logs pgadmin`

## Cleanup

- Stop containers: `docker stop postgres pgadmin`
- Remove: `docker rm postgres pgadmin`
- Remove network: `docker network rm mynetwork`

## Dependencies

- `pandas`, `sqlalchemy`, `psycopg2-binary`, `click`, `tqdm`, `pyarrow` (in `requirements.txt`).
- Installed in Docker image or local venv.

## Notes

- Data sources: Green taxi Parquet from AWS, zones CSV from GitHub.
- Modify `ingest.py` for different dates/files.
- Ensure ports 5433/8080 are free.
- For Windows/Mac, use `host.docker.internal` if needed in pgAdmin host.

This setup is reproducible and handles data ingestion without errors.