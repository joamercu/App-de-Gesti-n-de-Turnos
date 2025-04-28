# Archivo: reloj.py
import streamlit as st
from datetime import datetime, timedelta
import pytz
import pandas as pd

from modules.config_turnos import  FECHA_INICIO_GRUPOS
from modules.grupos import GRUPOS_DETALLE
from modules.config_turnos import grupo_activo

from modules.grupos import GRUPOS_DETALLE

from modules.grupos import obtener_grupos_como_string


def mostrar_reloj():
    tz = pytz.timezone("America/Bogota")
    fecha_hoy = datetime.now(tz)
    ahora = datetime.now(tz)  # <--- definida aquí

    activos = grupo_activo(ahora)  # <--- también aquí

    st.metric("🕓 Fecha y hora actual", fecha_hoy.strftime("%A, %d de %B de %Y - %H:%M:%S"))

    # Obtener estados activos/inactivos
    estados = grupo_activo(ahora)
    # estados es lista de tuplas (grupo, estado, dias_rest)
    # Obtener grupos actualizados
    GRUPOS_DETALLE = obtener_grupos_como_string()

    ## Mostrar métrica de grupos en turno
    #nombres_activos = [g for g, e, d in estados if e == 'trabajo']
    #st.metric("👷‍♂️ Grupo(s) activos (trabajo)", ", ".join(nombres_activos))

    info_turnos = []
    for grupo, _, _ in activos:
        inicio = FECHA_INICIO_GRUPOS[grupo]
        dias_transcurridos = (ahora - inicio).days % 21
        dias_restantes = 14 - dias_transcurridos if dias_transcurridos < 14 else 0
        if dias_restantes > 0:
            info_turnos.append(f"{grupo}: {dias_restantes} días restantes")

    st.metric("👷‍♂️ Grupo(s) activos (trabajo)", " | ".join(info_turnos))

    # Calcular días restantes para grupos activos
    grupos_activos = []

    for grupo, _, _ in activos:
        inicio = FECHA_INICIO_GRUPOS[grupo]
        dias_transcurridos = (ahora - inicio).days % 21
        dias_restantes = 14 - dias_transcurridos if dias_transcurridos < 14 else 0
        if dias_restantes > 0:

            grupos_activos.append(grupo)

    # Luego mostramos solo los integrantes de los grupos activos
    for grupo in grupos_activos:
        st.markdown(f"**👥 {grupo} - Integrantes en turno:**")
        integrantes = GRUPOS_DETALLE.get(grupo, "No definido").split(", ")
        df_integrantes = pd.DataFrame({"Integrantes": integrantes})
        st.table(df_integrantes)









    #df_tiempo = pd.DataFrame([
    #    {"Grupo": grupo, "Días restantes": 14 - (ahora - FECHA_INICIO_GRUPOS[grupo]).days % 21
    #    if (ahora - FECHA_INICIO_GRUPOS[grupo]).days % 21 < 14 else 0}
    #    for grupo, _, _ in activos
    #])
    #st.table(df_tiempo)
    #
    #df_tiempo = pd.DataFrame([
    #    {
    #        "Grupo": grupo,
    #        "Días restantes": 14 - (ahora - FECHA_INICIO_GRUPOS[grupo]).days % 21
    #        if (ahora - FECHA_INICIO_GRUPOS[grupo]).days % 21 < 14 else 0,
    #        "Integrantes": ", ".join(GRUPOS_DETALLE.get(grupo, []))
    #    }
    #    for grupo, _, _ in activos
    #])
    #
    #st.subheader("⏳ Tiempo restante del turno")
    #st.table(df_tiempo)
    #
    ## Supongamos que 'activos' ya contiene los grupos en turno con tupla (grupo, estado, días_rest)
    #info_turnos = []
    #
    #for grupo, estado, _ in activos:
    #    inicio = FECHA_INICIO_GRUPOS[grupo]
    #    dias_transcurridos = (ahora - inicio).days % 21
    #    dias_restantes = 14 - dias_transcurridos if dias_transcurridos < 14 else 0
    #
    #    integrantes = ", ".join(GRUPOS_DETALLE.get(grupo, []))  # <- CORRECTO
    #    info_turnos.append({
    #        "Grupo": grupo,
    #        "Días restantes": dias_restantes,
    #        "Integrantes": integrantes
    #    })
    #
    # Crear DataFrame limpio y ordenado
    df_turnos = pd.DataFrame(info_turnos)

    ## Mostrar tabla verticalmente centrada
    #st.subheader("📋 Grupos activos y tiempo restante")
    #st.dataframe(df_turnos, use_container_width=True)



    ## Construir DataFrame de estados
    #df_estados = pd.DataFrame([
    #    {
    #        'Grupo': g,
    #        'Estado': e.capitalize(),
    #        'Días restantes': d,
    #        'Integrantes': ", ".join(GRUPOS_DETALLE.get(g, []))
    #    }
    #    for g, e, d in estados
    #])

    ## Mostrar integrantes actuales en formato tabla
    #for grupo, _, _ in activos:
    #    st.markdown(f"**👥 {grupo} - Integrantes en turno:**")
    #    integrantes = GRUPOS_DETALLE.get(grupo, "No definido").split(", ")
    #    df_integrantes = pd.DataFrame({"Integrantes": integrantes})
    #    st.table(df_integrantes)
    #

    # Determinar próximo grupo en entrar y mostrar integrantes
    dias_para_entrada = []
    for grupo, inicio in FECHA_INICIO_GRUPOS.items():
        dias_transcurridos = (ahora - inicio).days % 21
        if dias_transcurridos >= 14:
            dias_faltan = 21 - dias_transcurridos
            dias_para_entrada.append((grupo, dias_faltan))
    if dias_para_entrada:
        proximo = sorted(dias_para_entrada, key=lambda x: x[1])[0]
        st.markdown("---")
        st.subheader(f"📅 Próximo grupo en entrar: {proximo[0]} en {proximo[1]} días")
        integrantes_proximo = GRUPOS_DETALLE.get(proximo[0], "No definido").split(", ")
        st.table(pd.DataFrame({"Integrantes": integrantes_proximo}))

    # Mostrar últimas 5 tareas si existe el archivo de tareas
    try:
        df_tareas = pd.read_excel("data/tareas.xlsx")
        st.markdown("---")
        st.subheader("🧾 Últimas 10 tareas Asignadas")
        st.dataframe(df_tareas.tail(10), use_container_width=True)
    except Exception as e:
        st.info("ℹ️ No se encontraron tareas recientes o el archivo no está disponible.")


