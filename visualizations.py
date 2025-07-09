import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
import pandas as pd
import database as db
import plotly.express as px

# Set page config to set a layout and theme for Streamlit
st.set_page_config(page_title="Clinic Dashboard", layout="wide")

# Use a clean, professional color palette
sns.set_palette("muted")  # Seaborn muted colors for cleaner visuals

# Visualize Patient Age Distribution with Seaborn for Aesthetic Bar Plot
def visualize_patient_age():
    conn, c = db.connection()
    with conn:
        c.execute("SELECT age FROM patient_record;")
        data = c.fetchall()
    
    if data:
        ages = [row[0] for row in data]
        bins = [0, 18, 40, 60, 100]
        labels = ['0-18', '19-40', '41-60', '61+']
        age_groups = pd.cut(ages, bins=bins, labels=labels, right=False)
        age_group_counts = age_groups.value_counts().sort_index()

        # Use seaborn for a more professional bar plot with muted color
        plt.figure(figsize=(8, 6))
        sns.barplot(x=age_group_counts.index, y=age_group_counts.values, color='#4C72B0')  # A muted blue

        plt.title('Përqindja e Pacientëve sipas Grupit të Moshës', fontsize=16, fontweight='bold')
        plt.xlabel('Grupi i Moshës', fontsize=12)
        plt.ylabel('Numri i Pacientëve', fontsize=12)
        plt.xticks(rotation=45, fontsize=10)
        plt.yticks(fontsize=10)
        st.pyplot(plt)
    else:
        st.warning("Nuk ka të dhëna për moshën e pacientëve.")

# Visualize Doctor Specializations with Altair for Interactive Bar Chart
def visualize_doctor_specializations():
    conn, c = db.connection()
    with conn:
        c.execute("SELECT specialization, COUNT(*) FROM doctor_record GROUP BY specialization;")
        data = c.fetchall()
    
    if data:
        df = pd.DataFrame(data, columns=['Specializimi', 'Numri'])
        
        chart = alt.Chart(df).mark_bar().encode(
            x=alt.X('Specializimi', sort='-y', title='Specializimi'),
            y=alt.Y('Numri', title='Numri i Mjekëve'),
            tooltip=['Specializimi', 'Numri']
        ).properties(
            title='Numri i Mjekëve sipas Specializimit',
            width=700,
            height=400
        ).configure_mark(
            color='#2c3e50'  # A muted professional color (dark gray)
        ).configure_title(
            fontSize=18,
            fontWeight='bold',
            font='Arial',
            anchor='middle'
        ).configure_axis(
            labelFont='Arial',
            labelFontSize=12,
            titleFont='Arial',
            titleFontSize=14
        )

        st.altair_chart(chart, use_container_width=True)
    else:
        st.warning("Nuk ka të dhëna për mjekët.")

# Visualize Most Prescribed Medicines with Interactive Plotly Bar Chart
def visualize_top_medicines():
    conn, c = db.connection()
    with conn:
        c.execute("SELECT medicine_name, COUNT(*) FROM prescription_record GROUP BY medicine_name ORDER BY COUNT(*) DESC LIMIT 10;")
        data = c.fetchall()

    if data:
        df = pd.DataFrame(data, columns=['Emri i Barnave', 'Numri i Përshkrimeve'])
        
        # Plotly bar chart with subtle color scheme
        fig = px.bar(df, x='Emri i Barnave', y='Numri i Përshkrimeve',
                     title='Barnat më të Përshkruara', color='Numri i Përshkrimeve',
                     color_continuous_scale='Blues')
        fig.update_layout(bargap=0.15,
                          title_font=dict(size=18, family='Arial', color='black'),
                          xaxis_title_font=dict(size=14, family='Arial', color='black'),
                          yaxis_title_font=dict(size=14, family='Arial', color='black'),
                          xaxis_tickangle=-45)
        st.plotly_chart(fig)
    else:
        st.warning("Nuk ka të dhëna për përshkrimet e barnave.")

# Main Visualization Function with Selection
def visualize_data():
    st.title("Vizualizimet e të dhënave")
    
    option = st.selectbox("Zgjidh", [
        "Përqindja e Pacientëve sipas Grupit të Moshës",
        "Numri i Mjekëve sipas Specializimit",
        "Barnat më të përshkruara"
    ])

    if option == "Përqindja e Pacientëve sipas Grupit të Moshës":
        visualize_patient_age()
    elif option == "Numri i Mjekëve sipas Specializimit":
        visualize_doctor_specializations()
    elif option == "Barnat më të përshkruara":
        visualize_top_medicines()