import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime, timedelta
from PIL import Image

# Constantes y configuraciones
TAREAS_PATH = "data/tareas.xlsx"
FOTOS_PATH = "data/fotos"
ESTADOS_TAREA = ["Pendiente", "En curso", "Pausada", "Completada"]
PRIORIDADES = ["Alta", "Media", "Baja"]

def cargar_grupos():
    """Carga los grupos disponibles desde config_turnos.py"""
    try:
        from config_turnos import GRUPOS
        return GRUPOS
    except ImportError:
        return ["Grupo A", "Grupo B", "Grupo C","Grupo D"]


def cargar_df_tareas():
    """Carga o crea el DataFrame de tareas con las columnas correctas"""
    columnas = [
        "ID", "Grupo", "Responsable", "Descripcion", "Estado",
        "% Avance", "Prioridad", "Fecha inicio", "Fecha fin",
        "Fecha estimada", "Observaciones", "Historial",
        "Ultima Actualizacion", "Foto_1", "Foto_2", "Foto_3"
    ]

    if os.path.exists(TAREAS_PATH):
        try:
            df = pd.read_excel(TAREAS_PATH)
            # Asegurar que todas las columnas necesarias existen
            for col in columnas:
                if col not in df.columns:
                    df[col] = None
            return df
        except Exception as e:
            st.error(f"Error al cargar el archivo de tareas: {str(e)}")
            return pd.DataFrame(columns=columnas)
    else:
        return pd.DataFrame(columns=columnas)

