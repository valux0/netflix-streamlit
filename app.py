import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de la página
st.set_page_config(page_title="Netflix Dashboard", layout="wide")

st.title("📊 Análisis de Datos: Netflix Movies & TV Shows")

# Cargar el dataset
@st.cache_data # Para que no recargue el CSV cada vez que mueves algo
def load_data():
    df = pd.read_csv('dataset/netflix_titles.csv')
    return df

df = load_data()

# Mostrar los primeros datos
if st.checkbox('Mostrar primeras filas del dataset'):
    st.write(df.head())

# --- GRÁFICA 1: Distribución de Películas vs Series ---
st.subheader("¿Qué hay más: Películas o Series?")
type_counts = df['type'].value_counts()
fig1 = px.pie(values=type_counts.values, names=type_counts.index, hole=0.4)
st.plotly_chart(fig1)

# --- GRÁFICA 2: Evolución por año ---
st.subheader("Contenido agregado por año")
df['year_added'] = pd.to_datetime(df['date_added']).dt.year
release_year_counts = df['release_year'].value_counts().sort_index()
fig2 = px.line(x=release_year_counts.index, y=release_year_counts.values, labels={'x':'Año', 'y':'Cantidad'})
st.plotly_chart(fig2)