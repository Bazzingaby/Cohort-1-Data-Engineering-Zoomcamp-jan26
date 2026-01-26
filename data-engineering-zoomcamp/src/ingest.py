#!/usr/bin/env python
# coding: utf-8

import click
import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm

# Data types for green taxi data (adapted from yellow taxi, with additions for green)
dtype_green = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64",
    "ehail_fee": "float64",  # Specific to green taxi
    "trip_type": "Int64"     # Specific to green taxi
}

parse_dates_green = [
    "lpep_pickup_datetime",
    "lpep_dropoff_datetime"
]

@click.command()
@click.option('--pg-user', default='postgres', help='PostgreSQL user')
@click.option('--pg-pass', default='postgres', help='PostgreSQL password')
@click.option('--pg-host', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', default=5433, type=int, help='PostgreSQL port')
@click.option('--pg-db', default='ny_taxi', help='PostgreSQL database name')
@click.option('--green-url', default='https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-11.parquet', help='URL for green taxi Parquet data')
@click.option('--green-table', default='green_taxi_trips', help='Target table name for green taxi data')
@click.option('--zones-url', default='https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv', help='URL for taxi zones CSV data')
@click.option('--zones-table', default='taxi_zones', help='Target table name for taxi zones data')
@click.option('--zones-chunksize', default=100000, type=int, help='Chunk size for reading zones CSV (if large)')
def run(pg_user, pg_pass, pg_host, pg_port, pg_db, green_url, green_table, zones_url, zones_table, zones_chunksize):
    """Ingest green taxi Parquet and taxi zones CSV data into PostgreSQL database."""
    engine = create_engine(f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')

    # Ingest green taxi Parquet data in chunks
    print(f"Ingesting green taxi data from {green_url} into {green_table}...")
    df_green = pd.read_parquet(green_url)
    
    # Apply data types and parse dates (fixes: dtypes and dates were defined but not used)
    df_green = df_green.astype(dtype_green)
    for col in parse_dates_green:
        df_green[col] = pd.to_datetime(df_green[col])
    
    first = True
    chunksize = 100000
    for i in tqdm(range(0, len(df_green), chunksize)):
        df_chunk = df_green.iloc[i:i + chunksize]
        
        if first:
            df_chunk.head(0).to_sql(
                name=green_table,
                con=engine,
                if_exists='replace'
            )
            first = False
        
        df_chunk.to_sql(
            name=green_table,
            con=engine,
            if_exists='append',
            index=False
        )
    print(f"Green taxi data ingested successfully.")

    # Ingest taxi zones CSV data (use chunks if needed, but assuming small file)
    print(f"Ingesting taxi zones data from {zones_url} into {zones_table}...")
    df_iter = pd.read_csv(
        zones_url,
        iterator=True,
        chunksize=zones_chunksize,
    )

    first = True
    for df_chunk in tqdm(df_iter):
        if first:
            df_chunk.head(0).to_sql(
                name=zones_table,
                con=engine,
                if_exists='replace'
            )
            first = False

        df_chunk.to_sql(
            name=zones_table,
            con=engine,
            if_exists='append'
        )
    print(f"Taxi zones data ingested successfully.")

if __name__ == '__main__':
    run()