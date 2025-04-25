# Archivo: tareas.py
import streamlit as st
import pandas as pd
import os
from datetime import datetime

GRUPOS = ["Grupo A", "Grupo B", "Grupo C", "Grupo D"]
ESTADOS = ["Todos", "En curso", "Pausada", "Completada"]

GRUPOS = ["Grupo A", "Grupo B", "Grupo C", "Grupo D"]
ESTADOS = ["Todos", "En curso", "Pausada", "Completada"]

def mostrar_tareas():
    st.header("📝 Tareas en Curso")

    # Contenedor para la última actualización
    update_container = st.empty()

    tareas_path = "data/tareas.xlsx"
    if os.path.exists(tareas_path):
        try:
            # Leer el archivo cada vez que se llama a la función
            tareas_df = pd.read_excel(tareas_path)

            # Mostrar última actualización
            ultima_act = tareas_df["Última Actualización"].max() if "Última Actualización" in tareas_df.columns else "No disponible"
            update_container.info(f"🕒 Última actualización: {ultima_act}")

            # Filtros en dos columnas
            col1, col2 = st.columns(2)
            with col1:
                filtro_grupo = st.selectbox("🔍 Filtrar por grupo", ["Todos"] + GRUPOS)
            with col2:
                filtro_estado = st.selectbox("🔄 Filtrar por estado", ESTADOS)

            # Aplicar filtros
            df_filtrado = tareas_df.copy()
            if filtro_grupo != "Todos":
                df_filtrado = df_filtrado[df_filtrado["Grupo"] == filtro_grupo]
            if filtro_estado != "Todos":
                df_filtrado = df_filtrado[df_filtrado["Estado"] == filtro_estado]

            # Mostrar métricas
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Tareas", len(df_filtrado))
            with col2:
                completadas = len(df_filtrado[df_filtrado["Estado"] == "Completada"])
                st.metric("Completadas", completadas)
            with col3:
                pendientes = len(df_filtrado[df_filtrado["Estado"] != "Completada"])
                st.metric("Pendientes", pendientes)

            # Mostrar tabla con formato mejorado
            st.dataframe(
                df_filtrado,
                use_container_width=True,
                column_config={
                    "ID": st.column_config.TextColumn("ID", width=80),
                    "Grupo": st.column_config.TextColumn("Grupo", width=100),
                    "Responsable": st.column_config.TextColumn("Responsable", width=150),
                    "Descripción": st.column_config.TextColumn("Descripción", width="medium"),
                    "Estado": st.column_config.TextColumn("Estado", width=100),
                    "% Avance": st.column_config.ProgressColumn(
                        "Avance",
                        width=100,
                        format="%d%%",
                        min_value=0,
                        max_value=100,
                    ),
                }
            )

            return df_filtrado

        except Exception as e:
            st.error(f"❌ Error al leer el archivo de tareas: {e}")
            return pd.DataFrame()
    else:
        st.warning("⚠️ No hay tareas registradas")
        return pd.DataFrame()