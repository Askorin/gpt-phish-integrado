import os
import streamlit as st
#from streamlit_gsheets import GSheetsConnection
from streamlit_js_eval import streamlit_js_eval
import pandas as pd
#import constants
#from react import phishing_react
import biografia
from phishing_generator import *
import time
import constants

os.environ["OPENAI_API_KEY"] = constants.APIKEY 
# copies 
home_title = "PhishingLab"
home_introduction = "Hola, esta es una aplicación de generación de correos phishing que te muestra cómo pueden ser los correos fraudulentos que intentan engañarte para obtener tus datos personales, financieros o de acceso. Con esta aplicación, puedes ver ejemplos de correos phishing que simulan ser de entidades legítimas, como bancos, empresas, organismos públicos, etc. **Solo tienes que introducir los datos que creas que filtras con mayor facilidad** y la aplicación te mostrará un correo falso que podrías recibir en tu bandeja de entrada. Esta aplicación utiliza la tecnología GPT de OpenAI para crear correos phishing convincentes. Úsala y aprende a identificar y evitar los correos phishing."
home_privacy = "Tu información personal no es almacenada de ninguna forma, apenas generas un correo todo se elimina, asegurando una completa privacidad y anonimato. Esto significa que puedes usar PhishingLab con tranquilidad, tus datos siempre están seguros."
home_getstarted = "Revise y acepte los Términos de uso y Política de privacidad, disponibles en la página de Términos. Al marcar la casilla, confirma que ha leído y aceptado las políticas. ¡Empecemos!"
instrucciones1 = "1-Primero debes marcar qué datos son los más probables que filtres con facilidad en internet."
instrucciones2 = "2-Una vez marcada las casillas deberás rellenar con los datos de la forma que se muestra en los ejemplos."
instrucciones3 = "3-Ya con todos los datos listos presiona el botón de generar los correo y espera a que se muestre en pantalla."
instrucciones4 = "4-Una vez generado los correos verifica que se generaron correctamente, **hay ocasiones en las que puede que no se generen de manera correcta, en caso de que no se genere como es deseado vuelve a presionar el botón de generar correos o intenta usar más datos**, hay veces que los datos entregados son muy pocos y no se puede generar un correo consistente. "
instrucciones5 = "5-Ya con los correos generados de manera correcta marca la casilla de “Correos generados correctamente”, de esta forma se desplegará una ventana con una encuesta para evaluar el contenido de los correos y la sensación generada."
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
#conn = st.connection("gsheets", type=GSheetsConnection)
#existing_data = conn.read(worksheet="datos", usecols=list(range(22)),ttl=22)
#existing_data = existing_data.dropna(how="all")

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
submitted = correof.form_submit_button('Generar correos')
if submitted:
        if agree:
                with st.spinner('La generación del correo puede tardar de 40 segundos a 2 minutos, por favor espera...'):
                        time.sleep(1)

                        datos_prelim = {
                                "Nombre": nombrep,
                                "Correo": correop,
                                "Direccion": direccionp,
                                "Fecha de Nacimiento": nacimientop,
                                "Teléfono": telefonop,
                                "Laboral": laboralp,
                                "Intereses": interesp,
                                "Familia": familiap
                        }
                        datos = dict()
                        # Tener llaves sin valor afecta el desempeño del modelo, por alguna razón.
                        for dato in datos_prelim:
                            if datos_prelim[dato] != "":
                                datos[dato] = datos_prelim[dato]


                        response1 = generate_phishing_react_R(datos, Models.GPT3)

                        # response2 = generate_phishing_react_A(datos, Models.GPT3)
                        # response2 = response2["msg"][0]["mensaje"].split("RESPUESTA:", 1)[1]

                        response3 = generate_phishing_bio(datos, Models.GPT3)

                        #response2 = biografia.phishing_biografia(nombrep,correop,direccionp,nacimientop,telefonop,laboralp,interesp,familiap)
                        st.session_state['correo_generado1'] = response1[0]
                        st.session_state['correo_generado2'] = response3[0]                        
                        st.session_state['trait1'] = response1[1]
                        st.session_state['trait2'] = response3[1] 

                        #response1 = react.phishing_react(nombrep,correop,direccionp,nacimientop,telefonop,laboralp,interesp,familiap)
                        #response2 = biografia.phishing_biografia(nombrep,correop,direccionp,nacimientop,telefonop,laboralp,interesp,familiap)
                        #st.session_state['correo_generado1'] = response1[0]
                        #st.session_state['correo_generado2'] = response2[0]
                        #st.session_state['trait1'] = response1[1]
                        #st.session_state['trait2'] = response2[1]
                        correof.info("METODO 1:")
                        correof.info(response1[0])
                        correof.info("METODO 2:")
                        correof.info(response3[0])
        else:
                with st.spinner('La generación del correo puede tardar de 40 segundos a 2 minutos, por favor espera...'):
                        time.sleep(1)
                        response="Debes aceptar los términos y condiciones!"
                        correof.info(response)
                        

                  

        




