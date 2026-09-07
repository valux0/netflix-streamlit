import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuración de la página (esto debe ir al principio)
st.set_page_config(
    page_title="Netflix Data Dashboard", 
    page_icon="🍿", 
    layout="wide"
)

# Estilo personalizado para el título
st.markdown("<h1 style='text-align: center; color: #E50914;'>🎬 Netflix: Movies & TV Shows Analysis</h1>", unsafe_allow_html=True)
st.markdown("---")

# 2. Función para cargar datos
@st.cache_data
def load_data():
    # Cargamos el archivo
    df = pd.read_csv('dataset/netflix_titles.csv')
    
    # LIMPIEZA: Quitamos espacios y corregimos fechas
    df['date_added'] = df['date_added'].str.strip()
    df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
    df['year_added'] = df['date_added'].dt.year
    
    # Eliminamos filas que quedaron sin año de agregado para evitar errores en gráficas
    df = df.dropna(subset=['year_added'])
    return df

# Cargar los datos base
df_raw = load_data()

# 3. BARRA LATERAL (Filtros)
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/0/08/Netflix_2015_logo.svg", width=150)
st.sidebar.header("Filtros del Dataset")

# Filtro por Tipo (Movie o TV Show)
tipo_seleccionado = st.sidebar.multiselect(
    "Selecciona el Tipo:",
    options=df_raw['type'].unique(),
    default=df_raw['type'].unique()
)

# Filtro por Año de lanzamiento (Slider)
year_min = int(df_raw['release_year'].min())
year_max = int(df_raw['release_year'].max())
rango_años = st.sidebar.slider(
    "Rango de años de lanzamiento:",
    year_min, year_max, (2010, year_max)
)

# APLICAR FILTROS al DataFrame
df = df_raw[
    (df_raw['type'].isin(tipo_seleccionado)) & 
    (df_raw['release_year'].between(rango_años[0], rango_años[1]))
]

# 4. MÉTRICAS CLAVE (KPIs)
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total de Títulos", len(df))
with col2:
    st.metric("Películas", len(df[df['type'] == 'Movie']))
with col3:
    st.metric("Series de TV", len(df[df['type'] == 'TV Show']))

st.markdown("---")

# 5. BUSCADOR INTERACTIVO
st.subheader("🔍 Buscador de Títulos")
busqueda = st.text_input("Ingresa el nombre de una película o serie:")
if busqueda:
    resultados = df[df['title'].str.contains(busqueda, case=False, na=False)]
    if not resultados.empty:
        st.dataframe(resultados[['title', 'type', 'release_year', 'director', 'listed_in']])
    else:
        st.warning("No se encontraron resultados.")

st.markdown("---")

# 6. GRÁFICAS
col_left, col_right = st.columns(2)

with col_left:
    # Gráfica 1: Distribución
    st.subheader("📊 Distribución de Contenido")
    type_counts = df['type'].value_counts()
    fig1 = px.pie(
        values=type_counts.values, 
        names=type_counts.index, 
        hole=0.4,
        color_discrete_sequence=['#E50914', '#564d4d']
    )
    st.plotly_chart(fig1, use_container_width=True)

with col_right:
    # Gráfica 2: Top 10 Géneros
    st.subheader("🔝 Top 10 Géneros")
    top_genres = df['listed_in'].value_counts().head(10)
    fig2 = px.bar(
        x=top_genres.values, 
        y=top_genres.index, 
        orientation='h',
        labels={'x': 'Cantidad', 'y': 'Género'},
        color=top_genres.values,
        color_continuous_scale='Reds'
    )
    fig2.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig2, use_container_width=True)

# Gráfica 3: Evolución de contenido agregado (Línea de tiempo)
st.subheader("📈 Evolución de contenido agregado por año")
line_data = df['year_added'].value_counts().sort_index()
fig3 = px.line(
    x=line_data.index, 
    y=line_data.values,
    labels={'x': 'Año de carga a Netflix', 'y': 'Cantidad de títulos'},
    markers=True
)
fig3.update_traces(line_color='#E50914')
st.plotly_chart(fig3, use_container_width=True)

# 7. TABLA DE DATOS FINAL
if st.checkbox("Ver base de datos filtrada"):
    st.subheader("Datos Detallados")
    st.dataframe(df)

# Pie de página
st.markdown("---")
st.caption("Dashboard creado para la clase de Inteligencia Artificial - Datos de Netflix")