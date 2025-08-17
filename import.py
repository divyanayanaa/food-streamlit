import sqlite3
import pandas as pd

conn = sqlite3.connect("food_sharing.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS Providers;")
cursor.execute("DROP TABLE IF EXISTS Receivers;")
cursor.execute("DROP TABLE IF EXISTS Food_Listings;")
cursor.execute("DROP TABLE IF EXISTS Claims;")

cursor.execute("""
CREATE TABLE Providers (
    Provider_ID INTEGER PRIMARY KEY,
    Name TEXT,
    Type TEXT,
    Address TEXT,
    City TEXT,
    Contact TEXT
);
""")

cursor.execute("""
CREATE TABLE Receivers (
    receiver_id INTEGER PRIMARY KEY,
    name TEXT,
    type TEXT,
    city TEXT,
    contact TEXT
);
""")

cursor.execute("""
CREATE TABLE Food_Listings (
    food_id INTEGER PRIMARY KEY,
    food_name TEXT,
    quantity INTEGER,
    expiry_date TEXT,
    provider_id INTEGER,
    provider_type TEXT,
    location TEXT,
    food_type TEXT,
    meal_type TEXT,
    FOREIGN KEY (provider_id) REFERENCES Providers(Provider_ID)
);
""")

cursor.execute("""
CREATE TABLE Claims (
    claim_id INTEGER PRIMARY KEY,
    food_id INTEGER,
    receiver_id INTEGER,
    status TEXT,
    timestamp TEXT,
    FOREIGN KEY (food_id) REFERENCES Food_Listings(food_id),
    FOREIGN KEY (receiver_id) REFERENCES Receivers(receiver_id)
);
""")

conn.commit()

providers = pd.read_csv("providers_clean.csv")
receivers = pd.read_csv("receivers_clean.csv")
food_listings = pd.read_csv("food_listings_clean.csv")
claims = pd.read_csv("claims_clean.csv")

providers.to_sql("Providers", conn, if_exists="append", index=False)
receivers.to_sql("Receivers", conn, if_exists="append", index=False)
food_listings.to_sql("Food_Listings", conn, if_exists="append", index=False)
claims.to_sql("Claims", conn, if_exists="append", index=False)

conn.commit()
conn.close()

print("SQLite DB created successfully with all CSV data: food_sharing.db")
