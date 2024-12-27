import random
from faker import Faker
from database import connection, db_init  

fake = Faker()

# Initialize the database (create tables if they don't exist)
db_init()

# Function to insert synthetic data into the database
def insert_synthetic_data():
    try:
        conn, c = connection()

        # Generating synthetic data for patients
        for _ in range(50):  # Adjust number of patients as needed
            id = fake.uuid4()
            full_name = fake.name()  # Full name instead of just first name
            age = random.randint(13, 80)
            gender = random.choice(['Mashkull', 'Femër'])
            contact_number = fake.phone_number()
            
            c.execute(
                """
                INSERT INTO patient_record (id, name, age, gender, contact_number_1)
                VALUES (?, ?, ?, ?, ?);
                """, (id, full_name, age, gender, contact_number)
            )

        # Generating synthetic data for doctors
        for _ in range(12):  # Adjust number of doctors as needed
            id = fake.uuid4()
            full_name = fake.name()  # Full name instead of just first name
            age = random.randint(30, 60)
            gender = random.choice(['Mashkull', 'Femër'])
            specialization = random.choice(['Kardiologji', 'Pediatri', 'Dermatologji', 'Ortopedi', 'Stomatologji', 'Oftamologji' ])
            
            contact_number = fake.phone_number()
            
            c.execute(
                """
                INSERT INTO doctor_record (id, name, age, gender, specialization, contact_number_1)
                VALUES (?, ?, ?, ?, ?, ?);
                """, (id, full_name, age, gender, specialization, contact_number)
            )

        # Generating synthetic data for prescriptions
        for _ in range(50):  # Adjust number of prescriptions as needed
            prescription_id = fake.uuid4()
            patient_id = random.choice([row[0] for row in c.execute("SELECT id FROM patient_record").fetchall()])
            doctor_id = random.choice([row[0] for row in c.execute("SELECT id FROM doctor_record").fetchall()])
            medicine_name = random.choice(['Paracetamol', 'Adderall', 'Tramadol', 'Ibuprofen', 'Sulidamor', 'Amoxicillin ', 'Aspirin' ])
            dosage_description = random.choice(['1 herë ne ditë', '2 herë ne ditë', 'Në mengjes', 'Në mbrëmje', 'Pas bukës', 'Para bukës'])
            
            c.execute(
                """
                INSERT INTO prescription_record (id, patient_id, doctor_id, medicine_name, dosage_description)
                VALUES (?, ?, ?, ?, ?);
                """, (prescription_id, patient_id, doctor_id, medicine_name, dosage_description)
            )

        conn.commit()
        conn.close()
        print("Synthetic data inserted successfully!")

    except Exception as e:
        print(f"Error while inserting synthetic data: {e}")

# Call the function to insert synthetic data
insert_synthetic_data()
