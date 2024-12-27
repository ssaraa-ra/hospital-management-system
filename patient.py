import streamlit as st
from datetime import datetime, date
import database as db
import pandas as pd

# Function to verify patient ID
def verify_patient_id(patient_id):
    verify = False
    conn, c = db.connection()
    with conn:
        c.execute(
            """
            SELECT id
            FROM patient_record;
            """
        )
    for id in c.fetchall():
        if id[0] == patient_id:
            verify = True
            break
    conn.close()
    return verify

# Function to calculate age using given date of birth
def calculate_age(dob):
    today = date.today()
    age = today.year - dob.year - ((dob.month, dob.day) > (today.month, today.day))
    return age

# Function to show the details of patient(s) given in a list (provided as a parameter)
def show_patient_details(list_of_patients):
    patient_titles = ['ID e Pacientit', 'Emri', 'Mosha', 'Gjinia', 'Numri i Kontaktit']
    if len(list_of_patients) == 0:
        st.warning('Nuk ka të dhëna për të shfaqur')
    elif len(list_of_patients) == 1:
        patient_details = [x for x in list_of_patients[0]]
        series = pd.Series(data=patient_details, index=patient_titles)
        st.write(series)
    else:
        patient_details = []
        for patient in list_of_patients:
            patient_details.append([x for x in patient])
        df = pd.DataFrame(data=patient_details, columns=patient_titles)
        st.write(df)

# Class containing all the fields and methods required to work with the patients' table in the database
class Patient:

    def __init__(self):
        self.name = str()
        self.id = str()
        self.gender = str()
        self.age = int()
        self.contact_number_1 = str()

    # Method to add a new patient record to the database
    def add_patient(self):
        st.write('Shkruani te dhenat e pacientit:')
        self.name = st.text_input('Emri i Plotë')
        gender = st.radio('Gjinia', ['Femër', 'Mashkull'])
        self.gender = gender
        dob = st.date_input('Data e Lindjes (VVVV/MM/DD)')
        self.age = calculate_age(dob)
        self.contact_number_1 = st.text_input('Numri i Kontaktit')
        self.date_of_registration = datetime.now().strftime('%d-%m-%Y')
        self.time_of_registration = datetime.now().strftime('%H:%M:%S')
        self.id = f"P-{self.date_of_registration.replace('-', '')}-{self.time_of_registration.replace(':', '')}"
        save = st.button('Ruaj')

        if save:
            conn, c = db.connection()
            with conn:
                c.execute(
                    """
                    INSERT INTO patient_record
                    (
                        id, name, age, gender, contact_number_1
                    )
                    VALUES (
                        :id, :name, :age, :gender, :phone_1
                    );
                    """,
                    {
                        'id': self.id, 'name': self.name, 'age': self.age,
                        'gender': self.gender, 'phone_1': self.contact_number_1
                    }
                )
            st.success('Të dhënat e pacientit u ruajtën me sukses.')
            st.write('ID-ja e Pacientit tuaj është: ', self.id)
            conn.close()

    # Method to update an existing patient record in the database
    def update_patient(self):
        id = st.text_input('Shkruani ID-në e Pacientit që do të përditësohet')
        if id == '':
            st.empty()
        elif not verify_patient_id(id):
            st.error('ID e Pacientit është e pavlefshme')
        else:
            st.success('E verifikuar')
            conn, c = db.connection()

            with conn:
                c.execute(
                    """
                    SELECT *
                    FROM patient_record
                    WHERE id = :id;
                    """,
                    {'id': id}
                )
                st.write('Këto janë te dhenat aktuale të pacientit:')
                patient_data = c.fetchone()
                if patient_data:
                    show_patient_details([patient_data])

            st.write('Shkruani te dhenat e reja të pacientit:')
            self.name = st.text_input('Emri i Plotë', value=patient_data[1])
            self.age = st.number_input('Mosha', value=patient_data[2], min_value=0, max_value=120)
            self.gender = st.text_input('Gjinia', value=patient_data[3])
            self.contact_number_1 = st.text_input('Numri i Kontaktit', value=patient_data[4])

            update = st.button('Përditëso')

            if update:
                with conn:
                    c.execute(
                        """
                        UPDATE patient_record
                        SET name = :name, age = :age, gender = :gender, contact_number_1 = :phone_1
                        WHERE id = :id;
                        """,
                        {
                            'id': id, 'name': self.name, 'age': self.age,
                            'gender': self.gender, 'phone_1': self.contact_number_1
                        }
                    )
                st.success('Të dhënat e pacientit u përditësuan me sukses.')
                conn.close()

    # Method to delete an existing patient record from the database
    def delete_patient(self):
        id = st.text_input('Shkruani ID-në e Pacientit që do të fshihet')
        if id == '':
            st.empty()
        elif not verify_patient_id(id):
            st.error('ID e Pacientit është e pavlefshme')
        else:
            st.success('E verifikuar')
            conn, c = db.connection()

            with conn:
                c.execute(
                    """
                    SELECT *
                    FROM patient_record
                    WHERE id = :id;
                    """,
                    {'id': id}
                )
                st.write('Këto janë te dhenat e pacientit që do të fshihet:')
                show_patient_details(c.fetchall())

                confirm = st.checkbox('Kontrolloni këtë kuti për të konfirmuar fshirjen')
                if confirm:
                    delete = st.button('Fshij')

                    if delete:
                        try:
                            c.execute(
                                """
                                DELETE FROM patient_record
                                WHERE id = :id;
                                """,
                                {'id': id}
                            )
                            st.success('Të dhënat e pacientit u fshinë me sukses.')
                        except Exception as e:
                            st.error(f"Ndodhi një gabim: {str(e)}")
            conn.close()

    # Method to show the complete patient record
    def show_all_patients(self):
        conn, c = db.connection()
        with conn:
            c.execute(
                """
                SELECT *
                FROM patient_record;
                """
            )
            show_patient_details(c.fetchall())
        conn.close()

    # Method to search and show a particular patient's details in the database using patient ID
    def search_patient(self):
        id = st.text_input('Shkruani ID-në e Pacientit që do të kërkohet')
        if id == '':
            st.empty()
        elif not verify_patient_id(id):
            st.error('ID e Pacientit është e pavlefshme')
        else:
            st.success('E verifikuar')
            conn, c = db.connection()
            with conn:
                c.execute(
                    """
                    SELECT *
                    FROM patient_record
                    WHERE id = :id;
                    """,
                    {'id': id}
                )
                st.write('Këto janë te dhenat e pacientit që kërkuat:')
                show_patient_details(c.fetchall())
            conn.close()

















            