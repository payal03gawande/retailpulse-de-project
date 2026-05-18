
import sqlite3
import os
from src.config.config import Config
# from dotenv import load_dotenv
from faker import Faker
import random
from datetime import datetime, timedelta

# # Load env
# load_dotenv()

# DB path
# folder = os.getenv("DB_FOLDER", "data/raw")
# db_name = os.getenv("DB_NAME", "retailpulse.db")
folder = Config.DB_FOLDER
db_name = Config.DB_NAME
db_path = os.path.join(folder,db_name)

os.makedirs(folder, exist_ok=True)

# Setup
fake = Faker("en_IN")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print(f"Connected to SQLite at {db_path} ✅")

# 🔥 CREATE TABLES
cursor.execute("""
CREATE TABLE IF NOT EXISTS inventory (
    product_id TEXT PRIMARY KEY,
    product_name TEXT NOT NULL,
    category TEXT NOT NULL,
    quantity INTEGER DEFAULT 0,
    price_inr REAL NOT NULL,
    warehouse TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    customer_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    city TEXT NOT NULL,
    tier TEXT NOT NULL,
    loyalty_pts INTEGER DEFAULT 0,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
)
""")

print("Tables created ✅")

# 🔥 DATA SETUP
categories = ['Electronics','Clothing','Jewellery','Books','Home']
warehouses = ['Mumbai','Delhi','Bengaluru','Hyderabad']
tiers = ['Bronze','Silver','Gold','Platinum']

# 🔥 INSERT INVENTORY
for i in range(200):
    cursor.execute("""
    INSERT OR IGNORE INTO inventory
    (product_id, product_name, category, quantity, price_inr, warehouse, created_at, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        f'PROD-{i+1:04d}',
        fake.catch_phrase(),
        random.choice(categories),
        random.randint(0,500),
        round(random.uniform(99,9999),2),
        random.choice(warehouses),
        (datetime.utcnow()-timedelta(days=random.randint(30,365))).isoformat(),
        (datetime.now()-timedelta(hours=random.randint(0,48))).isoformat()
    ))

# 🔥 INSERT CUSTOMERS
for i in range(200):
    cursor.execute("""
    INSERT OR IGNORE INTO customers
    (customer_id, name, email, city, tier, loyalty_pts, created_at, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        f'CUST-{i+1:04d}',
        fake.name(),
        fake.email(),
        fake.city(),
        random.choice(tiers),
        random.randint(0,10000),
        (datetime.utcnow()-timedelta(days=random.randint(30,365))).isoformat(),
        (datetime.utcnow()-timedelta(hours=random.randint(0,72))).isoformat()
    ))

print("Data inserted (200 rows each) ✅")

# Commit & Close
conn.commit()
conn.close()

print(f"Database created: {db_path}")
print("Tables: inventory & customers ready🚀")

