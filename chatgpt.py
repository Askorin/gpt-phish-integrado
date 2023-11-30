import os
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import streamlit as st
import constants
import react
import time

os.environ["OPENAI_API_KEY"] = constants.APIKEY

#Definir PromptTemplate
from langchain import PromptTemplate

# Page title
st.set_page_config(page_title='EmailCreator')
st.title('ProjectP0.1')
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    constants.APIKEY=openai_api_key
    os.environ["OPENAI_API_KEY"] = constants.APIKEY
# Text input
nombrep = st.text_input(
        "Nombre y Apellidos",
        None,
        key="nombrep",
        placeholder="Ej: Cristóbal González Muñoz",
        label_visibility="visible")

correop = st.text_input(
        "Correo electrónico",
        None,
        key="correop",
        placeholder="Ej: miguel.soto@gmail.com",
        label_visibility="visible")

direccionp = st.text_input(
        "Dirección domiciliaria",
        None,
        key="direccionp",
        placeholder="Ej: Av. Colón 1234, Depto. 56, Talcahuano, Región del Biobío",
        label_visibility="visible")

nacimientop = st.text_input(
        "Fecha de nacimiento",
        None,
        key="nacimientop",
        placeholder="Ej: 15 de agosto de 1995",
        label_visibility="visible")

telefonop = st.text_input(
        "Número de teléfono",
        None,
        key="telefonop",
        placeholder="Ej: +56 9 8765 4321",
        label_visibility="visible")

laboralp = st.text_input(
        "Experiencia laboral",
        None,
        key="laboralp",
        placeholder="Ej: Ingeniero civil industrial. 3 años trabajando en una empresa de consultoría en proyectos de optimización de procesos, gestión de calidad y mejora continua. He participado en diversos proyectos para clientes de distintos rubros, como minería, energía, salud y educación.",
        label_visibility="visible")

interesp = st.text_input(
        "Intereses",
        None,
        key="interesp",
        placeholder="Ej: Me gusta leer libros de negocios, innovación y desarrollo personal. Disfruto de viajar, conocer nuevas culturas y aprender idiomas. Practico deportes como fútbol, tenis y natación.",
        label_visibility="visible")

# Form to accept user's text input for summarization
result = []
with st.form('colecting_form', clear_on_submit=True):
    
    submitted = st.form_submit_button('Submit')
    if submitted:
        with st.spinner('Calculating...'):
            time.sleep(5)
            

            response = react.phishing_generator(nombrep,correop,direccionp,nacimientop,telefonop,laboralp,interesp)

            result.append(response)

if len(result):
    st.info(response)