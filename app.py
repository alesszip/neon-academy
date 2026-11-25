
import streamlit as st
import calendar
from datetime import date, timedelta

# CONFIGURACION
st.set_page_config(
    page_title="NEON ACADEMY",
    page_icon="🌿",
    layout="centered"
)

FECHA_FIN = date(2026, 11, 28)
DIAS_CLASE = [0, 1, 3]
HORAS_CLASE = 2

FERIADOS = [date(2026, 11, 16)]


# CALCULAR HORAS
def contar_horas():
    hoy = date.today()
    fecha = hoy
    clases = 0

    while fecha <= FECHA_FIN:
        if fecha.weekday() in DIAS_CLASE and fecha not in FERIADOS:
            clases += 1

        fecha += timedelta(days=1)

    return clases, clases * HORAS_CLASE


# CALENDARIO
def mostrar_calendario():
    st.subheader("🍃 Calendario de noviembre 2026")

    semanas = calendar.monthcalendar(2026, 11)
    dias = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]

    st.write(" | ".join(dias))
    
    for semana in semanas:
        fila = []

        for dia in semana:
            if dia == 0:
                fila.append(" ")
            else:
                fecha = date(2026, 11, dia)

                if fecha in FERIADOS:
                    fila.append("🟧 " + str(dia))
                elif fecha.weekday() in DIAS_CLASE:
                    fila.append("🟩 " + str(dia))
                else:
                    fila.append(str(dia))

        st.write(" | ".join(fila))

    st.caption("🟩 Día de clase | 🟧 Día feriado")


# DISEÑO
st.markdown("""
<style>
.stApp {
    background-color: #f5f0df;
}
h1, h2, h3, p, label {
    color: #344b36 !important;
}
div.stButton > button {
    background-color: #526b4d;
    color: white;
    border-radius: 10px;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)


# INTERFAZ PRINCIPAL
st.title("🌿 NEON ACADEMY")
st.write("Tu asistente académico")
st.write("Consulta las horas restantes del semestre.")

nombre = st.text_input("Nombre del profesor")
materia = st.text_input("Materia")

if st.button("Consultar mis horas"):

    if nombre.strip() == "" or materia.strip() == "":
        st.warning("Ingresa tu nombre y materia.")

    else:
        clases, horas = contar_horas()

        st.success("Consulta realizada correctamente.")

        st.write("**Profesor:**", nombre)
        st.write("**Materia:**", materia)

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Clases restantes", clases)

        with col2:
            st.metric("Horas restantes", horas)

        st.write("Fecha de finalización: 28 de noviembre de 2026")


mostrar_calendario()