def guardar_foto(foto):
    """Guarda una foto en el directorio de fotos y retorna la ruta"""
    if foto:
        os.makedirs(FOTOS_PATH, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{foto.name}"
        ruta = os.path.join(FOTOS_PATH, filename)

        # Procesar y optimizar la imagen
        with Image.open(foto) as img:
            # Redimensionar si es muy grande
            if max(img.size) > 1920:
                img.thumbnail((1920, 1920))
            # Guardar con optimización
            img.save(ruta, optimize=True, quality=85)

        return ruta
    return None

def mostrar_formulario_tarea(tarea=None, modo="crear"):
    """Muestra el formulario para crear o editar una tarea"""
    grupos = cargar_grupos()

    with st.form(f"{modo}_tarea_form"):
        col1, col2 = st.columns(2)

        with col1:
            grupo = st.selectbox(
                "Grupo", grupos,
                index=grupos.index(tarea["Grupo"]) if tarea else 0
            )
            responsable = st.text_input(
                "Responsable",
                value=tarea["Responsable"] if tarea else ""
            )
            prioridad = st.selectbox(
                "Prioridad", PRIORIDADES,
                index=PRIORIDADES.index(tarea["Prioridad"]) if tarea and "Prioridad" in tarea else 0
            )
            estado = st.selectbox(
                "Estado", ESTADOS_TAREA,
                index=ESTADOS_TAREA.index(tarea["Estado"]) if tarea else 0
            )
            avance = st.slider(
                "% Avance", 0, 100,
                value=int(tarea["% Avance"]) if tarea else 0
            )

        with col2:
            fecha_inicio = st.date_input(
                "Fecha de inicio",
                value=pd.to_datetime(tarea["Fecha inicio"]).date() if tarea else datetime.now()
            )
            fecha_estimada = st.date_input(
                "Fecha estimada de finalización",
                value=pd.to_datetime(tarea["Fecha estimada"]).date() if tarea and pd.notna(tarea["Fecha estimada"])
                else datetime.now() + timedelta(days=7)
            )
            if estado == "Completada":
                fecha_fin = st.date_input(
                    "Fecha de finalización",
                    value=pd.to_datetime(tarea["Fecha fin"]).date() if tarea and pd.notna(tarea["Fecha fin"])
                    else datetime.now()
                )
            else:
                fecha_fin = None

        descripcion = st.text_area(
            "Descripción de la tarea",
            value=tarea["Descripción"] if tarea else ""
        )
        observaciones = st.text_area(
            "Observaciones (opcional)",
            value=tarea["Observaciones"] if tarea and pd.notna(tarea["Observaciones"]) else ""
        )

        # Manejo de fotos
        st.write("### 📸 Imágenes de referencia (opcional)")
        col1, col2, col3 = st.columns(3)
        fotos = []

        for i, col in enumerate([col1, col2, col3]):
            with col:
                foto_actual = tarea[f"Foto_{i+1}"] if tarea and pd.notna(tarea[f"Foto_{i+1}"]) else None
                if foto_actual:
                    st.image(foto_actual, caption=f"Foto {i+1} actual")

                nueva_foto = st.file_uploader(
                    f"{'Actualizar' if foto_actual else 'Subir'} Foto {i+1}",
                    type=["jpg", "jpeg", "png"],
                    key=f"foto_{modo}_{i+1}"
                )

                if nueva_foto:
                    fotos.append(guardar_foto(nueva_foto))
                    st.image(nueva_foto)
                else:
                    fotos.append(foto_actual)

        submitted = st.form_submit_button("💾 Guardar Tarea")

        if submitted:
            return {
                "grupo": grupo,
                "responsable": responsable,
                "descripcion": descripcion,
                "estado": estado,
                "avance": avance,
                "prioridad": prioridad,
                "fecha_inicio": fecha_inicio,
                "fecha_estimada": fecha_estimada,
                "fecha_fin": fecha_fin,
                "observaciones": observaciones,
                "fotos": fotos
            }
        return None

def crear_nueva_tarea():
    st.subheader("🆕 Crear Nueva Tarea")

    df_tareas = cargar_df_tareas()

    # Generar nuevo ID
    ultimo_id = df_tareas["ID"].max() if not df_tareas.empty else "T000"
    nuevo_num = int(ultimo_id.replace("T", "")) + 1
    nuevo_id = f"T{nuevo_num:03d}"

    datos = mostrar_formulario_tarea(modo="crear")

    if datos:
        try:
            nueva_tarea = {
                "ID": nuevo_id,
                "Grupo": datos["grupo"],
                "Responsable": datos["responsable"],
                "Descripción": datos["descripcion"],
                "Estado": datos["estado"],
                "% Avance": datos["avance"],
                "Prioridad": datos["prioridad"],
                "Fecha inicio": datos["fecha_inicio"].strftime("%Y-%m-%d"),
                "Fecha estimada": datos["fecha_estimada"].strftime("%Y-%m-%d"),
                "Fecha fin": datos["fecha_fin"].strftime("%Y-%m-%d") if datos["fecha_fin"] else None,
                "Observaciones": datos["observaciones"],
                "Última Actualización": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Historial": json.dumps([{
                    "fecha": datetime.now().strftime("%Y-%m-%d"),
                    "estado": datos["estado"],
                    "avance": datos["avance"],
                    "usuario": st.session_state.get("usuario", "sistema"),
                    "accion": "creación"
                }]),
                "Foto_1": datos["fotos"][0] if len(datos["fotos"]) > 0 else None,
                "Foto_2": datos["fotos"][1] if len(datos["fotos"]) > 1 else None,
                "Foto_3": datos["fotos"][2] if len(datos["fotos"]) > 2 else None
            }

            df_tareas = pd.concat([df_tareas, pd.DataFrame([nueva_tarea])], ignore_index=True)
            df_tareas.to_excel(TAREAS_PATH, index=False)

            st.success(f"✅ Tarea {nuevo_id} creada exitosamente!")

            if st.button("📝 Crear otra tarea"):
                st.rerun()

        except Exception as e:
            st.error(f"❌ Error al crear la tarea: {str(e)}")

