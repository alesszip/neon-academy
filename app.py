
# ==========================================
#             NEON ACADEMY
# ==========================================

# 1. IMPORTAR LIBRERIAS

import streamlit as st
import calendar
from datetime import date, timedelta


# ==========================================
# 2. CONFIGURACION GENERAL
# ==========================================

st.set_page_config(
    page_title="NEON ACADEMY",
    page_icon="🌿",
    layout="centered"
)

FECHA_INICIO = date(2026, 8, 10)
FECHA_FIN = date(2026, 11, 28)

DIAS_CLASE = [0, 1, 3]  # Lunes, martes y jueves
HORAS_CLASE = 2


# ==========================================
# 3. DISEÑO DE LA PAGINA
# ==========================================

st.markdown("""
<style>
.stApp {
    background-color: #F5F0DF;
}
h1, h2, h3, p, label {
    color: #344B36;
}
.titulo {
    background-color: #344B36;
    padding: 25px;
    border-radius: 15px;
    text-align: center;
}
div.stButton > button {
    background-color: #526B4D;
    color: white;
    border-radius: 10px;
    width: 100%;
    height: 45px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)


# ==========================================
# 4. FUNCION PARA CONTAR LAS HORAS
# ==========================================

def contar_horas(excepciones):

    hoy = max(date.today(), FECHA_INICIO)
    fecha = hoy
    clases = 0

    while fecha <= FECHA_FIN:

        if fecha.weekday() in DIAS_CLASE and fecha not in excepciones:
            clases += 1

        fecha += timedelta(days=1)

    horas = clases * HORAS_CLASE

    return clases, horas


# ==========================================
# 5. FUNCION PARA MOSTRAR EL CALENDARIO
# ==========================================

def mostrar_calendario(excepciones):

    año = 2026
    mes = 11

    semanas = calendar.monthcalendar(año, mes)

    dias = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]

    html = """
    <style>
    .calendario {
        width: 100%;
        border-collapse: separate;
        border-spacing: 5px;
        text-align: center;
    }
    .calendario th {
        color: #344B36;
        padding: 10px;
    }
    .calendario td {
        background-color: #E8E3D5;
        padding: 12px 5px;
        border-radius: 8px;
        color: #344B36;
        font-weight: bold;
    }
    .clase {
        background-color: #B8C9A5 !important;
    }
    .feriado {
        background-color: #D99A65 !important;
        color: white !important;
    }
    .actual {
        background-color: #526B4D !important;
        color: white !important;
    }
    </style>
    <table class="calendario">
    <tr>
    """

    for dia in dias:
        html += f"<th>{dia}</th>"

    html += "</tr>"

    for semana in semanas:

        html += "<tr>"

        for dia in semana:

            if dia == 0:
                html += "<td></td>"
            else:

                fecha = date(año, mes, dia)
                clase_css = ""

                if fecha in excepciones:
                    clase_css = "feriado"
                elif fecha == date.today():
                    clase_css = "actual"
                elif fecha.weekday() in DIAS_CLASE:
                    clase_css = "clase"

                html += f'<td class="{clase_css}">{dia}</td>'

        html += "</tr>"

    html += "</table>"

    st.markdown(html, unsafe_allow_html=True)

    st.caption("🟩 Día de clase | 🟧 Excepción | 🟢 Fecha actual")


# ==========================================
# 6. ENCABEZADO
# ==========================================

st.markdown("""
<div class="titulo">
    <h1 style="color:white;">🌿 NEON ACADEMY</h1>
    <p style="color:white;">Tu asistente académico</p>
    <p style="color:white;">Consulta las horas restantes del semestre</p>
</div>
""", unsafe_allow_html=True)


# ==========================================
# 7. DATOS DEL PROFESOR
# ==========================================

st.subheader("📚 Datos del profesor")

nombre = st.text_input(
    "Nombre del profesor",
    placeholder="Escribe tu nombre"
)

materia = st.text_input(
    "Materia",
    placeholder="Escribe tu materia"
)


# ==========================================
# 8. SELECCIONAR EXCEPCIONES
# ==========================================

st.subheader("📅 Días de excepción")

st.write("Selecciona las fechas en las que no habrá clases.")

if "excepciones" not in st.session_state:
    st.session_state.excepciones = []

fecha_excepcion = st.date_input(
    "Seleccionar fecha de excepción",
    value=date(2026, 11, 16),
    min_value=FECHA_INICIO,
    max_value=FECHA_FIN
)

if st.button("Agregar día de excepción"):

    if fecha_excepcion.weekday() not in DIAS_CLASE:
        st.warning("La fecha seleccionada no corresponde a un día de clase.")

    elif fecha_excepcion in st.session_state.excepciones:
        st.warning("Esta fecha ya está registrada como excepción.")

    else:
        st.session_state.excepciones.append(fecha_excepcion)
        st.success("Día de excepción agregado correctamente.")

if st.session_state.excepciones:

    st.write("**Fechas registradas:**")

    for fecha in st.session_state.excepciones:
        st.write("🟧", fecha.strftime("%d/%m/%Y"))

    if st.button("Eliminar todas las excepciones"):
        st.session_state.excepciones = []
        st.rerun()


# ==========================================
# 9. CONFIRMACION Y CONSULTA
# ==========================================

st.subheader("Confirmar datos")

confirmacion = st.radio(
    "¿Los datos ingresados son correctos?",
    ["Sí", "No"],
    horizontal=True
)

if st.button("CONSULTAR MIS HORAS"):

    try:

        if nombre.strip() == "" or materia.strip() == "":
            st.warning("Debes ingresar tu nombre y materia.")

        elif confirmacion == "No":
            st.warning("Revisa tus datos antes de continuar.")

        elif confirmacion == "Sí":

            clases, horas = contar_horas(
                st.session_state.excepciones
            )

            st.success("Consulta realizada correctamente.")

            st.subheader("📋 Resultado de consulta")

            st.write("**Profesor:**", nombre)
            st.write("**Materia:**", materia)

            col1, col2 = st.columns(2)

            with col1:
                st.metric("Clases restantes", clases)

            with col2:
                st.metric("Horas restantes", horas)

            st.info("Fecha de finalización: 28 de noviembre de 2026")

    except Exception as error:

        st.error("Ocurrió un error al realizar la consulta.")
        st.write(error)


# ==========================================
# 10. CALENDARIO ACADEMICO
# ==========================================

st.divider()

st.subheader("🍃 Calendario académico")

st.write("Noviembre de 2026")

mostrar_calendario(st.session_state.excepciones)
