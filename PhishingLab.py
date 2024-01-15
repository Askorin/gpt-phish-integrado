import os
import openai
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import constants
import react
import time

os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
#openai.api_key = os.environ["OPENAI_API_KEY"]
# copies 
home_title = "PhishingLab"
home_introduction = "Hola, esta es una aplicación de generación de correos phishing que te muestra cómo pueden ser los correos fraudulentos que intentan engañarte para obtener tus datos personales, financieros o de acceso. Con esta aplicación, puedes ver ejemplos de correos phishing que simulan ser de entidades legítimas, como bancos, empresas, organismos públicos, etc. Solo tienes que introducir los datos que creas que filtras con mayor facilidad y la aplicación te mostrará un correo falso que podrías recibir en tu bandeja de entrada. Esta aplicación utiliza la tecnología GPT de OpenAI para crear correos phishing convincentes y peligrosos. Úsala y aprende a identificar y evitar los correos phishing."
home_privacy = "Tu información personal no es almacenada de ningún tipo, apenas generas un correo todo se elimina, asegurando una completa privacidad y anonimato. Esto significa que puedes usar PhishingLab con tranquilidad, sabiendo que tus datos siempre están seguros y protegidos."
home_getstarted = "Revise y acepte nuestros Términos de uso y Política de privacidad, disponibles en nuestra página de Términos. Al marcar la casilla, confirma que ha leído y aceptado nuestras políticas. ¡Empecemos!"
instrucciones1 = "1-Primero debes marcar qué datos son los más probables que filtres con facilidad en internet."
instrucciones2 = "2-Una vez marcada las casillas deberás rellenar con los datos de la forma que se muestra en los ejemplos."
instrucciones3 = "3-Ya con todos los datos listos presiona el botón de generar correo y espera a que se muestre en pantalla."
instrucciones4 = "4-Una vez generado el correo verifica que se genero correctamente, hay ocasiones en las que puede que no se genere el correo de manera correcta, en caso de que no se genere como es deseado vuelve a presionar el botón de generar correo o intenta usar más datos, hay veces que los datos entregados son muy pocos y no se puede generar un correo consistente. "
instrucciones5 = "5-Ya con el correo generado de manera correcta marca la casilla de “Correo generado correctamente”, de esta forma se desplegará una ventana con una encuesta para evaluar el contenido del correo y la sensación generada."
instrucciones6 = "6- Rellena la encuesta marcando las casillas según lo indicado y presiona el botón de enviar."
instrucciones7 = "7- Una vez ya enviada la encuesta se almacenarán los datos para su estudio, muchas gracias por participar."
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
agree = st.checkbox('He leído y acepto las Politicas de Privacidad')
if agree:
    st.write('Perfecto!')
st.markdown("""\n""")
st.markdown("""\n""")

#GSheets connection
conn = st.connection("gsheets", type=GSheetsConnection)
existing_data = conn.read(worksheet="datos", usecols=list(range(13)),ttl=13)
existing_data = existing_data.dropna(how="all")

st.markdown("#### Instrucciones de uso")
st.write(instrucciones1)
st.markdown("""\n""")
st.write(instrucciones2)
st.markdown("""\n""")
st.write(instrucciones3)
st.markdown("""\n""")
st.write(instrucciones4)
st.markdown("""\n""")
st.write(instrucciones5)
st.markdown("""\n""")
st.write(instrucciones6)
st.markdown("""\n""")
st.write(instrucciones7)
st.markdown("""\n""")

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

uso_familia = st.checkbox('Usar información familiar?')
if uso_familia:
        familiap = st.text_input(
                "Datos Familiares",
                None,
                key="familp",
                placeholder="Ej: Vivo con mi esposa y 2 hijos...",
                label_visibility="visible")
else:
        familiap = ""
        
# Form to accept user's text input for summarization
result = []
correof = st.form('colecting_form')
submitted = correof.form_submit_button('Generar correo')
if submitted:
        if agree:
                with st.spinner('Calculating...'):
                        time.sleep(1)
                        response = react.phishing_generator(nombrep,correop,direccionp,nacimientop,telefonop,laboralp,interesp,familiap)
                        result.append(response)
                        correof.info(response)
        else:
                with st.spinner('Calculating...'):
                        time.sleep(1)
                        response="Debes aceptar los términos y condiciones!"
                        result.append(response)
                        correof.info(response)
                        

                  

        




encuesta_lista = st.checkbox('Correo generado correctamente')
if encuesta_lista:
        st.write('ola')
        encuestaf = st.form("datos_form")
        ej1 = encuestaf.slider('Sensación de Autoridad:', 0, 5, 1)
        ej2 = encuestaf.slider('Sensación de Urgencia:', 0, 5, 1)
        ej3 = encuestaf.slider('Sensación de Deseo: ', 0, 5, 1)
        ej4 = encuestaf.slider('¿Que tan probable es que creyeras el contenido del correo?', 0, 5, 1)
        ej5 = encuestaf.slider('¿Piensas que esto podría ser peligroso en un futuro?', 0, 5, 1)
        ej6 = encuestaf.checkbox('Uso nombre?')
        ej7 = encuestaf.checkbox('Uso correo?')
        ej8 = encuestaf.checkbox('Uso direccion?')
        ej9 = encuestaf.checkbox('Uso Fecha de Nacimiento?')
        ej10 = encuestaf.checkbox('Uso numero de telefono?')
        ej11 = encuestaf.checkbox('Uso info laboral?')
        ej12 = encuestaf.checkbox('Uso intereses?')
        ej13 = encuestaf.checkbox('Uso info familiar?')
        
        submit_button = encuestaf.form_submit_button(label="Enviar") 
                        
        if submit_button:
                #crear fila
                ejemplo_data = pd.DataFrame(
                        [
                                {
                                "Autoridad": ej1,
                                "Urgencia": ej2,
                                "Deseo": ej3,
                                "CreerCorreo": ej4,
                                "PeligroFuturo": ej5,
                                "Nombre": ej6,
                                "Correo": ej7,
                                "Direccion": ej8,
                                "FechaNacimiento": ej9,
                                "NumeroTelefono": ej10,
                                "Laboral": ej11,
                                "Intereses": ej12,
                                "Familiar": ej13,       
                                }
                        ]
                        )
                updated_df = pd.concat([existing_data,ejemplo_data], ignore_index=True)
                #actualizar googlesheets
                conn.update(worksheet="datos", data=updated_df)
                encuestaf.success("Gracias!!", icon="✅")
        

        