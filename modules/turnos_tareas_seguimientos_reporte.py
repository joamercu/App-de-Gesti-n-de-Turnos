import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import os

def cargar_datos():
    """Carga los datos necesarios para el seguimiento"""
    try:
        # Cargar datos de tareas
        df_tareas = pd.read_excel("data/tareas.xlsx")

        # Cargar datos de transferencias si existe
        try:
            df_transferencias = pd.read_excel("data/transferencias.xlsx")
        except:
            df_transferencias = pd.DataFrame()

        return df_tareas, df_transferencias
    except Exception as e:
        st.error(f"Error al cargar datos: {str(e)}")
        return None, None

def mostrar_metricas_generales(df_tareas):
    """Muestra métricas generales del seguimiento de tareas"""
    st.subheader("📊 Métricas Generales")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_tareas = len(df_tareas)
        st.metric("Total Tareas", total_tareas)

    with col2:
        tareas_completadas = len(df_tareas[df_tareas["Estado"] == "Completada"])
        porcentaje_completadas = (tareas_completadas / total_tareas * 100) if total_tareas > 0 else 0
        st.metric("Tareas Completadas", f"{tareas_completadas} ({porcentaje_completadas:.1f}%)")

    with col3:
        tareas_curso = len(df_tareas[df_tareas["Estado"] == "En curso"])
        st.metric("Tareas en Curso", tareas_curso)

    with col4:
        avance_promedio = df_tareas["% Avance"].mean()
        st.metric("Avance Promedio", f"{avance_promedio:.1f}%")

def generar_grafico_estado_tareas(df_tareas):
    """Genera gráfico de estado de tareas por grupo"""
    # Preparar datos
    estado_grupo = df_tareas.groupby(['Grupo', 'Estado']).size().reset_index(name='Cantidad')

    # Crear gráfico
    fig = px.bar(estado_grupo,
                 x='Grupo',
                 y='Cantidad',
                 color='Estado',
                 title='Estado de Tareas por Grupo',
                 barmode='group')

    st.plotly_chart(fig, use_container_width=True)

def generar_grafico_avance_tiempo(df_tareas):
    """Genera gráfico de avance de tareas en el tiempo"""
    # Convertir historial de string JSON a datos
    def extraer_historial(historial_str):
        try:
            historial = json.loads(historial_str)
            return pd.DataFrame(historial)
        except:
            return pd.DataFrame()

    # Preparar datos para el gráfico
    datos_avance = []
    for _, tarea in df_tareas.iterrows():
        historial_df = extraer_historial(tarea['Historial'])
        if not historial_df.empty:
            historial_df['ID_Tarea'] = tarea['ID']
            historial_df['Grupo'] = tarea['Grupo']
            datos_avance.append(historial_df)

    if datos_avance:
        df_avance = pd.concat(datos_avance)
        df_avance['fecha'] = pd.to_datetime(df_avance['fecha'])

        fig = px.line(df_avance,
                     x='fecha',
                     y='avance',
                     color='ID_Tarea',
                     title='Progreso de Tareas en el Tiempo',
                     labels={'fecha': 'Fecha', 'avance': '% Avance'})

        st.plotly_chart(fig, use_container_width=True)

def mostrar_tabla_seguimiento(df_tareas):
    """Muestra tabla de seguimiento con filtros"""
    st.subheader("📋 Tabla de Seguimiento")

    df_tareas = df_tareas.rename(columns={
        "Descripcion": "Descripción",
        "Ultima Actualizacion": "Última Actualización"
    })

    # Filtros
    col1, col2, col3 = st.columns(3)

    with col1:
        grupos = ["Todos"] + list(df_tareas["Grupo"].unique())
        grupo_filtro = st.selectbox("Filtrar por Grupo", grupos)

    with col2:
        estados = ["Todos"] + list(df_tareas["Estado"].unique())
        estado_filtro = st.selectbox("Filtrar por Estado", estados)

    with col3:
        fecha_filtro = st.date_input("Filtrar por Fecha (desde)",
                                    value=datetime.now() - timedelta(days=30))

    # Aplicar filtros
    df_filtrado = df_tareas.copy()

    if grupo_filtro != "Todos":
        df_filtrado = df_filtrado[df_filtrado["Grupo"] == grupo_filtro]

    if estado_filtro != "Todos":
        df_filtrado = df_filtrado[df_filtrado["Estado"] == estado_filtro]

    df_filtrado = df_filtrado[pd.to_datetime(df_filtrado["Fecha inicio"]) >= pd.to_datetime(fecha_filtro)]


    # Mostrar tabla
    columnas_mostrar = [
        "ID", "Grupo", "Responsable", "Descripción", "Estado",
        "% Avance", "Fecha inicio", "Fecha estimada", "Última Actualización"
    ]

    st.dataframe(df_filtrado[columnas_mostrar], use_container_width=True)

def analizar_transferencias(df_transferencias):
    """Analiza y muestra estadísticas de transferencias"""
    if not df_transferencias.empty:
        st.subheader("🔄 Análisis de Transferencias")

        col1, col2 = st.columns(2)

        with col1:
            # Transferencias por grupo
            trans_grupo = df_transferencias.groupby('Grupo_Entrega').size()
            fig = px.pie(values=trans_grupo.values,
                        names=trans_grupo.index,
                        title='Transferencias por Grupo')
            st.plotly_chart(fig)

        with col2:
            # Timeline de transferencias
            df_transferencias['Fecha'] = pd.to_datetime(df_transferencias['Fecha'])
            trans_tiempo = df_transferencias.groupby('Fecha').size().reset_index(name='Cantidad')

            fig = px.line(trans_tiempo,
                         x='Fecha',
                         y='Cantidad',
                         title='Transferencias en el Tiempo')
            st.plotly_chart(fig)

def mostrar_seguimiento():
    """Función principal para mostrar el seguimiento"""
    st.title("📊 Seguimiento de Turnos y Tareas")

    # Cargar datos
    df_tareas, df_transferencias = cargar_datos()

    if df_tareas is not None:
        # Mostrar métricas generales
        mostrar_metricas_generales(df_tareas)

        # Pestañas para diferentes vistas
        tab1, tab2, tab3 = st.tabs([
            "📈 Gráficos de Progreso",
            "📋 Seguimiento Detallado",
            "🔄 Análisis de Transferencias"
        ])

        with tab1:
            generar_grafico_estado_tareas(df_tareas)
            generar_grafico_avance_tiempo(df_tareas)

        with tab2:
            mostrar_tabla_seguimiento(df_tareas)

        with tab3:
            if df_transferencias is not None and not df_transferencias.empty:
                analizar_transferencias(df_transferencias)
            else:
                st.info("No hay datos de transferencias disponibles")

        # Exportar datos
        if st.button("📥 Exportar Reporte"):
            # Crear reporte en Excel con todos los análisis
            try:
                with pd.ExcelWriter("data/reporte_seguimiento.xlsx") as writer:
                    df_tareas.to_excel(writer, sheet_name="Tareas", index=False)
                    if not df_transferencias.empty:
                        df_transferencias.to_excel(writer, sheet_name="Transferencias", index=False)

                st.success("✅ Reporte exportado exitosamente!")

            except Exception as e:
                st.error(f"❌ Error al exportar reporte: {str(e)}")

if __name__ == "__main__":
    mostrar_seguimiento()