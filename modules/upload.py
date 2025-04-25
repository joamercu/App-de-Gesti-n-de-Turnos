# Archivo: upload.py
import streamlit as st
import pandas as pd
import os
from PIL import Image
from datetime import datetime



def cargar_excel_estado():
    st.header("📤 Cargar estado actualizado de tareas")

    # Crear una columna para el estado de la operación
    status_container = st.empty()

    archivo = st.file_uploader("Selecciona un archivo Excel (.xlsx)", type=["xlsx"])

    columnas_requeridas = {"ID", "Grupo", "Estado", "% Avance"}

    if archivo is not None:
        try:
            # Leer el archivo subido
            df = pd.read_excel(archivo)

            # Verificar columnas
            if not columnas_requeridas.issubset(set(df.columns)):
                status_container.error(f"❌ El archivo debe contener las columnas: {', '.join(columnas_requeridas)}")
                return None

            # Mostrar preview de los cambios
            st.subheader("📋 Vista previa de los cambios")

            # Leer archivo actual de tareas si existe
            tareas_path = "data/tareas.xlsx"
            if os.path.exists(tareas_path):
                df_tareas_actual = pd.read_excel(tareas_path)

                # Crear DataFrame para mostrar los cambios
                cambios = []
                for i, row in df.iterrows():
                    tarea_actual = df_tareas_actual[df_tareas_actual["ID"] == row["ID"]]
                    if not tarea_actual.empty:
                        estado_anterior = tarea_actual.iloc[0]["Estado"]
                        estado_nuevo = row["Estado"]
                        avance_anterior = tarea_actual.iloc[0].get("% Avance", 0)
                        avance_nuevo = row.get("% Avance", 0)

                        if estado_anterior != estado_nuevo or avance_anterior != avance_nuevo:
                            cambios.append({
                                "ID": row["ID"],
                                "Grupo": row["Grupo"],
                                "Estado Anterior": estado_anterior,
                                "Nuevo Estado": estado_nuevo,
                                "Avance Anterior": avance_anterior,
                                "Nuevo Avance": avance_nuevo
                            })

                if cambios:
                    st.dataframe(pd.DataFrame(cambios), use_container_width=True)
                else:
                    st.info("ℹ️ No hay cambios para aplicar")
                    return None

                # Botón para aplicar cambios
                if st.button("📥 Aplicar cambios a tareas"):
                    try:
                        # Aplicar actualizaciones por ID
                        for i, row in df.iterrows():
                            idx = df_tareas_actual[df_tareas_actual["ID"] == row["ID"]].index
                            if not idx.empty:
                                for campo in ["Estado", "% Avance"]:
                                    if campo in df.columns:
                                        df_tareas_actual.loc[idx, campo] = row[campo]

                        # Agregar timestamp de última actualización
                        df_tareas_actual["Última Actualización"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                        # Guardar cambios
                        df_tareas_actual.to_excel(tareas_path, index=False)

                        # Mostrar mensaje de éxito
                        status_container.success("✅ Tareas actualizadas correctamente!")

                        # Agregar botón para ver tareas actualizadas
                        if st.button("👀 Ver Tareas Actualizadas"):
                            st.session_state.modulo = "Tareas en Curso"
                            st.rerun()

                    except Exception as e:
                        status_container.error(f"❌ Error al actualizar tareas: {str(e)}")
            else:
                status_container.error("❌ No se encontró el archivo de tareas base.")

        except Exception as e:
            status_container.error(f"❌ Error al leer el archivo: {str(e)}")

    return None


def cargar_fotos_referencia():
    st.header("📸 Subir imágenes de referencia de la tarea")

    imagenes = st.file_uploader(
        "Carga hasta 3 imágenes",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True
    )

    fotos_guardadas = []

    if imagenes:
        os.makedirs("data/fotos", exist_ok=True)

        for i, img in enumerate(imagenes[:3]):
            ruta = os.path.join("data", "fotos", img.name)
            with open(ruta, "wb") as f:
                f.write(img.getbuffer())
            fotos_guardadas.append(ruta)

            st.image(Image.open(ruta), caption=f"Imagen {i+1}", use_column_width=True)

    return fotos_guardadas
