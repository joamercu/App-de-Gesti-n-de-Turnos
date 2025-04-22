# Archivo: modules/config_turnos.py
import streamlit as st
import pandas as pd
import os
from datetime import datetime, time, timedelta
import pytz
# Ruta del archivo de configuración
CONFIG_PATH = "data/config_turnos.xlsx"
# Ruta del archivo de configuración\CONFIG_PATH = "data/config_turnos.xlsx"


# Composición de grupos para ayuda visual
GRUPOS_DETALLE = {
    "Grupo A": ["Julio Montoya", "Domingo Cuevas", "Oscar Rubio", "Julian Ramirez"],
    "Grupo B": ["Angel Oyuela", "Juan Salguero", "Miguel Varón", "Fansisco Lasso"],
    "Grupo C": ["Jhon Castañeda", "Luis Gomez", "Hernan Osorio", "Manuel Aramendis"],
    "Grupo D": ["Nelson Rubio", "Manuel Castañeda", "Cristian Osorio", "Camilo Lemus"]
}

# Fechas de inicio por defecto (naive datetimes)
# Parámetros de entrada según tu configuración
DEFAULT_FECHAS = {
    'Grupo A': datetime(2025, 3, 31),
    'Grupo B': datetime(2025, 4, 10),
    'Grupo C': datetime(2025, 4, 7),
    'Grupo D': datetime(2025, 4, 3),
}
tz = pytz.timezone("America/Bogota")

# Guarda la configuración de inicio de turnos en Excel
def guardar_config(config):
    data = []
    for grupo, fecha in config.items():
        fecha_naive = fecha.replace(tzinfo=None)
        data.append({"Grupo": grupo, "Fecha de Inicio": fecha_naive})
    df = pd.DataFrame(data)
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    df.to_excel(CONFIG_PATH, index=False)

# Carga la configuración de turnos si existe, o usa fechas por defecto
def cargar_config():
    config = {}
    if os.path.exists(CONFIG_PATH):
        df = pd.read_excel(CONFIG_PATH)
        for grupo in GRUPOS_DETALLE:
            # buscar fila del grupo
            matches = df[df["Grupo"] == grupo]
            if not matches.empty:
                val = matches.iloc[0]["Fecha de Inicio"]
                if pd.isna(val):
                    fecha_naive = DEFAULT_FECHAS[grupo]
                else:
                    fecha_naive = pd.to_datetime(val).to_pydatetime()
            else:
                fecha_naive = DEFAULT_FECHAS[grupo]
            # asignar zona horaria
            if fecha_naive.tzinfo is None:
                config[grupo] = fecha_naive.replace(tzinfo=tz)
            else:
                config[grupo] = fecha_naive.astimezone(tz)
    else:
        for grupo, fecha in DEFAULT_FECHAS.items():
            config[grupo] = fecha.replace(tzinfo=tz)
    return config

# Interfaz de configuración editable por el usuario
def configurar_turnos_usuario():
    st.header("⚙️ Configuración de Turnos por Grupo")

    # Ayuda visual: composición de grupos
    st.markdown("### 🧑‍🤝‍🧑 Composición de grupos")
    for grupo, integrantes in GRUPOS_DETALLE.items():
        st.markdown(f"**{grupo}**: {', '.join(integrantes)}")

    st.markdown("---")
    st.markdown("### 📅 Configurar fechas de inicio de ciclo")

    config_actual = cargar_config()
    nueva_config = {}

    for grupo in sorted(GRUPOS_DETALLE.keys()):
        fecha_pred = config_actual[grupo].date()
        fecha_sel = st.date_input(f"Fecha de inicio {grupo}", fecha_pred)
        dt = datetime.combine(fecha_sel, time(0, 0))
        nueva_config[grupo] = dt.replace(tzinfo=tz)

    if st.button("💾 Guardar configuración de turnos"):
        guardar_config(nueva_config)
        st.success("✅ Configuración guardada correctamente.")


# Localizar fechas de inicio
FECHA_INICIO_GRUPOS = {g: tz.localize(dt) for g, dt in DEFAULT_FECHAS.items()}

def grupo_activo(fecha_hoy):
    estados = {}
    for grupo, inicio in FECHA_INICIO_GRUPOS.items():
        dias = (fecha_hoy - inicio).days
        if dias < 0:
            estados[grupo] = 'Descanso'
        else:
            ciclo = dias % 21
            estados[grupo] = 'X' if ciclo < 14 else 'Descanso'
    return estados



data = []


df = pd.DataFrame(data)
st.dataframe(df, use_container_width=True)






# Interfaz de configuración editable por el usuario
def configurar_turnos_usuario():
    st.header("⚙️ Configuración de Turnos por Grupo")

    # Ayuda visual: composición de grupos
    st.markdown("### 🧑‍🤝‍🧑 Composición de grupos")
    for grupo, integrantes in GRUPOS_DETALLE.items():
        st.markdown(f"**{grupo}**: {', '.join(integrantes)}")

    st.markdown("---")
    st.markdown("### 📅 Configurar fechas de inicio de ciclo")

    actuales = cargar_config()
    nuevos = {}
    for grupo in sorted(GRUPOS_DETALLE.keys()):
        pred = actuales[grupo].date()
        sel = st.date_input(f"Fecha de inicio {grupo}", pred)
        dt = datetime.combine(sel, time(0, 0))
        nuevos[grupo] = dt.replace(tzinfo=tz)

    if st.button("💾 Guardar configuración de turnos"):
        guardar_config(nuevos)
        st.success("✅ Configuración guardada correctamente.")

    st.markdown("---")
    st.markdown("### 🔄 Vista previa de turnos (14/7)")
    dias = st.number_input("Días a previsualizar", min_value=7, max_value=90, value=30)
    if st.button("🔍 Mostrar vista previa"):
        from modules.turnos import generar_tabla_turnos
        inicio = datetime.now(tz)
        fin = inicio + timedelta(days=dias-1)
        tabla = generar_tabla_turnos(inicio, fin)
        st.dataframe(tabla, use_container_width=True)

