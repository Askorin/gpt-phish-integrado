import os
import openai
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import streamlit as st
from streamlit_gsheets import GSheetsConnection
from streamlit_js_eval import streamlit_js_eval
import pandas as pd
import constants
import react
import biografia
import time

os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
#openai.api_key = os.environ["OPENAI_API_KEY"]
# copies 
home_title = "PhishingLab"
home_introduction = "Hola, esta es una aplicación de generación de correos phishing que te muestra cómo pueden ser los correos fraudulentos que intentan engañarte para obtener tus datos personales, financieros o de acceso. Con esta aplicación, puedes ver ejemplos de correos phishing que simulan ser de entidades legítimas, como bancos, empresas, organismos públicos, etc. **Solo tienes que introducir los datos que creas que filtras con mayor facilidad** y la aplicación te mostrará un correo falso que podrías recibir en tu bandeja de entrada. Esta aplicación utiliza la tecnología GPT de OpenAI para crear correos phishing convincentes y peligrosos. Úsala y aprende a identificar y evitar los correos phishing."
home_privacy = "Tu información personal no es almacenada de ninguna forma, apenas generas un correo todo se elimina, asegurando una completa privacidad y anonimato. Esto significa que puedes usar PhishingLab con tranquilidad, sabiendo que tus datos siempre están seguros y protegidos."
home_getstarted = "Revise y acepte nuestros Términos de uso y Política de privacidad, disponibles en nuestra página de Términos. Al marcar la casilla, confirma que ha leído y aceptado nuestras políticas. ¡Empecemos!"
instrucciones1 = "1-Primero debes marcar qué datos son los más probables que filtres con facilidad en internet."
instrucciones2 = "2-Una vez marcada las casillas deberás rellenar con los datos de la forma que se muestra en los ejemplos."
instrucciones3 = "3-Ya con todos los datos listos presiona el botón de generar correo y espera a que se muestre en pantalla."
instrucciones4 = "4-Una vez generado el correo verifica que se generó correctamente, hay ocasiones en las que puede que no se genere el correo de manera correcta, en caso de que no se genere como es deseado vuelve a presionar el botón de generar correo o intenta usar más datos, hay veces que los datos entregados son muy pocos y no se puede generar un correo consistente. "
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
existing_data = conn.read(worksheet="datos", usecols=list(range(19)),ttl=19)
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

if 'correo_generado1' not in st.session_state:
        st.session_state['correo_generado1'] = 'Correo 1 sin generar'

if 'correo_generado2' not in st.session_state:
        st.session_state['correo_generado2'] = 'Correo 2 sin generar'

if 'trait1' not in st.session_state:
        st.session_state['trait1'] = 'Trait1 sin generar'

if 'trait2' not in st.session_state:
        st.session_state['trait2'] = 'Trait2 sin generar'

# Text input
uso_nombre = st.checkbox('¿Utilizar el nombre?')
if uso_nombre:
        nombrep = st.text_input(
                "Nombre y Apellidos",
                None,
                key="nombrep",
                placeholder="Ej: Cristóbal González Muñoz",
                label_visibility="visible")
else:
        nombrep = ""
        
uso_correo = st.checkbox('¿Utilizar el correo electrónico?')
if uso_correo:
        correop = st.text_input(
                "Correo electrónico",
                None,
                key="correop",
                placeholder="Ej: miguel.soto@gmail.com",
                label_visibility="visible")
else:
        correop = ""

uso_direccion = st.checkbox('¿Utilizar la dirección domiciliaria?')
if uso_direccion:
        direccionp = st.text_input(
                "Dirección domiciliaria",
                None,
                key="direccionp",
                placeholder="Ej: Av. Colón 1234, Depto. 56, Talcahuano, Región del Biobío",
                label_visibility="visible")
else:
        direccionp = ""

uso_nacimiento = st.checkbox('¿Utilizar la fecha de nacimiento?')
if uso_nacimiento:
        nacimientop = st.text_input(
                "Fecha de nacimiento",
                None,
                key="nacimientop",
                placeholder="Ej: 15 de agosto de 1995",
                label_visibility="visible")
else:
        nacimientop = ""

uso_telefono = st.checkbox('¿Utilizar el número de teléfono?')
if uso_telefono:
        telefonop = st.text_input(
                "Número de teléfono",
                None,
                key="telefonop",
                placeholder="Ej: +56 9 8765 4321",
                label_visibility="visible")
