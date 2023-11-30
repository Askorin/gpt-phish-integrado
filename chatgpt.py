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
#st.set_page_config(page_title='EmailCreator')
#st.title('ProjectP0.1')
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    constants.APIKEY=openai_api_key
    os.environ["OPENAI_API_KEY"] = constants.APIKEY

st.set_page_config(
    page_title="GPT Lab",
    page_icon="https://api.dicebear.com/5.x/bottts-neutral/svg?seed=gptLAb"#,
    #menu_items={"About": "GPT Lab is a user-friendly app that allows anyone to interact with and create their own AI Assistants powered by OpenAI's GPT-3 language model. Our goal is to make AI accessible and easy to use for everyone, so you can focus on designing your Assistant without worrying about the underlying infrastructure.", "Get help": None, "Report a Bug": None}
)



# copies 
home_title = "GPT Lab"
home_introduction = "Welcome to GPT Lab, where the power of OpenAI's GPT technology is at your fingertips. Socialize with pre-trained AI Assistants in the Lounge or create your own custom AI companions in the Lab. Whether you need a personal helper, writing partner, or more, GPT Lab has you covered. Join now and start exploring the endless possibilities!"
home_privacy = "At GPT Lab, your privacy is our top priority. To protect your personal information, our system only uses the hashed value of your OpenAI API Key, ensuring complete privacy and anonymity. Your API key is only used to access AI functionality during each visit, and is not stored beyond that time. This means you can use GPT Lab with peace of mind, knowing that your data is always safe and secure."

st.markdown(
    "<style>#MainMenu{visibility:hidden;}</style>",
    unsafe_allow_html=True
)

#st.title(home_title)
st.markdown(f"""# {home_title} <span style=color:#2E9BF5><font size=5>Beta</font></span>""",unsafe_allow_html=True)

st.markdown("""\n""")
st.markdown("#### Greetings")
st.write(home_introduction)

#st.markdown("---")

st.markdown("#### Privacy")
st.write(home_privacy)

st.markdown("""\n""")
st.markdown("""\n""")

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