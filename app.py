
import streamlit as st
from datetime import date, timedelta

# ==========================================
# CONFIGURACION
# ==========================================

st.set_page_config(
    page_title="NEON ACADEMY",
    page_icon="🌿",
    layout="centered"
)

FECHA_FIN = date(2026, 11, 28)
DIAS_CLASE = [0, 1, 3]  # Lunes, martes y jueves
HORAS_POR_CLASE = 2
CLASES_FERIADAS = 2

# ==========================================
# DISEÑO
# ==========================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Nunito:wght@400;600;700&display=swap');

.stApp {
    background: #eee8d7;
    color: #403b2c;
    font-family: 'Nunito', sans-serif;
}

.block-container {
    max-width: 850px;
    padding-top: 2rem;
}

.header {
    background: linear-gradient(120deg,#405b3c,#82966c);
    padding: 30px;
    border-radius: 18px;
    text-align: center;
    color: white;
}

.header h1 {
    font-family: 'DM Serif Display', serif;
    font-size: 42px;
}

.card {
    background: #fff8e9;
    border: 2px solid #c8b48c;
    border-radius: 15px;
    padding: 22px;
    margin-top: 18px;
}

.robot {
    text-align: center;
    font-size: 75px;
}

.result {
    background: #e5eddc;
    border: 2px solid #82966c;
    border-radius: 15px;
    padding: 22px;
    text-align: center;
    margin-top: 20px;
}

.big-number {
    color: #496a3d;
    font-size: 45px;
    font-weight: bold;
}

.stButton button {
    background: #66834e;
    color: white;
    border-radius: 10px;
    border: none;
    width: 100%;
    height: 50px;
    font-weight: bold;
}

.stButton button:hover {
    background: #496a3d;
    color: white;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# ENCABEZADO
# ==========================================

st.markdown("""
<div class="header">
    <h1>NEON ACADEMY</h1>
    <p>✿ ASISTENTE ACADÉMICO ✿</p>
</div>

<div class="card">
    <div class="robot">🌳</div>
    <h3 style="text-align:center;color:#526c45;">
        ¡Bienvenido, profesor!
    </h3>
    <p style="text-align:center;">
        Soy Neko, tu asistente académico.
        Escribe tu nombre y materia para conocer
        cuántas horas de clase te quedan.
    </p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# DATOS DEL PROFESOR
# ==========================================

st.markdown("""
<div class="card">
    <h3 style="color:#526c45;">📚 Datos del profesor</h3>
</div>
""", unsafe_allow_html=True)

nombre = st.text_input(
    "Nombre del profesor",
    placeholder="Escribe tu nombre"
)

materia = st.text_input(
    "Materia",
    placeholder="Escribe tu materia"
)

# ==========================================
# CALCULO
# ==========================================

if st.button("🌿 CONSULTAR MIS HORAS"):

    if not nombre.strip() or not materia.strip():

        st.warning("NEKO: Escribe tu nombre y materia.")

    else:

        hoy = date.today()

        if hoy > FECHA_FIN:

            st.error("El semestre ha finalizado.")

        else:

            clases = 0
            fecha = hoy

            while fecha <= FECHA_FIN:

                if fecha.weekday() in DIAS_CLASE:
                    clases += 1

                fecha += timedelta(days=1)

            # Descontar las dos clases feriadas

            clases = max(0, clases - CLASES_FERIADAS)

            horas = clases * HORAS_POR_CLASE

            # ==================================
            # RESULTADO
            # ==================================

            st.markdown(f"""
            <div class="result">

                <h2 style="color:#526c45;">
                    📖 REPORTE ACADÉMICO
                </h2>

                <p><b>Profesor:</b> {nombre}</p>

                <p><b>Materia:</b> {materia}</p>

                <p><b>Fecha de consulta:</b>
                {hoy.strftime('%d/%m/%Y')}</p>

                <p><b>Fin del semestre:</b>
                28/11/2026</p>

                <hr>

                <p>CLASES PENDIENTES</p>

                <div class="big-number">
                    {clases}
                </div>

                <p>HORAS PENDIENTES</p>

                <div class="big-number">
                    {horas} HORAS
                </div>

                <hr>

                <p>
                    🌱 Neko dice: Profesor {nombre},
                    te quedan {horas} horas de clase
                    de {materia}.
                </p>

            </div>
            """, unsafe_allow_html=True)
