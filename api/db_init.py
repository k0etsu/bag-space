import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

conn = psycopg2.connect(
    database="flask_db",
    user=DB_USER,
    password=DB_PASS,
    port=5432
)

cur = conn.cursor()

# Execute a command: this creates a new table
cur.execute('DROP TABLE IF EXISTS items;')
cur.execute('CREATE TABLE items (id serial PRIMARY KEY,'
            'name varchar (150) NOT NULL,'
            'category varchar (50) NOT NULL,'
            'stock integer NOT NULL,'
            'notes text,'
            'date_added date DEFAULT CURRENT_TIMESTAMP);'
)

# Insert data into the table

cur.execute(
    'INSERT INTO items (name, category, stock, notes)'
    'VALUES (%s, %s, %s, %s)',
    (
        'Chicken stock',
        'Kitchen',
        3,
        'Not surprisingly, Costco is the cheapest'
    )
)


cur.execute(
    'INSERT INTO items (name, category, stock, notes)'
    'VALUES (%s, %s, %s, %s)',
    (
        'Toilet paper',
        'Bathroom',
        24,
        'Check booth before buying'
    )
)

conn.commit()

cur.close()
conn.close()
