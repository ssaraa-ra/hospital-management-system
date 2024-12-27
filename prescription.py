import streamlit as st
from datetime import datetime
import database as db
import pandas as pd
import patient
import doctor


# Funksioni për të verifikuar ID-në e recetës
def verify_prescription_id(prescription_id):
    conn, c = db.connection()
    with conn:
        c.execute("SELECT id FROM prescription_record WHERE id = :id;", {'id': prescription_id})
        return c.fetchone() is not None


# Funksioni për të shfaqur detajet e recetës
def show_prescription_details(list_of_prescriptions):
    prescription_titles = ['ID e Recetës', 'ID e Pacientit', 'ID e Mjekut', 'Emri i Medikamentit', 'Përshkrimi i Dozës']
    if not list_of_prescriptions:
        st.warning('Nuk ka të dhëna për të shfaqur.')
    elif len(list_of_prescriptions) == 1:
        series = pd.Series(data=list_of_prescriptions[0], index=prescription_titles)
        st.write(series)
    else:
        df = pd.DataFrame(data=list_of_prescriptions, columns=prescription_titles)
        st.write(df)


# Funksioni për të gjeneruar një ID të veçantë për recetën
def generate_prescription_id():
    id_1 = datetime.now().strftime('%S%M%H')
    id_2 = datetime.now().strftime('%Y%m%d')[2:]
    return f'R-{id_1}-{id_2}'


# Klasa për operacionet e recetave
class Prescription:

    def __init__(self):
        self.id = None
        self.patient_id = None
        self.doctor_id = None
        self.medicine_name = None
        self.dosage_description = None

    # Metoda për të shtuar një rekord të ri recete
    def add_prescription(self):
        st.write('Shkruani detajet e recetës:')

        # Verifikimi i ID-së së pacientit
        self.patient_id = st.text_input('ID e Pacientit')
        if not self.patient_id or not patient.verify_patient_id(self.patient_id):
            st.error('ID e Pacientit është e pavlefshme ose bosh.')
            return

        # Verifikimi i ID-së së mjekut
        self.doctor_id = st.text_input('ID e Mjekut')
        if not self.doctor_id or not doctor.verify_doctor_id(self.doctor_id):
            st.error('ID e Mjekut është e pavlefshme ose bosh.')
            return

        # Detajet e medikamentit
        self.medicine_name = st.text_input('Emri i Medikamentit')
        self.dosage_description = st.text_area('Përshkrimi i Dozës')

        # Gjenerimi i ID-së për recetën
        self.id = generate_prescription_id()

        save = st.button('Ruaj Recetën')
        if save:
            conn, c = db.connection()
            with conn:
                c.execute(
                    """
                    INSERT INTO prescription_record
                    (id, patient_id, doctor_id, medicine_name, dosage_description)
                    VALUES (:id, :p_id, :dr_id, :med_name, :dose_desc);
                    """,
                    {
                        'id': self.id,
                        'p_id': self.patient_id,
                        'dr_id': self.doctor_id,
                        'med_name': self.medicine_name,
                        'dose_desc': self.dosage_description,
                    }
                )
            st.success('Detajet e recetës u ruajtën me sukses.')
            st.write('ID-ja e Recetës është:', self.id)

    # Metoda për të përditësuar një rekord ekzistues të recetës
    def update_prescription(self):
        id = st.text_input('Shkruani ID-në e Recetës që do të përditësohet')
        if not id or not verify_prescription_id(id):
            st.error('ID e Recetës është e pavlefshme.')
            return

        conn, c = db.connection()
        with conn:
            c.execute("SELECT * FROM prescription_record WHERE id = :id;", {'id': id})
            prescription = c.fetchone()
            if not prescription:
                st.error('Receta nuk u gjet.')
                return

            st.write('Detajet aktuale të recetës:')
            show_prescription_details([prescription])

            # Përditësimi i detajeve të recetës
            self.medicine_name = st.text_input('Emri i ri i Medikamentit', prescription[3])
            self.dosage_description = st.text_area('Përshkrimi i ri i Dozës', prescription[4])

            update = st.button('Përditëso Recetën')
            if update:
                c.execute(
                    """
                    UPDATE prescription_record
                    SET medicine_name = :med_name, dosage_description = :dose_desc
                    WHERE id = :id;
                    """,
                    {
                        'id': id,
                        'med_name': self.medicine_name,
                        'dose_desc': self.dosage_description,
                    }
                )
                st.success('Receta u përditësua me sukses.')

    # Metoda për të fshirë një rekord ekzistues të recetës
    def delete_prescription(self):
        id = st.text_input('Shkruani ID-në e Recetës që do të fshihet')
        if not id or not verify_prescription_id(id):
            st.error('ID e Recetës është e pavlefshme.')
            return

        conn, c = db.connection()
        with conn:
            c.execute("SELECT * FROM prescription_record WHERE id = :id;", {'id': id})
            prescription = c.fetchone()
            if not prescription:
                st.error('Receta nuk u gjet.')
                return

            st.write('Receta që do të fshihet:')
            show_prescription_details([prescription])

            confirm = st.checkbox('Shënoni këtë kuti për të konfirmuar fshirjen')
            if confirm:
                delete = st.button('Fshi Recetën')
                if delete:
                    c.execute("DELETE FROM prescription_record WHERE id = :id;", {'id': id})
                    st.success('Receta u fshi me sukses.')

    # Metoda për të shfaqur të gjitha recetat e një pacienti të caktuar
    def prescriptions_by_patient(self):
        patient_id = st.text_input('Shkruani ID-në e Pacientit për të parë recetat')
        if not patient_id or not patient.verify_patient_id(patient_id):
            st.error('ID e Pacientit është e pavlefshme.')
            return

        conn, c = db.connection()
        with conn:
            c.execute("SELECT * FROM prescription_record WHERE patient_id = :p_id;", {'p_id': patient_id})
            prescriptions = c.fetchall()
            if prescriptions:
                st.write(f"Recetat për Pacientin me ID {patient_id}:")
                show_prescription_details(prescriptions)
            else:
                st.warning('Nuk ka receta për këtë pacient.')
