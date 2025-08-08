# connect_db.py

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect, text
import pandas as pd

# Load env vars from .env file
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)

# Create inspector
inspector = inspect(engine)



    
    # leads
    # ▸ lead_id (VARCHAR(100))
    # ▸ search_keyword (JSONB)
    # ▸ draft_data (JSONB)
    # ▸ company (VARCHAR(1000))
    # ▸ website (VARCHAR(1000))
    # ▸ industry (VARCHAR(1000))
    # ▸ product_category (VARCHAR(2000))
    # ▸ business_type (VARCHAR(1000))
    # ▸ employees (INTEGER)
    # ▸ revenue (DOUBLE PRECISION)
    # ▸ year_founded (VARCHAR(100))
    # ▸ bbb_rating (VARCHAR(10))
    # ▸ street (VARCHAR(1000))
    # ▸ city (VARCHAR(1000))
    # ▸ state (VARCHAR(1000))
    # ▸ company_phone (VARCHAR(100))
    # ▸ company_linkedin (VARCHAR(1000))
    # ▸ owner_first_name (VARCHAR(1000))
    # ▸ owner_last_name (VARCHAR(1000))
    # ▸ owner_title (VARCHAR(1000))
    # ▸ owner_linkedin (VARCHAR(1000))
    # ▸ owner_phone_number (VARCHAR(100))
    # ▸ owner_email (VARCHAR(1000))
    # ▸ phone (VARCHAR(100))
    # ▸ source (VARCHAR(1000))
    # ▸ created_at (TIMESTAMP)
    # ▸ updated_at (TIMESTAMP)
    # ▸ deleted (BOOLEAN)
    # ▸ deleted_at (TIMESTAMP)
    # ▸ status (VARCHAR(1000))
    # ▸ edited_at (TIMESTAMP)
    # ▸ edited_by (TEXT)
    # ▸ is_edited (BOOLEAN)
    # ▸ country (VARCHAR(100))
    # ▸ company_id (VARCHAR(255))

try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT NOW();"))
        print("Connected successfully at:", result.fetchone()[0])
        # Use inspector to show DB structure
        # inspector = inspect(engine)
        # tables = inspector.get_table_names()

        # print("\n📄 Tables:")
        # for table in tables:
        #     if table =="leads":
        #         print(f"Table: {table}")
        #         # Print columns for each table
        #         columns = inspector.get_columns(table)
        #         for col in columns:
        #             print(f"    ▸ {col['name']} ({col['type']})")

        query = """
SELECT DISTINCT industry
FROM leads
WHERE industry IS NOT NULL
ORDER BY industry;
"""     
        query1 = """
SELECT 
  city,
  ARRAY_AGG(lead_id ORDER BY lead_id) AS lead_ids
FROM leads
WHERE city IS NOT NULL
GROUP BY city
ORDER BY city;
"""


        df = pd.read_sql(query1, engine)
        df.to_csv("unique_city.csv", index=False)
        print("Unique city saved to unique_city.csv")

        print(df.head(10000))
            

            
except Exception as e:
    print("Connection failed:", str(e))

