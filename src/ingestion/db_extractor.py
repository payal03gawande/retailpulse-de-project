
import sqlite3
import boto3
import json
import os
from datetime import datetime, timedelta
from src.config.config import Config

# CONFIG
BUCKET = Config.BRONZE_BUCKET
DB_PATH = os.path.join(Config.DB_FOLDER, Config.DB_NAME)
WATERMARK = os.path.join(Config.DB_FOLDER, Config.WATERMARK_FILE)

s3 = boto3.client("s3")


# 1. GET LAST RUN
def get_last_run_ts():
    if os.path.exists(WATERMARK):
        with open(WATERMARK, "r") as f:
            ts = f.read().strip()
            print(f"Last run found: {ts}")
            return ts

    # FIRST RUN → get all data
    print("First run: loading full data")
    return "2000-01-01T00:00:00"


# 2. SAVE LAST RUN
def save_last_run_ts(ts):
    with open(WATERMARK, "w") as f:
        f.write(ts)


# 3. CDC QUERY
def extract_table(cursor, table, last_ts):
    query = f"""
        SELECT * FROM {table}
        WHERE updated_at > ?
        ORDER BY updated_at ASC
    """

    cursor.execute(query, (last_ts,))
    cols = [desc[0] for desc in cursor.description]

    rows = [dict(zip(cols, row)) for row in cursor.fetchall()]

    print(f"{table}: {len(rows)} records")
    return rows


# 4. UPLOAD TO S3
def upload_to_s3(entity, rows, run_ts):
    if not rows:
        print(f"No data for {entity}")
        return

    now = datetime.fromisoformat(run_ts)

    payload = {
        "source": "sqlite",
        "entity": entity,
        "extract_ts": run_ts,
        "record_count": len(rows),
        "data": rows
    }

    key = (
        f"sqlite/{entity}/"
        f"year={now.year}/month={now.month:02d}/"
        f"day={now.day:02d}/"
        f"{entity}_{now.strftime('%H%M%S')}.json"
    )

    s3.put_object(
        Bucket=BUCKET,
        Key=key,
        Body=json.dumps(payload, default=str),
        ContentType="application/json"
    )

    print(f"Uploaded → {key}")


# 5. MAIN RUN
def run():
    print("Starting CDC...")

    last_ts = get_last_run_ts()
    run_ts = datetime.utcnow().isoformat()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for table in ["inventory", "customers"]:
        rows = extract_table(cursor, table, last_ts)
        upload_to_s3(table, rows, run_ts)

    conn.close()

    save_last_run_ts(run_ts)

    print("CDC completed 🚀")


if __name__ == "__main__":
    run()