from functools import cache
from unicodedata import numeric
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt

#Importamos base de datos
df=pd.read_csv("Airbnb_limpio.csv")

st.set_page_config(page_title="Opciones de Airbnb en Mexico",
                   page_icon=":busts_in_silhouette:")

st.title("Airbnb en Ciudad de México")
st.markdown("Identifica el valor del espacio te gustaría promocionar en Airbnb y genera ingresos")

st.sidebar.image("Airbnb_logo.jpeg")
st.sidebar.markdown("##")


#Aplicamos cache a nuestros datos
@st.cache
def load_data(nrows):
    data = pd.read_csv("Airbnb_limpio.csv", nrows=nrows, encoding= "ISO-8859-1")
    lowercase = lambda x: str(x).lower()
    return data

data_load_state = st.text('Cargando datos..')
data = load_data(1000)
data_load_state.text("Datos cargados")

@st.cache
def load_data_del(neighbourhood):
  filtrodelegacion=df[df['neighbourhood'] == neighbourhood]
  return filtrodelegacion

selecdele = st.sidebar.selectbox("Selecciona la delegación",df['neighbourhood'].unique())
btnFilterbydel = st.sidebar.button("Filtro por delegación")

if (btnFilterbydel):
  filterdel = load_data_del(selecdele)
  count_row1 = filterdel.shape[0]
  st.write(f"Resultados encontrados: {count_row1}")
  st.title("Filtro por delegación")
  st.dataframe(filterdel)

price_min = st.sidebar.slider(
    "Precio mínimo",
    min_value=float(data['price'].min()),
    max_value=float(data['price'].max())
)
price_max = st.sidebar.slider(
    "Precio máximo",
    min_value=float(data['price'].min()),
    max_value=float(data['price'].max())
)
subset_price = data[ (data['price'] >= price_min) & (data['price'] <= price_max)]

st.write(f"Number of registros con precio entre {price_min} and {price_max}: {subset_price.shape[0]}")
st.write(subset_price)

@st.cache
def load_data_del(room_type):
  filtrotipo=df[df['room_type'] == room_type]

  return filtrotipo

seleccroom = st.sidebar.selectbox("Selecciona el tipo de habitación",df['room_type'].unique())
btnFilterbyroom = st.sidebar.button("Filtrar por tipo de habitación")

if (btnFilterbyroom):
  filterbyroom = load_data_del(seleccroom)
  count_row3 = filterbyroom.shape[0]
  st.write(f"Resultados totales: {count_row3}")
  st.title("Filtro por tipo de habitación")
  st.dataframe(filterbyroom)


histo= st.sidebar.checkbox("Distribución de precios propiedades")
if histo:
    fig, ax = plt.subplots()
    ax.hist(data.price)
    st.header("Distribución del precio de las habitaciones")
    st.pyplot(fig)
    st.markdown("_")


graf= st.sidebar.checkbox("Precios por propiedades") 
if graf:
    fig, ax = plt.subplots()
    x= data["room_type"]
    y=data["price"]
    ax.barh(x,y)
    ax.set_ylabel("Tipo de Espacio")
    ax.set_xlabel("Precio promedio de todas las propiedades")
    st.header("Propiedades por precio promedio")
    st.pyplot(fig)
    st.markdown("_")


graf1= st.sidebar.checkbox("Delegacion por el precio promedio") 
if graf1:
    fig, ax = plt.subplots()
    x= data["neighbourhood"]
    y=data["price"]
    ax.barh(x,y)
    ax.set_ylabel("Delegación")
    ax.set_xlabel("Precio promedio por delegación ")
    st.header("Delegacion con el precio")
    st.pyplot(fig)
    st.markdown("_")


#--- CONCLUSION ---#
agreeconc=st.sidebar.checkbox("Conclusión de la situación")
if agreeconc:
    st.markdown("Conclusión")
    st.markdown("Para conocer el precio que debes asignar a tu propiedad próxima a promocionarse en Airbnb es necesaria la implementación de algunos indicadores, mismos que se muestran en el dashboard generado con el equipo, la primera decisión es conocer el tipo de espacio que se estará ofreciendo y la ubicación.")
    st.markdown("Para la situación de Carina, al buscar ofrecer un departamento en la calle Cholula, cerca de la colonia Condensa, el Parque España y el Bosque de Chapultepec, con dos recámaras con camas matrimoniales, un baño, sala, comedor, cocina , área de lavado, servicio Wifi  y sin estacionamiento, el precio aproximado que podría estar solicitando se encuentra entre 1,400.00  y 1,699.00")