def editar_tarea_existente():
    st.subheader("✏️ Editar Tarea Existente")

    df_tareas = cargar_df_tareas()

    if df_tareas.empty:
        st.warning("No hay tareas disponibles para editar")
        return

    # Crear opciones para el selector de tareas
    try:
        tareas_dict = {}
        for _, row in df_tareas.iterrows():
            id_tarea = str(row.get('ID', ''))
            descripcion = str(row.get('Descripcion', ''))
            if id_tarea and descripcion:
                # Limitar la descripción a 50 caracteres
                desc_corta = descripcion[:50] + '...' if len(descripcion) > 50 else descripcion
                key = f"{id_tarea} - {desc_corta}"
                tareas_dict[key] = id_tarea

        if not tareas_dict:
            st.warning("No hay tareas disponibles para editar")
            return

        # Selector de tarea
        tarea_seleccionada = st.selectbox(
            "Seleccione la tarea a editar",
            options=list(tareas_dict.keys())
        )

        if tarea_seleccionada:
            id_tarea = tareas_dict[tarea_seleccionada]
            tarea = df_tareas[df_tareas['ID'] == id_tarea].iloc[0]

            # Aquí continúa el código para editar la tarea...
            with st.form("editar_tarea_form"):
                # Campos del formulario
                col1, col2 = st.columns(2)

                with col1:
                    grupo = st.selectbox(
                        "Grupo",
                        ["Grupo A", "Grupo B", "Grupo C", "Grupo D"],
                        index=["Grupo A", "Grupo B", "Grupo C", "Grupo D"].index(tarea.get('Grupo', 'Grupo A'))
                    )
                    responsable = st.text_input("Responsable", value=str(tarea.get('Responsable', '')))
                    estado = st.selectbox(
                        "Estado",
                        ["Pendiente", "En curso", "Pausada", "Completada"],
                        index=["Pendiente", "En curso", "Pausada", "Completada"].index(tarea.get('Estado', 'Pendiente'))
                    )
                    avance = st.slider("% Avance", 0, 100, int(tarea.get('% Avance', 0)))

                with col2:
                    fecha_inicio_val = tarea.get('Fecha inicio', None)
                    if pd.notna(fecha_inicio_val):
                        fecha_inicio_val = pd.to_datetime(fecha_inicio_val).date()
                    else:
                        fecha_inicio_val = datetime.now().date()
                    fecha_inicio = st.date_input("Fecha de inicio", value=fecha_inicio_val)

                    # Agregar este bloque para fecha_estimada
                    fecha_estimada_val = tarea.get('Fecha estimada', None)
                    if pd.notna(fecha_estimada_val):
                        fecha_estimada_val = pd.to_datetime(fecha_estimada_val).date()
                    else:
                        fecha_estimada_val = datetime.now().date()
                    fecha_estimada = st.date_input("Fecha estimada", value=fecha_estimada_val)

                descripcion = st.text_area("Descripción", value=str(tarea.get('Descripcion', '')))
                observaciones = st.text_area("Observaciones", value=str(tarea.get('Observaciones', '')))

                submitted = st.form_submit_button("💾 Guardar Cambios")

                if submitted:
                    try:
                        # Actualizar los datos
                        idx = df_tareas[df_tareas['ID'] == id_tarea].index[0]
                        df_tareas.loc[idx, 'Grupo'] = grupo
                        df_tareas.loc[idx, 'Responsable'] = responsable
                        df_tareas.loc[idx, 'Estado'] = estado
                        df_tareas.loc[idx, '% Avance'] = avance
                        df_tareas.loc[idx, 'Descripcion'] = descripcion
                        df_tareas.loc[idx, 'Observaciones'] = observaciones
                        df_tareas.loc[idx, 'Fecha inicio'] = fecha_inicio.strftime("%Y-%m-%d")
                        df_tareas.loc[idx, 'Fecha estimada'] = fecha_estimada.strftime("%Y-%m-%d")
                        df_tareas.loc[idx, 'Ultima Actualizacion'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                        # Guardar cambios
                        df_tareas.to_excel(TAREAS_PATH, index=False)
                        st.success(f"✅ Tarea {id_tarea} actualizada exitosamente!")

                    except Exception as e:
                        st.error(f"❌ Error al actualizar la tarea: {str(e)}")

    except Exception as e:
        st.error(f"Error al procesar las tareas: {str(e)}")

def formulario_tareas():
    st.header("📝 Gestión de Tareas")

    # Selector de modo
    modo = st.radio(
        "Seleccione una acción:",
        ["Crear Nueva Tarea", "Editar Tarea Existente"],
        horizontal=True
    )

    if modo == "Crear Nueva Tarea":
        crear_nueva_tarea()
    else:
        editar_tarea_existente()

if __name__ == "__main__":
    formulario_tareas()