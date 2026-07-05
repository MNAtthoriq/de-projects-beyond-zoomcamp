"""
Ingest NYC TLC tripdata from the TLC CDN into GCS.
The script downloads the raw parquet files, standardizes the schema, and uploads to GCS.
"""

import argparse
import os
from datetime import date

import pandas as pd
import requests
from dotenv import load_dotenv
from google.cloud import storage
from tqdm import tqdm

load_dotenv()

TLC_CDN = "https://d37ci6vzurychx.cloudfront.net/trip-data"

# common dtypes across yellow & green tripdata
DTYPES = {
    "VendorID": "Int64",
    "RatecodeID": "Int64",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "passenger_count": "Int64",
    "payment_type": "Int64",
    "store_and_fwd_flag": "string",
    "trip_distance": "float64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64",
}

# unified schema after renaming pickup/dropoff columns
COMMON_COLUMNS = ["pickup_datetime", "dropoff_datetime", *DTYPES.keys()]

def month_list(n_months: int, lag_months: int = 2) -> list[tuple[int, int]]:
    """Get a list of (year, month) tuples for the last n_months, lagging by lag_months"""
    today = date.today()
    y, m = today.year, today.month
    for _ in range(lag_months): # lag_months is 2 because NYC TLC publishes latest data with a 2-month lag
        m -= 1
        if m == 0:
            m, y = 12, y-1
    
    months = []
    for _ in range(n_months):
        months.append((y,m))
        m -= 1
        if m == 0:
            m, y = 12, y-1
    return list(reversed(months))

def download_with_progress(url: str, local_path: str, desc: str) -> bool:
    """Download a file from a URL with a progress bar, returning True if successful, False if 404, error for other issues"""
    with requests.get(url, stream=True) as r:
        if r.status_code == 404:
            print(f"  not published yet, skipping: {url}")
            return False
        r.raise_for_status()
        total = int(r.headers.get("content-length", 0))
        with (
            open(local_path, "wb") as f,
            tqdm(total=total, unit="B", unit_scale=True, unit_divisor=1024, desc=desc) as bar,
        ):
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                if not chunk:
                    continue
                bar.update(f.write(chunk))
    return True

def standardize(local_parquet: str, service: str, year: int, month: int) -> str:
    """Standardize the schema of a raw parquet file, returning the path to the standardized parquet file"""
    df = pd.read_parquet(local_parquet)

    pickup_col = "tpep_pickup_datetime" if service == "yellow" else "lpep_pickup_datetime"
    dropoff_col = "tpep_dropoff_datetime" if service == "yellow" else "lpep_dropoff_datetime"
    df = df.rename(columns={pickup_col: "pickup_datetime", dropoff_col: "dropoff_datetime"})

    for col, dtype in DTYPES.items():
        if col not in df.columns:
            df[col] = pd.NA
        df[col] = df[col].astype(dtype)

    df = df[COMMON_COLUMNS].copy()
    df["taxi_type"] = service
    df["source_month"] = f"{year:04d}-{month:02d}"

    out_path = local_parquet.replace(".parquet", "_standardized.parquet")
    df.to_parquet(out_path, engine="pyarrow", index=False)
    return out_path

def upload_to_gcs_with_progress(bucket: str, object_name: str, local_file: str):
    """Upload a local file to GCS with a progress bar, skipping if already exists"""
    # tune chunk size for slow uploads
    storage.blob._MAX_MULTIPART_SIZE = 5 * 1024 * 1024
    storage.blob._DEFAULT_CHUNKSIZE = 5 * 1024 * 1024

    client = storage.Client()
    blob = client.bucket(bucket).blob(object_name)

    if blob.exists(client):
        print(f"  already in GCS, skipping: gs://{bucket}/{object_name}")
        return
    
    file_size = os.path.getsize(local_file)
    with open(local_file, "rb") as f:
        with tqdm.wrapattr(
            f, "read", total=file_size, unit="B", unit_scale=True, unit_divisor=1024,
            desc=f"Uploading {os.path.basename(local_file)}",
        ) as wrapped:
            blob.upload_from_file(wrapped, size=file_size)
    print(f"  uploaded: gs://{bucket}/{object_name}")

def main():
    """Ingest NYC TLC tripdata from the TLC CDN into GCS"""
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "--months", type=int, default=12,
        help="How many months to pull (default: 12)"
    )
    parser.add_argument("--colors", nargs="+", default=["yellow", "green"], choices=["yellow", "green"])
    parser.add_argument("--bucket", default=os.environ.get("GCP_GCS_BUCKET"))
    args = parser.parse_args()

    if not args.bucket:
        raise SystemExit("No bucket given. Pass --bucket or set GCP_GCS_BUCKET in .env")
    
    months = month_list(args.months)
    print(f"Target months: {[f'{y}-{m:02d}' for y, m in months]}")

    client = storage.Client()
    bucket_obj = client.bucket(args.bucket)

    for service in args.colors:
        for year, month in tqdm(months, desc=f"{service} months", unit="month"):
            file_name = f"{service}_tripdata_{year:04d}-{month:02d}.parquet"
            object_name = f"raw/{service}/{file_name}"

            if bucket_obj.blob(object_name).exists(client):
                print(f"already in GCS, skipping: gs://{args.bucket}/{object_name}")
                continue

            if not os.path.exists(file_name):
                ok = download_with_progress(f"{TLC_CDN}/{file_name}", file_name, desc=f"Downloading {file_name}")
                if not ok:
                    continue
            
            std_path = None

            try:
                std_path = standardize(file_name, service, year, month)
                upload_to_gcs_with_progress(args.bucket, object_name, std_path)

            finally: # cleanup local files
                if os.path.exists(file_name):
                    os.remove(file_name)

                if std_path and os.path.exists(std_path):
                    os.remove(std_path)
    
    print("Done. Raw standardized months are under gs://<bucket>/raw/{yellow,green}/")

if __name__ == "__main__":
    main()