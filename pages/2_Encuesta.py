import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import PhishingLab as pl
#GSheets connection
conn = st.connection("gsheets", type=GSheetsConnection)
survey = "Responder la encuesta una vez generado el correo de prueba..."

existing_data = conn.read(worksheet="datos", usecols=list(range(6)),ttl=5)
existing_data = existing_data.dropna(how="all")
st.markdown("#### Encuesta")
st.write(survey)
#listo = st.checkbox('listo')
listo = pl.estado_escuesta()
if listo:    
        with st.form("datos_form"):
                ej1 = st.slider('Sensación de Autoridad:', 0, 5, 1)
                ej2 = st.slider('Sensación de Urgencia:', 0, 5, 1)
                ej3 = st.slider('Sensación de Deseo: ', 0, 5, 1)
                ej4 = st.slider('¿Que tan probable es que creyeras el contenido del correo?', 0, 5, 1)
                ej5 = st.slider('¿Piensas que esto podría ser peligroso en un futuro?', 0, 5, 1)
                        
                submit_button = st.form_submit_button(label="Enviar")
                        
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
                                        }
                                ]
                                )
                        updated_df = pd.concat([existing_data,ejemplo_data], ignore_index=True)
                        #actualizar googlesheets
                        conn.update(worksheet="datos", data=updated_df)
                        st.success("Gracias!!")
