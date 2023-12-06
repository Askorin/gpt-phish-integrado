import os
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import streamlit as st
import constants
import react
import time

os.environ["OPENAI_API_KEY"] = constants.APIKEY

# Page title
#st.set_page_config(page_title='EmailCreator')
#st.title('ProjectP0.1')
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    constants.APIKEY=openai_api_key
    os.environ["OPENAI_API_KEY"] = constants.APIKEY


# copies 
home_title = "PhishingLab"
home_introduction = "Hola, esta es una aplicación de generación de correos phishing que te muestra cómo pueden ser los correos fraudulentos que intentan engañarte para obtener tus datos personales, financieros o de acceso. Con esta aplicación, puedes ver ejemplos de correos phishing que simulan ser de entidades legítimas, como bancos, empresas, organismos públicos, etc. Solo tienes que introducir los datos que creas que filtras con mayor facilidad y la aplicación te mostrará un correo falso que podrías recibir en tu bandeja de entrada. Esta aplicación utiliza la tecnología GPT de OpenAI para crear correos phishing convincentes y peligrosos. Úsala con precaución y aprende a identificar y evitar los correos phishing."
home_privacy = "En PhishingLab, tu privacidad es nuestra máxima prioridad. Tu información personal no es almacenada de ningún tipo, apenas generas un correo todo se elimina, asegurando una completa privacidad y anonimato. Esto significa que puedes usar GPT Lab con tranquilidad, sabiendo que tus datos siempre están seguros y protegidos."
home_getstarted = "¿Listo para explorar las infinitas posibilidades de la IA? Revise y acepte nuestros Términos de uso y Política de privacidad, disponibles en nuestra página de Términos. Al marcar la casilla, confirma que ha leído y aceptado nuestras políticas. ¡Empecemos!"
st.markdown(
    "<style>#MainMenu{visibility:hidden;}</style>",
    unsafe_allow_html=True
)

#st.title(home_title)
st.markdown(f"""# {home_title} <span style=color:#2E9BF5><font size=5>Beta</font></span>""",unsafe_allow_html=True)

st.markdown("""\n""")
st.markdown("#### Saludos")
st.write(home_introduction)

#st.markdown("---")

st.markdown("#### Privacidad")
st.write(home_privacy)

st.markdown("#### Comenzar")
st.write(home_getstarted)
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
extrap = st.text_input(
        "Datos Extra",
        None,
        key="interesp",
        placeholder="Ej: RUT, Redes sociales, etc",
        label_visibility="visible")

# Form to accept user's text input for summarization
result = []
with st.form('colecting_form', clear_on_submit=True):
    
    submitted = st.form_submit_button('Submit')
    if submitted:
        with st.spinner('Calculating...'):
            time.sleep(5)
            

            response = react.phishing_generator(nombrep,correop,direccionp,nacimientop,telefonop,laboralp,interesp,extrap)

            result.append(response)

if len(result):
    st.info(response)