encuesta_lista = st.checkbox('Correos generados correctamente')
if encuesta_lista :
        if st.session_state['correo_generado1'] != 'Correo 1 sin generar' and st.session_state['correo_generado2'] != 'Correo  sin generar':
                #Explicar autoridad, urgencia y deseo, explicar la escal;a del 1 al 5.
                st.write('Esta es una encuesta para estudiar el correo generado, a continuación se mostrarán una serie de preguntas junto a unas barras con el valor del 0 al 4, **utiliza las barras para responder las preguntas según se indique (0-nada, 1-poco, 2-neutral, 3-bastante, 4-mucho)**:')
                encuestaf = st.form("datos_form")
                correo_correcto1 = st.session_state['correo_generado1']
                correo_correcto2 = st.session_state['correo_generado2']
                encuestaf.info("METODO 1:")
                encuestaf.info(correo_correcto1)
                encuestaf.info("METODO 2:")
                encuestaf.info(correo_correcto2)
                
                
                #CONTENIDO ENCUESTA
                
                #DATOS USADOS
                ej1 = uso_nombre
                ej2 = uso_correo
                ej3 = uso_direccion
                ej4 = uso_nacimiento
                ej5 = uso_telefono
                ej6 = uso_laboral
                ej7 = uso_interes
                ej8 = uso_familia
                
                #TRAITS USADOS SEGUN MODELO
                ej9 = st.session_state['trait1']
                ej10 = st.session_state['trait2']
                
                #PREGUNTAS CORREO 1
                ej11 = encuestaf.slider('¿Cuál fue la sensación de **autoridad** que te causó el correo generado con el **Metodo 1**? (Por ejemplo: Se utiliza alguna figura de autoridad como Jefe de algún área o entidades gubernamentales.)', 0, 4, 1)
                ej12 = encuestaf.slider('¿Cuál fue la sensación de **urgencia** que te causó el correo generado con el **Metodo 1**? (Por ejemplo: Se presiona a tomar una acción de forma urgente debido a una fecha límite o escasez de algo.)', 0, 4, 1)
                ej13 = encuestaf.slider('¿Cuál fue la sensación de **deseo** que te causó el correo generado con el **Metodo 1**? (Por ejemplo: La atracción hacia un producto o servicio específico que te beneficie.)', 0, 4, 1)
                ej14 = encuestaf.slider('¿Qué tan probable es que creyeras el contenido del correo del **Metodo 1**?', 0, 4, 1)
                #PREGUNTA ABIERTA(falla tecnica,calidad del correo-complementar respuesta)
                ej15 = encuestaf.text_input(
                "En relación a tu respuesta de la pregunta anterior. Explica por qué elegiste ese resultado para el contenido del correo del **Metodo 1**.",
                None,
                key="ej15",
                placeholder="Explica en este recuadro.",
                label_visibility="visible")
                
                
                #PREGUNTAS DE CORREO 2
                ej16 = encuestaf.slider('¿Cuál fue la sensación de **autoridad** que te causó el correo generado con el **Metodo 2**? (Por ejemplo: Se utiliza alguna figura de autoridad como Jefe de algún área o entidades gubernamentales.)', 0, 4, 1)
                ej17 = encuestaf.slider('¿Cuál fue la sensación de **urgencia** que te causó el correo generado con el **Metodo 2**? (Por ejemplo: Se presiona a tomar una acción de forma urgente debido a una fecha límite o escasez de algo.)', 0, 4, 1)
                ej18 = encuestaf.slider('¿Cuál fue la sensación de **deseo** que te causó el correo generado con el **Metodo 2**? (Por ejemplo: La atracción hacia un producto o servicio específico que te beneficie.)', 0, 4, 1)
                ej19 = encuestaf.slider('¿Qué tan probable es que creyeras el contenido del correo del **Metodo 2**?', 0, 4, 1)
                #PREGUNTA ABIERTA(falla tecnica,calidad del correo-complementar respuesta)
                
                ej20 = encuestaf.text_input(
                "En relación a tu respuesta de la pregunta anterior. Explica por qué elegiste ese resultado para el contenido del correo del **Metodo 2**.",
                None,
                key="ej20",
                placeholder="Explica en este recuadro.",
                label_visibility="visible")
                
                ej21 = encuestaf.slider('¿Piensas que esto podría ser más peligroso que el phishing tradicional?', 0, 4, 1)
                #PREGUNTA ABIERTA(por que??)
                
                ej22 = encuestaf.text_input(
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
                                        "Nombre": ej1,
                                        "Correo": ej2,
                                        "Direccion": ej3,
                                        "FechaNacimiento": ej4,
                                        "NumeroTelefono": ej5,
                                        "Laboral": ej6,
                                        "Intereses": ej7,
                                        "Familiar": ej8,
                                        "RasgoDefinido1": ej9,
                                        "RasgoDefinido2": ej10,
                                        "Autoridad1": ej11,
                                        "Urgencia1": ej12,
                                        "Deseo1": ej13,
                                        "CreerCorreo1": ej14,
                                        "ExplicaCreerCorreo1": ej15, 
                                        "Autoridad2": ej16,
                                        "Urgencia2": ej17,
                                        "Deseo2": ej18,
                                        "CreerCorreo2": ej19,
                                        "ExplicaCreerCorreo2": ej20,
                                        "PeligroFuturo": ej21, 
                                        "ExplicaPeligroFuturo": ej22,     
                                        }
                                ]
                                )
                        #updated_df = pd.concat([existing_data,ejemplo_data], ignore_index=True)
                        #actualizar googlesheets
                        #conn.update(worksheet="datos", data=updated_df)
                        encuestaf.success("Gracias!!", icon="✅")
                        time.sleep(3)
                        streamlit_js_eval(js_expressions="parent.window.location.reload()")
        
        else: 
                st.write('¡Primero debes generar un correo!')
                
