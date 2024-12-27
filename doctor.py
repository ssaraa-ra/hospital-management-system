import streamlit as st
from datetime import datetime
import database as db
import pandas as pd

# Funksioni për të verifikuar nëse ekziston një mjek në bazën e të dhënave
def verify_doctor_id(doctor_id):
    verify = False
    conn, c = db.connection()
    with conn:
        c.execute("""SELECT id FROM doctor_record;""")
        for id in c.fetchall():
            if id[0] == doctor_id:
                verify = True
                break
    conn.close()
    return verify

# Funksioni për të shfaqur detajet e mjekut në një format të lexueshëm
def show_doctor_details(list_of_doctors):
    doctor_titles = ['ID e Mjekut', 'Emri', 'Mosha', 'Gjinia', 'Specializimi', 'Numri i Kontaktit']
    if len(list_of_doctors) == 0:
        st.warning('Nuk ka të dhëna për të shfaqur')
    elif len(list_of_doctors) == 1:
        doctor_details = [x for x in list_of_doctors[0]]
        series = pd.Series(data=doctor_details, index=doctor_titles)
        st.write(series)
    else:
        doctor_details = []
        for doctor in list_of_doctors:
            doctor_details.append([x for x in doctor])
        df = pd.DataFrame(data=doctor_details, columns=doctor_titles)
        st.write(df)

# Funksioni për të gjeneruar një ID të veçantë për mjekun bazuar në kohën aktuale
def generate_doctor_id():
    id_1 = datetime.now().strftime('%S%M%H')
    id_2 = datetime.now().strftime('%Y%m%d')[2:]
    id = f'DR-{id_1}-{id_2}'
    return id

# Klasa për të menaxhuar operacionet e lidhura me mjekët në bazën e të dhënave
class Doctor:
    def __init__(self):
        self.name = str()
        self.id = str()
        self.age = int()
        self.gender = str()
        self.specialization = str()
        self.contact_number_1 = str()

    # Metoda për të shtuar një mjek të ri në bazën e të dhënave
    def add_doctor(self):
        st.write('Shkruani te dhenat e mjekut:')
        self.name = st.text_input('Emri i Plotë')
        gender = st.radio('Gjinia', ['Femër', 'Mashkull'])
        self.gender = gender
        self.specialization = st.text_input('Specializimi')
        self.contact_number_1 = st.text_input('Numri i Kontaktit')
        self.id = generate_doctor_id()
        save = st.button('Ruaj')

        if save:
            conn, c = db.connection()
            with conn:
                c.execute("""
                    INSERT INTO doctor_record (id, name, age, gender, specialization, contact_number_1)
                    VALUES (:id, :name, :age, :gender, :specialization, :phone_1);
                """, {
                    'id': self.id,
                    'name': self.name,
                    'age': self.age,
                    'gender': self.gender,
                    'specialization': self.specialization,
                    'phone_1': self.contact_number_1
                })
            st.success('Te dhenat e mjekut u ruajtën me sukses.')
            st.write('ID-ja juaj e Mjekut është: ', self.id)
            conn.close()

    # Metoda për të përditësuar detajet e një mjeku ekzistues
    def update_doctor(self):
        id = st.text_input('Shkruani ID-në e Mjekut që do të përditësohet')
        if id == '':
            st.empty()
        elif not verify_doctor_id(id):
            st.error('ID e Mjekut është e pavlefshme')
        else:
            st.success('E verifikuar')
            conn, c = db.connection()
            with conn:
                c.execute("""
                    SELECT * FROM doctor_record WHERE id = :id;
                """, {'id': id})
                doctor_data = c.fetchone()

            if not doctor_data:
                st.error('Mjeku nuk u gjet')
                return

            st.write('Te dhenat aktuale të mjekut:')
            show_doctor_details([doctor_data])

            # Prefill the form with existing data
            st.write('Përditësoni te dhenat e mjekut:')
            self.name = st.text_input('Emri i Plotë', value=doctor_data[1])
            self.age = st.number_input('Mosha', value=doctor_data[2], min_value=0, max_value=120)
            self.gender = st.radio('Gjinia', ['Femër', 'Mashkull'], index=(0 if doctor_data[3] == 'Femër' else 1))
            self.specialization = st.text_input('Specializimi', value=doctor_data[4])
            self.contact_number_1 = st.text_input('Numri i Kontaktit', value=doctor_data[5])

            update = st.button('Përditëso')
            if update:
                with conn:
                    c.execute("""
                        UPDATE doctor_record
                        SET name = :name, age = :age, gender = :gender, specialization = :specialization, contact_number_1 = :phone_1
                        WHERE id = :id;
                    """, {
                        'id': id,
                        'name': self.name,
                        'age': self.age,
                        'gender': self.gender,
                        'specialization': self.specialization,
                        'phone_1': self.contact_number_1
                    })
                st.success('Te dhenat e mjekut u përditësuan me sukses.')
            conn.close()

    # Metoda për të fshirë një rekord mjeku nga baza e të dhënave
    def delete_doctor(self):
        id = st.text_input('Shkruani ID-në e Mjekut që do të fshihet')
        if id == '':
            st.empty()
        elif not verify_doctor_id(id):
            st.error('ID e Mjekut është e pavlefshme')
        else:
            st.success('E verifikuar')
            conn, c = db.connection()
            with conn:
                c.execute("""
                    SELECT * FROM doctor_record WHERE id = :id;
                """, {'id': id})
                st.write('Te dhenat e mjekut që do të fshihet:')
                show_doctor_details(c.fetchall())

            confirm = st.checkbox('Konfirmoni fshirjen')
            if confirm:
                delete = st.button('Fshi')
                if delete:
                    with conn:
                        c.execute("""
                            DELETE FROM doctor_record WHERE id = :id;
                        """, {'id': id})
                    st.success('Mjeku u fshi me sukses.')
            conn.close()

    # Metoda për të shfaqur të gjithë mjekët në bazën e të dhënave
    def show_all_doctors(self):
        conn, c = db.connection()
        with conn:
            c.execute("""SELECT * FROM doctor_record;""")
            show_doctor_details(c.fetchall())
        conn.close()

    # Metoda për të kërkuar një mjek me ID-në e tij
    def search_doctor(self):
        id = st.text_input('Shkruani ID-në e Mjekut që kërkuat')
        if id == '':
            st.empty()
        elif not verify_doctor_id(id):
            st.error('ID e Mjekut është e pavlefshme')
        else:
            st.success('E verifikuar')
            conn, c = db.connection()
            with conn:
                c.execute("""
                    SELECT * FROM doctor_record WHERE id = :id;
                """, {'id': id})
                st.write('Te dhenat e mjekut që kërkuat:')
                show_doctor_details(c.fetchall())
            conn.close()