else:
        telefonop = ""

uso_laboral = st.checkbox('¿Utilizar la información laboral/ocupacional?')
if uso_laboral:
        laboralp = st.text_input(
                "Experiencia laboral",
                None,
                key="laboralp",
                placeholder="Ej: Ingeniero civil industrial. 3 años trabajando en una empresa de consultoría en proyectos de optimización de procesos, gestión de calidad y mejora continua. He participado en diversos proyectos para clientes de distintos rubros, como minería, energía, salud y educación.",
                label_visibility="visible")
else:
        laboralp = ""

uso_interes = st.checkbox('¿Utilizar intereses?')
if uso_interes:
        interesp = st.text_input(
                "Intereses",
                None,
                key="interesp",
                placeholder="Ej: Me gusta leer libros de negocios, innovación y desarrollo personal. Disfruto de viajar, conocer nuevas culturas y aprender idiomas. Practico deportes como fútbol, tenis y natación.",
                label_visibility="visible")
else:
        interesp = ""

uso_familia = st.checkbox('¿Utilizar información familiar?')
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
correof = st.form('colecting_form')
submitted = correof.form_submit_button('Generar correo')
if submitted:
        if agree:
                with st.spinner('La generación del correo puede tardar de 40 segundos a 2 minutos, por favor espera...'):
                        time.sleep(1)
                        #response1 = react.phishing_react(nombrep,correop,direccionp,nacimientop,telefonop,laboralp,interesp,familiap)
                        #response2 = biografia.phishing_biografia(nombrep,correop,direccionp,nacimientop,telefonop,laboralp,interesp,familiap)
                        #st.session_state['correo_generado1'] = response1[0]
                        #st.session_state['correo_generado2'] = response2[0]
                        #st.session_state['trait1'] = response1[1]
                        #st.session_state['trait2'] = response2[1]

                        response1 = react.phishing_react(nombrep,correop,direccionp,nacimientop,telefonop,laboralp,interesp,familiap)
                        response2 = biografia.phishing_biografia(nombrep,correop,direccionp,nacimientop,telefonop,laboralp,interesp,familiap)
                        st.session_state['correo_generado1'] = response1[0]
                        st.session_state['correo_generado2'] = response2[0]
                        st.session_state['trait1'] = response1[1]
                        st.session_state['trait2'] = response2[1]
                        correof.info("METODO 1:")
                        correof.info(response1[0])
                        correof.info("METODO 2:")
                        correof.info(response2[0])
        else:
                with st.spinner('La generación del correo puede tardar de 40 segundos a 2 minutos, por favor espera...'):
                        time.sleep(1)
                        response="Debes aceptar los términos y condiciones!"
                        correof.info(response)
                        

                  

        




