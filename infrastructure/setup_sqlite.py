import sqlite3
import os
from dotenv import load_dotenv
from faker import Faker
import random
from datetime import datetime

# load env
load_dotenv()

# dynamic path
folder = os.getenv("DB_FOLDER", "data/raw")
db_name = os.getenv("DB_NAME", "retailpulse.db")
db_path = os.path.join(folder, db_name)

# ensure folder exists
os.makedirs(folder, exist_ok=True)

# faker setup
fake = Faker("en_IN")

# connect DB
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print(f"Connected to SQLite at {db_path} ✅")


# 🔥 CREATE TABLES

cursor.execute("""
CREATE TABLE IF NOT EXISTS inventory (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    category TEXT,
    quantity INTEGER,
    price REAL,
    warehouse TEXT,
    updated_at TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    city TEXT,
    tier TEXT,
    loyalty_pts INTEGER,
    updated_at TEXT
)
""")

print("Tables created ✅")


# 🔥 INSERT DATA

categories = ["Electronics", "Clothing", "Home", "Sports"]
tiers = ["Silver", "Gold", "Platinum"]

# inventory data (200 rows)
for _ in range(200):
    cursor.execute("""
    INSERT INTO inventory (name, category, quantity, price, warehouse, updated_at)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        fake.word(),
        random.choice(categories),
        random.randint(1, 500),
        round(random.uniform(100, 5000), 2),
        fake.city(),
        datetime.now().isoformat()
    ))

# customers data (200 rows)
for _ in range(200):
    cursor.execute("""
    INSERT INTO customers (name, email, city, tier, loyalty_pts, updated_at)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        fake.name(),
        fake.email(),
        fake.city(),
        random.choice(tiers),
        random.randint(0, 1000),
        datetime.now().isoformat()
    ))

print("Data inserted (200 rows each) ✅")


# commit & close
conn.commit()
conn.close()

print(f"Database created: {db_path}")
