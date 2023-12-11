import os
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import constants
import react
import time

os.environ["OPENAI_API_KEY"] = st.secrets["openaikey"]["apikey"]
# Page title
#st.set_page_config(page_title='EmailCreator')
#st.title('ProjectP0.1')

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
agree = st.checkbox('He leído y acepto los términos y condiciones de uso')
if agree:
    st.write('Perfecto!')
st.markdown("""\n""")
st.markdown("""\n""")

#GSheets connection
conn = st.connection("gsheets", type=GSheetsConnection)

# Text input
uso_nombre = st.checkbox('Usar nombre?')
if uso_nombre:
        nombrep = st.text_input(
                "Nombre y Apellidos",
                None,
                key="nombrep",
                placeholder="Ej: Cristóbal González Muñoz",
                label_visibility="visible")
else:
        nombrep = ""
        
uso_correo = st.checkbox('Usar correo?')
if uso_correo:
        correop = st.text_input(
                "Correo electrónico",
                None,
                key="correop",
                placeholder="Ej: miguel.soto@gmail.com",
                label_visibility="visible")
else:
        correop = ""

uso_direccion = st.checkbox('Usar Dirección domiciliaria?')
if uso_direccion:
        direccionp = st.text_input(
                "Dirección domiciliaria",
                None,
                key="direccionp",
                placeholder="Ej: Av. Colón 1234, Depto. 56, Talcahuano, Región del Biobío",
                label_visibility="visible")
else:
        direccionp = ""

uso_nacimiento = st.checkbox('Usar fecha de nacimiento?')
if uso_nacimiento:
        nacimientop = st.text_input(
                "Fecha de nacimiento",
                None,
                key="nacimientop",
                placeholder="Ej: 15 de agosto de 1995",
                label_visibility="visible")
else:
        nacimientop = ""

uso_telefono = st.checkbox('Usar numero de telefono?')
if uso_telefono:
        telefonop = st.text_input(
                "Número de teléfono",
                None,
                key="telefonop",
                placeholder="Ej: +56 9 8765 4321",
                label_visibility="visible")
else:
        telefonop = ""

uso_laboral = st.checkbox('Usar información laboral/ocupación?')
if uso_laboral:
        laboralp = st.text_input(
                "Experiencia laboral",
                None,
                key="laboralp",
                placeholder="Ej: Ingeniero civil industrial. 3 años trabajando en una empresa de consultoría en proyectos de optimización de procesos, gestión de calidad y mejora continua. He participado en diversos proyectos para clientes de distintos rubros, como minería, energía, salud y educación.",
                label_visibility="visible")
else:
        laboralp = ""

uso_interes = st.checkbox('Usar intereses?')
if uso_interes:
        interesp = st.text_input(
                "Intereses",
                None,
                key="interesp",
                placeholder="Ej: Me gusta leer libros de negocios, innovación y desarrollo personal. Disfruto de viajar, conocer nuevas culturas y aprender idiomas. Practico deportes como fútbol, tenis y natación.",
                label_visibility="visible")
else:
        interesp = ""

uso_extra = st.checkbox('Usar información extra?')
if uso_extra:
        extrap = st.text_input(
                "Datos Extra",
                None,
                key="extrap",
                placeholder="Ej: RUT, Redes sociales, etc",
                label_visibility="visible")
else:
        extrap = ""
# Form to accept user's text input for summarization
result = []
with st.form('colecting_form', clear_on_submit=True):

        submitted = st.form_submit_button('Submit')
        if submitted:
                if agree:
                        with st.spinner('Calculating...'):
                                time.sleep(1)
                                response = react.phishing_generator(nombrep,correop,direccionp,nacimientop,telefonop,laboralp,interesp,extrap)
                                result.append(response)
                else:
                        with st.spinner('Calculating...'):
                                time.sleep(1)
                                response="Debes aceptar los términos y condiciones!"
                                result.append(response)
                        
                       
if len(result):
        st.info(response)
        with st.form(key="datos_form"):
                ej1=st.slider("EJEMPLO1",0,50,5)
                ej2=st.slider("EJEMPLO2",0,50,5)
                ej3=st.slider("EJEMPLO3",0,50,5)
                ej4=st.slider("EJEMPLO4",0,50,5)
                ej5=st.slider("EJEMPLO5",0,50,5)
                ej6=st.slider("EJEMPLO6",0,50,5)

                st.markdown("**required*")

                submit_button = st.form_submit_button(label="Submit ejemplos")

                if submit_button:
                        st.write("GRACIAS")
