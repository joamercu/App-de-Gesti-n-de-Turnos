# Archivo: modules/config_turnos.py
import streamlit as st
import pandas as pd
import os
from datetime import datetime, time, timedelta
import pytz

from modules.grupos import GRUPOS_DETALLE

# Ruta del archivo de configuración
CONFIG_PATH = "data/config_turnos.xlsx"
# Ruta del archivo de configuración\CONFIG_PATH = "data/config_turnos.xlsx"


# Composición de grupos para ayuda visual
#GRUPOS_DETALLE = {
#    "Grupo A": ["Julio Montoya", "Domingo Cuevas", "Oscar Rubio", "Julian Ramirez"],
#    "Grupo B": ["Angel Oyuela", "Juan Salguero", "Miguel Varón", "Fansisco Lasso"],
#    "Grupo C": ["Jhon Castañeda", "Luis Gomez", "Hernan Osorio", "Manuel Aramendis"],
#    "Grupo D": ["Nelson Rubio", "Manuel Castañeda", "Cristian Osorio", "Camilo Lemus"]
#}

# Fechas de inicio por defecto (naive datetimes)
# Parámetros de entrada según tu configuración
FECHA_INICIO_GRUPOS = {
    'Grupo A': datetime(2025, 3, 31),
    'Grupo B': datetime(2025, 4, 10),
    'Grupo C': datetime(2025, 4, 7),
    'Grupo D': datetime(2025, 4, 3),
}
tz = pytz.timezone("America/Bogota")


GRUPOS = list(FECHA_INICIO_GRUPOS.keys())

# Diccionarios para formateo manual de fecha en español
MESES_ES = [
    "enero", "febrero", "marzo", "abril", "mayo", "junio",
    "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
]
DIAS_ES = [
    "lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"
]



def formatear_fecha_es(fecha: datetime) -> str:
    dia_semana = DIAS_ES[fecha.weekday()]
    dia = fecha.day
    mes = MESES_ES[fecha.month - 1]
    anio = fecha.year
    return f"{dia_semana}, {dia} de {mes} de {anio}"


# Guarda la configuración de inicio de turnos en Excel
#def guardar_config(config):
#    data1 = []
#    for grupo, fecha in config.items():
#        fecha_naive = fecha.replace(tzinfo=None)
#        data1.append({"Grupo": grupo, "Fecha de Inicio": fecha_naive})
#    df = pd.DataFrame(data1)
#    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
#    df.to_excel(CONFIG_PATH, index=False)
#
# Carga la configuración de turnos si existe, o usa fechas por defecto

def cargar_config():
    config = {}
    if os.path.exists(CONFIG_PATH):
        df1 = pd.read_excel(CONFIG_PATH)
        for grupo in GRUPOS_DETALLE:
            # buscar fila del grupo
            matches = df1[df1["Grupo"] == grupo]
            if not matches.empty:
                val = matches.iloc[0]["Fecha de Inicio"]
                if pd.isna(val):
                    fecha_naive = FECHA_INICIO_GRUPOS[grupo]
                else:
                    fecha_naive = pd.to_datetime(val).to_pydatetime()
            else:
                fecha_naive = FECHA_INICIO_GRUPOS[grupo]
            # asignar zona horaria
            if fecha_naive.tzinfo is None:
                config[grupo] = fecha_naive.replace(tzinfo=tz)
            else:
                config[grupo] = fecha_naive.astimezone(tz)
    else:
        for grupo, fecha in FECHA_INICIO_GRUPOS.items():
            config[grupo] = fecha.replace(tzinfo=tz)
    return config

# Interfaz de configuración editable por el usuario


    # Localizar fechas de inicio
FECHA_INICIO_GRUPOS = {g: tz.localize(dt) for g, dt in FECHA_INICIO_GRUPOS.items()}

def grupo_activo(fecha_hoy):
    """
    Devuelve lista de tuplas (grupo, estado, días_restantes) con ciclo 14/7 días.
    """
    estados = []
    for grupo, inicio in FECHA_INICIO_GRUPOS.items():
        dias = (fecha_hoy - inicio).days
        if dias >= 0:
            ciclo = dias % 21
            if ciclo < 14:
                estado = 'trabajo'
                dias_rest = 14 - ciclo
            else:
                estado = 'descanso'
                dias_rest = 21 - ciclo
            estados.append((grupo, estado, dias_rest))
    return estados
data = []
df = pd.DataFrame(data)
st.dataframe(df, use_container_width=True)



def generar_tabla_turnos(desde: datetime, hasta: datetime):
    """
    Genera tabla estilizada de turnos con emoticones y texto centrado.
    """
    fechas = pd.date_range(desde, hasta)
    data1 = []
    for fecha in fechas:
        fecha_hoy = tz.localize(datetime.combine(fecha, datetime.min.time()))
        estados = grupo_activo(fecha_hoy)
        fila = { 'Fecha': formatear_fecha_es(fecha_hoy) }
        for grupo, estados, dias_rest in estados:
            icon = '🛠️' if estados == 'trabajo' else '😴'
            fila[grupo] = f"{icon} {estados.capitalize()} ({dias_rest})"
        # Asegurar columnas para todos los grupos
        for g in GRUPOS:
            fila.setdefault(g, '')
        data1.append(fila)

    df2 = pd.DataFrame(data1)[['Fecha'] + GRUPOS]
    styler = df2.style.set_properties(**{
        'text-align': 'center',
        'white-space': 'normal',
        'word-wrap': 'break-word'
    })
    return styler



def configurar_turnos_usuario():
    st.header("⚙️ Configuración de Turnos por Grupo")
    # Ayuda visual: composición de grupos
    st.markdown("### 🧑‍🤝‍🧑 Composición de grupos")
    for grupo, integrantes in GRUPOS_DETALLE.items():
        st.markdown(f"**{grupo}**: {', '.join(integrantes)}")

    st.markdown("---")
    st.markdown("### 📅 Configurar fechas de inicio de ciclo")

    #config_actual = {}
    nueva_config = {}

    for grupo in sorted(GRUPOS_DETALLE.keys()):
        # fecha_pred = config_actual[grupo].date()
        fecha_sel = st.date_input(f"Fecha de inicio {grupo}")
        dt = datetime.combine(fecha_sel, time(0, 0))
        nueva_config[grupo] = dt.replace(tzinfo=tz)

    if st.button("💾 Guardar configuración de turnos"):
        # guardar_config(nueva_config)
        st.success("✅ Configuración guardada correctamente.")

    st.markdown("---")
    st.markdown("### 🔄 Vista previa de turnos (14/7)")
    dias = st.number_input("Días a previsualizar", min_value=7, max_value=100, value=60)
    if st.button("🔍 Mostrar vista previa"):
        inicio = datetime(2025, 3, 31)
        fin = inicio + timedelta(days=dias - 1)
        # fin = datetime(2025, 4, 30)
        tabla = generar_tabla_turnos(inicio, fin)
        st.dataframe(tabla, use_container_width=True)
