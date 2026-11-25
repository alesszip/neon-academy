import calendar
from datetime import date, timedelta
from IPython.display import display, HTML
import ipywidgets as widgets

# ==========================================
# CONFIGURACION GENERAL
# ==========================================

FECHA_FIN = date(2026, 11, 28)

DIAS_CLASE = [0, 1, 3]  # Lunes, martes y jueves

HORAS_CLASE = 2

FERIADOS = [
    date(2026, 11, 16)
]


# ==========================================
# CALCULAR HORAS RESTANTES
# ==========================================

def contar_horas(excepciones):

    hoy = date.today()
    fecha = hoy
    clases = 0

    while fecha <= FECHA_FIN:

        if (fecha.weekday() in DIAS_CLASE
                and fecha not in FERIADOS
                and fecha not in excepciones):

            clases += 1

        fecha += timedelta(days=1)

    horas = clases * HORAS_CLASE

    return clases, horas


# ==========================================
# MOSTRAR CALENDARIO
# ==========================================

def mostrar_calendario(excepciones):

    año = 2026
    mes = 11

    semanas = calendar.monthcalendar(año, mes)

    dias = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]

    resultado = widgets.HTML()

    calendario_widget = widgets.GridBox(
        [],
        layout=widgets.Layout(
            grid_template_columns="repeat(7, 1fr)",
            grid_gap="5px",
            width="100%",
            max_width="600px"
        )
    )

    def actualizar():

        # CALCULAR RESULTADOS
        clases, horas = contar_horas(excepciones)

        resultado.value = f"""
        <div style="background:#f5f0df;padding:22px;
        border-radius:15px;margin-top:15px;color:#344b36;">

        <h2>📚 Resultado de consulta</h2>

        <p><b>Profesor:</b> {nombre}</p>
        <p><b>Materia:</b> {materia}</p>

        <hr>

        <div style="display:flex;justify-content:space-around;
        text-align:center;">

            <div>
                <h3>Clases restantes</h3>
                <h1>{clases}</h1>
            </div>

            <div>
                <h3>Horas restantes</h3>
                <h1>{horas}</h1>
            </div>

        </div>

        <hr>

        <p>Excepciones registradas: {len(excepciones)}</p>
        <p>Fecha final: 28 de noviembre de 2026</p>

        </div>
        """

        elementos = []

        # ENCABEZADOS
        for dia in dias:
            elementos.append(
                widgets.HTML(
                    f"<div style='text-align:center;font-weight:bold;"
                    f"color:#344b36;padding:8px;'>{dia}</div>"
                )
            )

        # DIAS DEL MES
        for semana in semanas:

            for dia in semana:

                if dia == 0:
                    elementos.append(widgets.Label(""))
                    continue

                fecha = date(año, mes, dia)

                boton = widgets.Button(
                    description=str(dia),
                    layout=widgets.Layout(
                        width="100%",
                        height="48px"
                    )
                )

                # FERIADO
                if fecha in FERIADOS:

                    boton.style.button_color = "#d99a65"
                    boton.disabled = True

                # EXCEPCION
                elif fecha in excepciones:

                    boton.style.button_color = "#e6b6b6"

                # DIA ACTUAL
                elif fecha == date.today():

                    boton.style.button_color = "#526b4d"

                # DIA DE CLASE
                elif fecha.weekday() in DIAS_CLASE:

                    boton.style.button_color = "#b8c9a5"

                # DIA SIN CLASE
                else:

                    boton.style.button_color = "#e8e3d5"
                    boton.disabled = True

                # SELECCIONAR O QUITAR EXCEPCIONES
                if (seleccion_si
                    and fecha.weekday() in DIAS_CLASE
                    and fecha not in FERIADOS
                    and fecha >= date.today()
                    and fecha <= FECHA_FIN):

                    def seleccionar(b, f=fecha):

                        if f in excepciones:
                            excepciones.remove(f)
                        else:
                            excepciones.add(f)

                        actualizar()

                    boton.on_click(seleccionar)

                else:
                    boton.disabled = True

                elementos.append(boton)

        calendario_widget.children = elementos

    display(HTML("""
    <div style="background:#f5f0df;padding:20px;
    border-radius:15px;color:#344b36;max-width:600px;">
    <h2 style="text-align:center;">🍃 Noviembre 2026</h2>
    </div>
    """))

    display(calendario_widget)

    display(HTML("""
    <div style="background:#f5f0df;padding:15px;
    border-radius:15px;color:#344b36;max-width:600px;
    text-align:center;margin-top:10px;">

    🟩 Clase &nbsp; 🟧 Feriado &nbsp; 🟥 Excepción

    <p>Selecciona los lunes, martes o jueves para
    registrar una excepción.</p>

    </div>
    """))

    display(resultado)

    actualizar()


# ==========================================
# ENCABEZADO
# ==========================================

display(HTML("""
<div style="background:#344b36;padding:25px;
border-radius:15px;color:white;text-align:center;">
<h1>🌿 NEON ACADEMY</h1>
<p>Tu asistente académico</p>
<p>Consulta tus horas restantes del semestre</p>
</div>
"""))


# ==========================================
# DATOS DEL PROFESOR
# ==========================================

nombre = input("Nombre del profesor: ")
materia = input("Materia: ")


# ==========================================
# SECCION DE EXCEPCIONES
# ==========================================

print("\n========== EXCEPCIONES ==========")

print("¿Hay alguna clase que no se impartirá?")
print("Ejemplos: lluvia, suspensión o evento.")

excepciones = set()

respuesta = input(
    "\n¿Deseas agregar una excepción? (si/no): "
).strip().lower()

while respuesta not in ["si", "sí", "no"]:

    print("Respuesta incorrecta. Escribe SI o NO.")

    respuesta = input(
        "¿Deseas agregar una excepción? (si/no): "
    ).strip().lower()


if respuesta in ["si", "sí"]:

    seleccion_si = True

    print("\n¡Perfecto!")
    print("Selecciona directamente en el calendario")
    print("los lunes, martes o jueves que no habrá clase.")
    print("Cada día seleccionado se marcará en rojo.")
    print("Puedes volver a hacer clic para quitarlo.")

else:

    seleccion_si = False

    print("\nNo se registrarán excepciones.")
    print("Todas las clases permanecerán normales.")


# ==========================================
# RESULTADOS
# ==========================================

if nombre.strip() == "" or materia.strip() == "":

    print("\nDebes ingresar tu nombre y materia.")

else:

    mostrar_calendario(excepciones)
