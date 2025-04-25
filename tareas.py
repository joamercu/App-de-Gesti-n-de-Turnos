# Archivo: tareas.py
import streamlit as st
import pandas as pd
import os

GRUPOS = ["Grupo A", "Grupo B", "Grupo C", "Grupo D"]
ESTADOS = ["Todos", "En curso", "Pausada", "Completada"]

def mostrar_tareas():
    st.header("📝 Tareas en Curso")

    tareas_path = "data/tareas.xlsx"
    if os.path.exists(tareas_path):
        try:
            tareas_df = pd.read_excel(tareas_path)

            # Crear columnas de filtros en dos columnas
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

            # Mostrar estadísticas
            st.subheader("📊 Resumen de Tareas")
            col1, col2, col3 = st.columns(3)

            with col1:
                total_tareas = len(df_filtrado)
                st.metric("Total de Tareas", total_tareas)

            with col2:
                tareas_completadas = len(df_filtrado[df_filtrado["Estado"] == "Completada"])
                st.metric("Tareas Completadas", tareas_completadas)

            with col3:
                tareas_pendientes = len(df_filtrado[df_filtrado["Estado"].isin(["En curso", "Pausada"])])
                st.metric("Tareas Pendientes", tareas_pendientes)

            # Mostrar tabla de tareas
            st.subheader("📋 Lista de Tareas")

            # Ordenar por ID de forma descendente (las más recientes primero)
            df_filtrado = df_filtrado.sort_values(by='ID', ascending=False)

            # Dar formato a la tabla
            st.dataframe(
                df_filtrado,
                use_container_width=True,
                column_config={
                    "ID": st.column_config.TextColumn("ID", width="small"),
                    "Grupo": st.column_config.TextColumn("Grupo", width="small"),
                    "Responsable": st.column_config.TextColumn("Responsable", width="medium"),
                    "Descripción": st.column_config.TextColumn("Descripción", width="large"),
                    "Estado": st.column_config.TextColumn(
                        "Estado",
                        width="small",
                        help="Estado actual de la tarea"
                    )
                }
            )

            # Mostrar gráfico de tareas por estado
            st.subheader("📈 Distribución de Tareas")
            col1, col2 = st.columns(2)

            with col1:
                # Gráfico de tareas por estado
                estado_counts = df_filtrado["Estado"].value_counts()
                st.bar_chart(estado_counts)

            with col2:
                # Gráfico de tareas por grupo
                grupo_counts = df_filtrado["Grupo"].value_counts()
                st.bar_chart(grupo_counts)

            return df_filtrado

        except Exception as e:
            st.error(f"❌ Error al leer el archivo de tareas: {e}")
            return pd.DataFrame()
    else:
        st.warning("⚠️ No se encontró el archivo de tareas. Se mostrará una tabla de ejemplo.")
        tareas_df = pd.DataFrame({
            "ID": ["T001", "T002"],
            "Grupo": ["Grupo A", "Grupo B"],
            "Responsable": ["Oscar Rubio", "Angel Oyuela"],
            "Descripción": ["Inspección de válvulas", "Soldadura criogénica"],
            "Estado": ["En curso", "Pausada"]
        })
        st.dataframe(tareas_df, use_container_width=True)
        return tareas_df