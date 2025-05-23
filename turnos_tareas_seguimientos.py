# Archivo principal: app_streamlit.py
import streamlit as st
# ¡ESTA LÍNEA DEBE IR AQUÍ!
st.set_page_config(page_title="Gestión de Turnos 14x7", layout="wide")

import pandas as pd
from datetime import datetime, timedelta
import pytz
import os
if not os.path.exists('data'):
    os.makedirs('data')

from modules.reloj import mostrar_reloj
from modules.tareas import mostrar_tareas
from modules.transferencias import formulario_transferencia
from modules.upload import cargar_excel_estado
from modules.excel_export import exportar_excel
from modules.config_turnos import configurar_turnos_usuario
from modules.grupos import gestionar_grupos
# Importar el nuevo módulo
from modules.formulario_tareas import formulario_tareas  # Nueva importación
from modules.turnos_tareas_seguimientos_reporte import mostrar_seguimiento  # Nueva importación

# ==================== CONFIGURACIONES ==================== #
st.title("🕒 Gestión de Turnos, Tareas y Transferencias PROYECTOS METALMECANICA")

# ==================== SELECCIÓN DE MÓDULOS ==================== #
# En el archivo principal
if 'modulo' not in st.session_state:
    st.session_state.modulo = "Reloj y Turno Actual"

# Selección de módulos
modulo = st.sidebar.selectbox("📂 Selecciona un módulo",
    [
        "Reloj y Turno Actual",
        "Tareas en Curso",
        "Gestión de Tareas",  # Nueva opción
        "Transferencia de Turno",
        "Carga de Estado de Tareas",
        "Exportar a Excel",
        "Calendario de Turnos",
        "Configuración de Turnos",
        "Gestión de Grupos",
        "Seguimiento y Reportes"  # Nueva opción
    ],
    key="modulo"  # Esto conecta el selectbox con session_state.modulo
)

# ==================== LLAMADO A MÓDULOS ==================== #
if modulo == "Reloj y Turno Actual":
    mostrar_reloj()

elif modulo == "Configuración de Turnos":
    configurar_turnos_usuario()

elif modulo == "Tareas en Curso":
    tareas_df = mostrar_tareas()

elif modulo == "Gestión de Tareas":
    tareas_df = formulario_tareas()  # Si necesitas el DataFrame actualizado

elif modulo == "Transferencia de Turno":
    tareas_df = mostrar_tareas()
    formulario_transferencia(tareas_df)

elif modulo == "Carga de Estado de Tareas":
    cargar_excel_estado()

elif modulo == "Exportar a Excel":
    tareas_df = mostrar_tareas()
    exportar_excel(tareas_df)

elif modulo == "Calendario de Turnos":
    from modules.calendario import mostrar_calendario_turnos
    mostrar_calendario_turnos()

elif modulo == "Seguimiento y Reportes":
    mostrar_seguimiento()

# En la sección de módulos:
elif modulo == "Gestión de Grupos":
    gestionar_grupos()

# En la sección de módulos:



