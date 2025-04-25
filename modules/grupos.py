# Archivo: modules/grupos.py
import streamlit as st
import pandas as pd
from datetime import datetime
import json

# Grupos predeterminados
GRUPOS_DETALLE = {
    "Grupo A": "Julio Montoya, Domingo Cuevas, Oscar Rubio, Julian Ramirez",
    "Grupo B": "Angel Oyuela, Juan Salguero, Miguel Varón, Fansisco Lasso",
    "Grupo C": "Jhon Castañeda, Luis Gomez, Hernan Osorio, Manuel Aramendis",
    "Grupo D": "Nelson Rubio, Manuel Castañeda, Cristian Osorio, Camilo Lemus"
}

# Crear lista de todo el personal disponible
PERSONAL_DISPONIBLE = list(set([
    persona.strip()
    for personas in GRUPOS_DETALLE.values()
    for persona in personas.split(',')
]))
PERSONAL_DISPONIBLE.sort()  # Ordenar alfabéticamente

def cargar_grupos():
    try:
        with open('data/grupos_config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Si no existe el archivo, usar los grupos predeterminados
        grupos_dict = {
            grupo: [p.strip() for p in personas.split(',')]
            for grupo, personas in GRUPOS_DETALLE.items()
        }
        guardar_grupos(grupos_dict)
        return grupos_dict

def guardar_grupos(grupos):
    with open('data/grupos_config.json', 'w') as f:
        json.dump(grupos, f, indent=4)

def gestionar_grupos():
    st.header("👥 Gestión de Grupos")

    # Cargar grupos existentes
    grupos = cargar_grupos()

    # Sección para crear nuevo grupo
    with st.expander("➕ Crear Nuevo Grupo", expanded=False):
        nuevo_grupo = st.text_input("Nombre del nuevo grupo")
        if nuevo_grupo:
            if nuevo_grupo not in grupos:
                personas_seleccionadas = st.multiselect(
                    "Seleccionar integrantes",
                    PERSONAL_DISPONIBLE,
                    key=f"nuevo_grupo_{nuevo_grupo}"
                )

                if st.button("Crear Grupo"):
                    grupos[nuevo_grupo] = personas_seleccionadas
                    guardar_grupos(grupos)
                    st.success(f"Grupo '{nuevo_grupo}' creado exitosamente!")
            else:
                st.warning("Este nombre de grupo ya existe.")

    # Sección para editar grupos existentes
    st.subheader("📝 Editar Grupos Existentes")

    for grupo_nombre in list(grupos.keys()):
        with st.expander(f"Grupo: {grupo_nombre}"):
            # Mostrar y permitir editar integrantes
            integrantes_actuales = grupos[grupo_nombre]
            nuevos_integrantes = st.multiselect(
                "Integrantes del grupo",
                PERSONAL_DISPONIBLE,
                default=integrantes_actuales,
                key=f"edit_{grupo_nombre}"
            )

            col1, col2 = st.columns(2)

            with col1:
                if st.button("Actualizar", key=f"update_{grupo_nombre}"):
                    grupos[grupo_nombre] = nuevos_integrantes
                    guardar_grupos(grupos)
                    st.success("Grupo actualizado!")

            with col2:
                if st.button("Eliminar Grupo", key=f"delete_{grupo_nombre}"):
                    del grupos[grupo_nombre]
                    guardar_grupos(grupos)
                    st.warning("Grupo eliminado!")
                    st.rerun()

    # Mostrar resumen de grupos
    st.subheader("📊 Resumen de Grupos")

    # Crear un DataFrame con todos los grupos
    all_groups_data = []
    for grupo, integrantes in grupos.items():
        for integrante in integrantes:
            all_groups_data.append({
                'Grupo': grupo,
                'Integrante': integrante
            })

    if all_groups_data:
        df = pd.DataFrame(all_groups_data)
        # Mostrar grupos en formato tabla agrupada
        for grupo in grupos.keys():
            st.write(f"**{grupo}**")
            grupo_df = df[df['Grupo'] == grupo][['Integrante']]
            st.table(grupo_df)

def obtener_grupos_como_string():
    """Convierte los grupos del formato JSON al formato string para compatibilidad"""
    grupos = cargar_grupos()
    return {
        grupo: ", ".join(integrantes)
        for grupo, integrantes in grupos.items()
    }