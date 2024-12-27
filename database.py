import sqlite3 as sql
import config

# Function to connect to the database and enable foreign key constraints
def connection():
    conn = sql.connect(config.database_name + '.db')
    conn.execute("PRAGMA foreign_keys = ON;")
    c = conn.cursor()
    return conn, c

# Function to initialize the database and create tables if they don't exist
def db_init():
    conn, c = connection()
    with conn:
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS patient_record (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                gender TEXT NOT NULL,
                contact_number_1 TEXT NOT NULL
            );
            """
        )
    with conn:
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS doctor_record (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                gender TEXT NOT NULL,
                specialization TEXT NOT NULL,
                contact_number_1 TEXT NOT NULL
            );
            """
        )
    with conn:
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS prescription_record (
                id TEXT PRIMARY KEY,
                patient_id TEXT NOT NULL,
                doctor_id TEXT NOT NULL,
                medicine_name TEXT NOT NULL,
                dosage_description TEXT NOT NULL,
                FOREIGN KEY (patient_id) REFERENCES patient_record(id)
                ON UPDATE CASCADE
                ON DELETE CASCADE,
                FOREIGN KEY (doctor_id) REFERENCES doctor_record(id)
                ON UPDATE CASCADE
                ON DELETE CASCADE
            );
            """
        )
    conn.close()