encuesta_lista = st.checkbox('Correo generado correctamente')
if encuesta_lista :
        if st.session_state['correo_generado1'] != 'Correo 1 sin generar' and st.session_state['correo_generado2'] != 'Correo  sin generar':
                #Explicar autoridad, urgencia y deseo, explicar la escal;a del 1 al 5.
                st.write('Esta es una encuesta para estudiar el correo generado, a continuación se mostrarán una serie de preguntas junto a unas barras con el valor del 0 al 4, utiliza las barras para responder las preguntas según se indique (0-nada, 1-poco, 2-neutral, 3-bastante, 4-mucho):')
                encuestaf = st.form("datos_form")
                correo_correcto1 = st.session_state['correo_generado1']
                correo_correcto2 = st.session_state['correo_generado2']
                correof.info("METODO 1:")
                encuestaf.info(correo_correcto1)
                correof.info("METODO 2:")
                encuestaf.info(correo_correcto2)
                
                
                #CONTENIDO ENCUESTA
                
                #DATOS USADOS
                ej6 = uso_nombre
                ej7 = uso_correo
                ej8 = uso_direccion
                ej9 = uso_nacimiento
                ej10 = uso_telefono
                ej11 = uso_laboral
                ej12 = uso_interes
                ej13 = uso_familia
                
                #TRAITS USADOS SEGUN MODELO
                ej14 = st.session_state['trait1']
                ej19 = st.session_state['trait2']
                
                #PREGUNTAS CORREO 1
                ej1 = encuestaf.slider('¿Cuál fue la sensación de autoridad que te causó el correo generado con el **Metodo 1**? (Se utiliza alguna figura de autoridad)', 0, 4, 1)
                ej2 = encuestaf.slider('¿Cuál fue la sensación de urgencia que te causó el correo generado con el **Metodo 1**? (Se presiona a tomar una acción de forma urgente)', 0, 4, 1)
                ej3 = encuestaf.slider('¿Cuál fue la sensación de deseo que te causó el correo generado con el **Metodo 1**? (La atracción hacia un producto o servicio específico)', 0, 4, 1)
                ej4 = encuestaf.slider('¿Qué tan probable es que creyeras el contenido del correo del **Metodo 1**?', 0, 4, 1)
                #PREGUNTA ABIERTA(falla tecnica,calidad del correo-complementar respuesta)
                
                ej20 = st.text_input(
                "En relación a tu respuesta de la pregunta anterior. Explica por qué elegiste ese resultado para el contenido del correo del **Metodo 1**.",
                None,
                key="ej20",
                placeholder="Explica en este recuadro.",
                label_visibility="visible")
                
                ej6 = uso_nombre
                ej7 = uso_correo
                ej8 = uso_direccion
                ej9 = uso_nacimiento
                ej10 = uso_telefono
                ej11 = uso_laboral
                ej12 = uso_interes
                ej13 = uso_familia
                
                ej15 = encuestaf.slider('¿Cuál fue la sensación de autoridad que te causó el correo generado con el **Metodo 2**? (Se utiliza alguna figura de autoridad)', 0, 4, 1)
                ej16 = encuestaf.slider('¿Cuál fue la sensación de urgencia que te causó el correo generado con el **Metodo 2**? (Se presiona a tomar una acción de forma urgente)', 0, 4, 1)
                ej17 = encuestaf.slider('¿Cuál fue la sensación de deseo que te causó el correo generado con el **Metodo 2**? (La atracción hacia un producto o servicio específico)', 0, 4, 1)
                ej18 = encuestaf.slider('¿Qué tan probable es que creyeras el contenido del correo del **Metodo 2**?', 0, 4, 1)
                #PREGUNTA ABIERTA(falla tecnica,calidad del correo-complementar respuesta)
                
                ej21 = st.text_input(
                "En relación a tu respuesta de la pregunta anterior. Explica por qué elegiste ese resultado para el contenido del correo del **Metodo 2**.",
                None,
                key="ej21",
                placeholder="Explica en este recuadro.",
                label_visibility="visible")
                
                ej5 = encuestaf.slider('¿Piensas que esto podría ser más peligroso que el phishing tradicional?', 0, 4, 1)
                #PREGUNTA ABIERTA(por que??)
                
                ej22 = st.text_input(
                "En relación a tu respuesta de la pregunta anterior. Explica por qué elegiste ese resultado.",
                None,
                key="ej22",
                placeholder="Explica en este recuadro.",
                label_visibility="visible")
                
                
                
                
                submit_button = encuestaf.form_submit_button(label="Enviar") 
                                
                if submit_button:
                        #crear fila
                        ejemplo_data = pd.DataFrame(
                                [
                                        {
                                        "Autoridad1": ej1,
                                        "Urgencia1": ej2,
                                        "Deseo1": ej3,
                                        "CreerCorreo1": ej4,
                                        "PeligroFuturo": ej5,
                                        "Nombre": ej6,
                                        "Correo": ej7,
                                        "Direccion": ej8,
                                        "FechaNacimiento": ej9,
                                        "NumeroTelefono": ej10,
                                        "Laboral": ej11,
                                        "Intereses": ej12,
                                        "Familiar": ej13,
                                        "RasgoDefinido1": ej14,
                                        "Autoridad2": ej15,
                                        "Urgencia2": ej16,
                                        "Deseo2": ej17,
                                        "RasgoDefinido2": ej19,
                                        "CreerCorreo2": ej18,        
                                        }
                                ]
                                )
                        updated_df = pd.concat([existing_data,ejemplo_data], ignore_index=True)
                        #actualizar googlesheets
                        conn.update(worksheet="datos", data=updated_df)
                        encuestaf.success("Gracias!!", icon="✅")
                        time.sleep(3)
                        streamlit_js_eval(js_expressions="parent.window.location.reload()")
        
        else: 
                st.write('¡Primero debes generar un correo!')
                