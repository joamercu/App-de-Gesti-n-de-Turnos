# Archivo: tareas.py
import streamlit as st
import pandas as pd
import os
from datetime import datetime

GRUPOS = ["Grupo A", "Grupo B", "Grupo C", "Grupo D"]
ESTADOS = ["Todos", "En curso", "Pausada", "Completada"]

GRUPOS = ["Grupo A", "Grupo B", "Grupo C", "Grupo D"]
ESTADOS = ["Todos", "En curso", "Pausada", "Completada"]

def cargar_datos_iniciales():
    """Carga los datos iniciales si no existe el archivo de tareas"""
    tareas_path = "data/tareas.xlsx"

    # Si ya existe el archivo, no hacemos nada
    if os.path.exists(tareas_path):
        return

    # Asegurarse de que existe el directorio data
    if not os.path.exists('data'):
        os.makedirs('data')

    # Datos iniciales de tareas
    datos_tareas = [
        {"ID": "T001", "Grupo": "Grupo A", "Responsable": "Julio Montoya",
         "Descripción": "Hidrociclon 4, gasificadores para muestras, torres zeolitas", "Estado": "Completada",
         "% Avance": 100, "Fecha inicio": "2025-04-25", "Fecha fin": "", "Foto_1": "img1.jpg", "Foto_2": "",
         "Foto_3": ""},
        {"ID": "T002", "Grupo": "Grupo B", "Responsable": "Angel Oyuela",
         "Descripción": "Recuperación de Trailer de 3 ejes, EDS Caldas Viejo", "Estado": "Completada", "% Avance": 100,
         "Fecha inicio": "2025-04-23", "Fecha fin": "", "Foto_1": "", "Foto_2": "img2.jpg", "Foto_3": ""},
        {"ID": "T003", "Grupo": "Grupo C", "Responsable": "Angel Oyuela",
         "Descripción": "Recuperación Trailer de 3 ejes.", "Estado": "Completada", "% Avance": 100,
         "Fecha inicio": "2025-04-21", "Fecha fin": "", "Foto_1": "", "Foto_2": "", "Foto_3": "img3.jpg"},
        {"ID": "T004", "Grupo": "Grupo A", "Responsable": "Jhon Castañeda",
         "Descripción": "HIDROCICLON #4 PSA SEPARADOR TRIFÁSICO", "Estado": "Completada", "% Avance": 100,
         "Fecha inicio": "2025-04-19", "Fecha fin": "", "Foto_1": "", "Foto_2": "img1.jpg", "Foto_3": ""},
        {"ID": "T005", "Grupo": "Grupo B", "Responsable": "Angel Oyuela", "Descripción": "Trabajos en EDS Caldas Viejo",
         "Estado": "Completada", "% Avance": 100, "Fecha inicio": "2025-04-17", "Fecha fin": "", "Foto_1": "",
         "Foto_2": "img2.jpg", "Foto_3": ""},
        {"ID": "T006", "Grupo": "Grupo C", "Responsable": "Angel Oyuela",
         "Descripción": "Cambio de válvulas de drenaje de escruber de 1ra 2da 3ra 4ta etapa. Alistamiento de materia trail...",
         "Estado": "Completada", "% Avance": 100, "Fecha inicio": "2025-04-15", "Fecha fin": "", "Foto_1": "",
         "Foto_2": "", "Foto_3": "img3.jpg"},
        {"ID": "T007", "Grupo": "Grupo A", "Responsable": "Angel Oyuela",
         "Descripción": "Cambios de válvulas de 1\" drenajes de escrubeer 1,2,3 y 4 etapa wortinthogn #2 Soldaduras en Spoo...",
         "Estado": "Completada", "% Avance": 100, "Fecha inicio": "2025-04-13", "Fecha fin": "", "Foto_1": "",
         "Foto_2": "img1.jpg", "Foto_3": ""},
        {"ID": "T008", "Grupo": "Grupo B", "Responsable": "Nelson Rubio",
         "Descripción": "Arregló del radiador de la psa", "Estado": "Completada", "% Avance": 100,
         "Fecha inicio": "2025-04-11", "Fecha fin": "", "Foto_1": "", "Foto_2": "img2.jpg", "Foto_3": ""},
        {"ID": "T009", "Grupo": "Grupo C", "Responsable": "Jhon Castañeda",
         "Descripción": "Separador trifásico Chiller propano Torres de zeolita", "Estado": "Completada",
         "% Avance": 100, "Fecha inicio": "2025-04-09", "Fecha fin": "", "Foto_1": "", "Foto_2": "",
         "Foto_3": "img3.jpg"},
        {"ID": "T010", "Grupo": "Grupo A", "Responsable": "Nelson Rubio", "Descripción": "Fabricación de hidrosiclon 4",
         "Estado": "Completada", "% Avance": 100, "Fecha inicio": "2025-04-07", "Fecha fin": "", "Foto_1": "",
         "Foto_2": "img1.jpg", "Foto_3": ""},
        {"ID": "T011", "Grupo": "Grupo A", "Responsable": "Oscar Rubio",
         "Descripción": "Terminación de línea de pulgada y alistamiento de materiales para las torres 4y5",
         "Estado": "Completada", "% Avance": 100, "Fecha inicio": "2025-04-20", "Fecha fin": "", "Foto_1": "",
         "Foto_2": "img1.jpg", "Foto_3": ""},
        {"ID": "T012", "Grupo": "Grupo B", "Responsable": "Oscar Rubio",
         "Descripción": "fabricación de línea para enviar gas de la sisterna así los generadores", "Estado": "Pausada",
         "% Avance": 60, "Fecha inicio": "2025-04-15", "Fecha fin": "", "Foto_1": "", "Foto_2": "img2.jpg",
         "Foto_3": "img3.jpg"},
        {"ID": "T013", "Grupo": "Grupo C", "Responsable": "Oscar Rubio",
         "Descripción": "montaje de las torres de Zeolitas", "Estado": "Completada", "% Avance": 100,
         "Fecha inicio": "2025-04-05", "Fecha fin": "2025-04-10", "Foto_1": "img4.jpg", "Foto_2": "", "Foto_3": ""},
        {"ID": "T014", "Grupo": "Grupo A", "Responsable": "Oscar Rubio",
         "Descripción": "izaje del gasificador para dejarlo al pie del separador de CO2", "Estado": "En curso",
         "% Avance": 30, "Fecha inicio": "2025-04-20", "Fecha fin": "", "Foto_1": "", "Foto_2": "img1.jpg",
         "Foto_3": ""},
        {"ID": "T015", "Grupo": "Grupo B", "Responsable": "Jhon Castañeda",
         "Descripción": "Bomba torre de enfriamiento", "Estado": "Pausada", "% Avance": 50,
         "Fecha inicio": "2025-04-15", "Fecha fin": "", "Foto_1": "", "Foto_2": "img2.jpg", "Foto_3": "img3.jpg"},
        {"ID": "T016", "Grupo": "Grupo C", "Responsable": "Angel Oyuela", "Descripción": "Torres de Zeolitas",
         "Estado": "Completada", "% Avance": 100, "Fecha inicio": "2025-04-05", "Fecha fin": "2025-04-10",
         "Foto_1": "img4.jpg", "Foto_2": "", "Foto_3": ""},

    ]

    # Crear DataFrame
    df_tareas = pd.DataFrame(datos_tareas)

    # Agregar timestamp de creación
    df_tareas["Última Actualización"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Guardar a Excel
    df_tareas.to_excel(tareas_path, index=False)

    return df_tareas

#def mostrar_tareas():
#    st.header("📝 Tareas en Curso")
#
#    # Contenedor para la última actualización
#    update_container = st.empty()
#
#    tareas_path = "data/tareas.xlsx"
#    if os.path.exists(tareas_path):
#        try:
#            # Leer el archivo cada vez que se llama a la función
#            tareas_df = pd.read_excel(tareas_path)
#
#            # Mostrar última actualización
#            ultima_act = tareas_df["Última Actualización"].max() if "Última Actualización" in tareas_df.columns else "No disponible"
#            update_container.info(f"🕒 Última actualización: {ultima_act}")
#
#            # Filtros en dos columnas
#            col1, col2 = st.columns(2)
#            with col1:
#                filtro_grupo = st.selectbox("🔍 Filtrar por grupo", ["Todos"] + GRUPOS)
#            with col2:
#                filtro_estado = st.selectbox("🔄 Filtrar por estado", ESTADOS)
#
#            # Aplicar filtros
#            df_filtrado = tareas_df.copy()
#            if filtro_grupo != "Todos":
#                df_filtrado = df_filtrado[df_filtrado["Grupo"] == filtro_grupo]
#            if filtro_estado != "Todos":
#                df_filtrado = df_filtrado[df_filtrado["Estado"] == filtro_estado]
#
#            # Mostrar métricas
#            col1, col2, col3 = st.columns(3)
#            with col1:
#                st.metric("Total Tareas", len(df_filtrado))
#            with col2:
#                completadas = len(df_filtrado[df_filtrado["Estado"] == "Completada"])
#                st.metric("Completadas", completadas)
#            with col3:
#                pendientes = len(df_filtrado[df_filtrado["Estado"] != "Completada"])
#                st.metric("Pendientes", pendientes)
#
#            # Mostrar tabla con formato mejorado
#            st.dataframe(
#                df_filtrado,
#                use_container_width=True,
#                column_config={
#                    "ID": st.column_config.TextColumn("ID", width=80),
#                    "Grupo": st.column_config.TextColumn("Grupo", width=100),
#                    "Responsable": st.column_config.TextColumn("Responsable", width=150),
#                    "Descripción": st.column_config.TextColumn("Descripción", width="medium"),
#                    "Estado": st.column_config.TextColumn("Estado", width=100),
#                    "% Avance": st.column_config.ProgressColumn(
#                        "Avance",
#                        width=100,
#                        format="%d%%",
#                        min_value=0,
#                        max_value=100,
#                    ),
#                }
#            )
#
#            return df_filtrado
#
#        except Exception as e:
#            st.error(f"❌ Error al leer el archivo de tareas: {e}")
#            return pd.DataFrame()
#    else:
#        st.warning("⚠️ No hay tareas registradas")
#        return pd.DataFrame()

def mostrar_tareas():
    st.header("📝 Tareas en Curso")

    # Verificar si existe el archivo de tareas, si no, cargar datos iniciales
    tareas_path = "data/tareas.xlsx"
    if not os.path.exists(tareas_path):
        with st.spinner("Cargando datos iniciales..."):
            cargar_datos_iniciales()
            st.success("✅ Datos iniciales cargados correctamente")

    # Contenedor para la última actualización
    update_container = st.empty()

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
                "Fecha inicio": st.column_config.DateColumn("Inicio", format="DD/MM/YYYY"),
                "Fecha fin": st.column_config.DateColumn("Fin", format="DD/MM/YYYY"),
            }
        )

        # Agregar botón para restablecer datos iniciales
        with st.expander("🔄 Opciones avanzadas"):
            if st.button("Restablecer datos iniciales"):
                with st.spinner("Restableciendo datos..."):
                    cargar_datos_iniciales()
                    st.success("✅ Datos restablecidos correctamente")
                    st.rerun()

        return df_filtrado

    except Exception as e:
        st.error(f"❌ Error al leer el archivo de tareas: {e}")
        return pd.DataFrame()




