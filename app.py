import streamlit as st
import database as db
from patient import Patient
from doctor import Doctor
from prescription import Prescription
import config
import sqlite3 as sql
from visualizations import visualize_data




with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)



# Funksioni për verifikimin e fjalëkalimit të adminit për operacionet e redaktimit
def verify_edit_mode_password():
    edit_mode_password = st.sidebar.text_input('Shkruaj fjalëkalimin e adminit për redaktim', type='password')
    if edit_mode_password == config.edit_mode_password:
        st.sidebar.success('Fjalekalimi i sakte')
        return True
    elif edit_mode_password == '':
        st.empty()
    else:
        st.sidebar.error('Fjalëkalimi i gabuar')
        return False

# Funksioni për operacionet me pacientët
def patients():
    st.header('Menaxhimi i Pacientëve')
    options = ['Zgjidh veprimin', 'Shto pacient', 'Përditëso pacient', 'Fshi pacient', 'Shiko pacientët', 'Kërko pacient']
    choice = st.sidebar.selectbox('Zgjidh veprimin për pacientët', options)
    patient_obj = Patient()

    if choice == 'Shto pacient' and verify_edit_mode_password():
        st.subheader('Shto një pacient të ri')
        patient_obj.add_patient()
    elif choice == 'Përditëso pacient' and verify_edit_mode_password():
        st.subheader('Përditëso të dhënat e pacientit')
        patient_obj.update_patient()
    elif choice == 'Fshi pacient' and verify_edit_mode_password():
        st.subheader('Fshi të dhënat e pacientit')
        patient_obj.delete_patient()
    elif choice == 'Shiko pacientët':
        st.subheader('Shiko të gjitha të dhënat e pacientëve')
        patient_obj.show_all_patients()
    elif choice == 'Kërko pacient':
        st.subheader('Kërko për një pacient')
        patient_obj.search_patient()

# Funksioni për operacionet me mjekët
def doctors():
    st.header('Menaxhimi i Mjekëve')
    options = ['Zgjidh veprimin', 'Shto mjek', 'Përditëso mjek', 'Fshi mjek', 'Shiko mjekët', 'Kërko mjek']
    choice = st.sidebar.selectbox('Zgjidh veprimin për mjekët', options)
    doctor_obj = Doctor()

    if choice == 'Shto mjek' and verify_edit_mode_password():
        st.subheader('Shto një mjek të ri')
        doctor_obj.add_doctor()
    elif choice == 'Përditëso mjek' and verify_edit_mode_password():
        st.subheader('Përditëso të dhënat e mjekut')
        doctor_obj.update_doctor()
    elif choice == 'Fshi mjek' and verify_edit_mode_password():
        st.subheader('Fshi të dhënat e mjekut')
        doctor_obj.delete_doctor()
    elif choice == 'Shiko mjekët':
        st.subheader('Shiko të gjitha të dhënat e mjekëve')
        doctor_obj.show_all_doctors()
    elif choice == 'Kërko mjek':
        st.subheader('Kërko për një mjek')
        doctor_obj.search_doctor()

# Funksioni për operacionet me recetat
def prescriptions():
    st.header('Menaxhimi i Recetave')
    options = ['Zgjidh veprimin', 'Shto recetë', 'Përditëso recetë', 'Fshi recetë', 'Shiko recetat e pacientëve']
    choice = st.sidebar.selectbox('Zgjidh veprimin për recetat', options)
    prescription_obj = Prescription()

    if choice == 'Shto recetë' and verify_edit_mode_password():
        st.subheader('Shto një recetë të re')
        prescription_obj.add_prescription()
    elif choice == 'Përditëso recetë' and verify_edit_mode_password():
        st.subheader('Përditëso të dhënat e recetës')
        prescription_obj.update_prescription()
    elif choice == 'Fshi recetë' and verify_edit_mode_password():
        st.subheader('Fshi recetë')
        prescription_obj.delete_prescription()
    elif choice == 'Shiko recetat e pacientëve':
        st.subheader('Shiko recetat e një pacienti të veçantë')
        prescription_obj.prescriptions_by_patient()

# Menyja kryesore për zgjedhjen e moduleve
def main_menu():
    db.db_init()  # Krijon bazën e të dhënave (tabelat nëse nuk ekzistojnë)
    modules = ['Zgjidh ', 'Pacientët', 'Mjekët', 'Recetat', 'Statistika']  # Add 'Statistika'
    selected_module = st.sidebar.selectbox('', modules)

    if selected_module == 'Pacientët':
        patients()
    elif selected_module == 'Mjekët':
        doctors()
    elif selected_module == 'Recetat':
        prescriptions()
    elif selected_module == 'Statistika':  # Call the visualization function
        visualize_data()

# Logjika kryesore e aplikacionit
st.title('Sistemi i Menaxhimit të Poliklinikës S.R. ')
password = st.sidebar.text_input('Shkruaj fjalëkalimin', type='password')

# Verifikimi i fjalëkalimit
if password == config.password:
    st.sidebar.success('Fjalëkalimi i sakte')
    main_menu()
elif password == '':
    st.empty()
else:
    st.sidebar.error('Fjalëkalimi i gabuar')



    
