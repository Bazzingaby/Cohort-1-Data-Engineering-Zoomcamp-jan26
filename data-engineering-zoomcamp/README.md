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

## Module 1 Homework: Docker & SQL

In this homework we'll prepare the environment and practice Docker and SQL.

### Question 1. 
- Answer ::25.3  
ran "pip --version" inside container


### Question 2. 
- Answer::  db:5432
- container network port is 5432, not using local host here, and session name is db




### Prepare the Data

- added files and folder in repo to ingest data for the 2 files

### Question 3. Counting short trips

For the trips in November 2025 (lpep_pickup_datetime between '2025-11-01' and '2025-12-01', exclusive of the upper bound), how many trips had a `trip_distance` of less than or equal to 1 mile?

- 7,853
- 8,007
- 8,254
- 8,421

- Solution : 
### SQL
select * from green_taxi_trips  where
lpep_pickup_datetime>='2025-11-01' and lpep_pickup_datetime<'2025-12-01' and trip_distance <='1.0'; --8007 rows

Answer:: 8007


### Question 4. Longest trip for each day

Which was the pick up day with the longest trip distance? Only consider trips with `trip_distance` less than 100 miles (to exclude data errors).

Use the pick up time for your calculations.

- 2025-11-14
- 2025-11-20
- 2025-11-23
- 2025-11-25

- Solution : 
### SQL
SELECT DATE(lpep_pickup_datetime) AS pickup_day, MAX(trip_distance) AS max_distance
FROM green_taxi_trips
WHERE trip_distance < 100
GROUP BY pickup_day
ORDER BY max_distance DESC
; --2025-11-14 

Answer:: 2025-11-14


### Question 5. Biggest pickup zone

Which was the pickup zone with the largest `total_amount` (sum of all trips) on November 18th, 2025?

- East Harlem North
- East Harlem South
- Morningside Heights
- Forest Hills

- Solution: 
select "PULocationID",sum(fare_amount),"Zone"
	FROM green_taxi_trips
	join taxi_zones
	on "PULocationID"="LocationID"
where date(lpep_pickup_datetime)='2025-11-18'
	group by "PULocationID","Zone"
	order by 2 desc;--East Harlem North

"PULocationID"	"sum"	"Zone"
74	6555.319999999998	"East Harlem North"


Answer: - East Harlem North


### Question 6. Largest tip

For the passengers picked up in the zone named "East Harlem North" in November 2025, which was the drop off zone that had the largest tip?

Note: it's `tip` , not `trip`. We need the name of the zone, not the ID.

- JFK Airport
- Yorkville West
- East Harlem North
- LaGuardia Airport

- solution 
select c."Zone","tip_amount",*
FROM green_taxi_trips a
	left join taxi_zones b 	on a."PULocationID"=b."LocationID"
	left join taxi_zones c on a."DOLocationID"=c."LocationID"
	where b."Zone"='East Harlem North'
	and date(lpep_pickup_datetime)>='2025-11-01' and date(lpep_pickup_datetime)<'2025-12-01'
	order by "tip_amount" desc;
	--"Yorkville West"  : 81.89 

-Answer :: Yorkville West


### Terraform

terraform init , plan , approve and destroy completed with creation of GCP bucket

### Question 7. Terraform Workflow

Which of the following sequences, respectively, describes the workflow for:
1. Downloading the provider plugins and setting up backend,
2. Generating proposed changes and auto-executing the plan
3. Remove all resources managed by terraform`

Answers:

- terraform init, terraform apply -auto-approve, terraform destroy