#def mostrar_reloj():
#    tz = pytz.timezone('America/Bogota')
#    ahora = datetime.now(tz)
#
#    # Mostrar fecha y hora actual
#    st.metric("🕓 Fecha y hora actual",
#              ahora.strftime("%A, %d de %B de %Y - %H:%M:%S"))
#
#    # Obtener estados activos/inactivos
#    estados = grupo_activo(ahora)
#    # estados es lista de tuplas (grupo, estado, dias_rest)
#
#    # Mostrar métrica de grupos en turno
#    nombres_activos = [g for g, e, d in estados if e == 'trabajo']
#    st.metric("👷‍♂️ Grupo(s) activos (trabajo)", ", ".join(nombres_activos))
#
#    # Construir DataFrame de estados
#    df_estados = pd.DataFrame([
#        {
#            'Grupo': g,
#            'Estado': e.capitalize(),
#            'Días restantes': d,
#            'Integrantes': ", ".join(GRUPOS_DETALLE.get(g, []))
#        }
#        for g, e, d in estados
#    ])
#
#    # Mostrar tabla de estado de turnos
#    st.subheader("📊 Detalle de estado de cada grupo")
#    st.table(df_estados)
#
#    # Botón para previsualizar calendario del mes
#    if st.button("📅 Ver calendario del mes actual"):
#        from modules.calendario import mostrar_calendario_turnos
#        mostrar_calendario_turnos()
#



