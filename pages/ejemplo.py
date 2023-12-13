import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

#GSheets connection
conn = st.connection("gsheets", type=GSheetsConnection)

existing_data = conn.read(worksheet="datos", usecols=list(range(6)),ttl=5)
existing_data = existing_data.dropna(how="all")

with st.form(key="datos_form"):
        ej1 = st.slider('Sensación de Autoridad:', 0, 5, 1)
        ej2 = st.slider('Sensación de Urgencia:', 0, 5, 1)
        ej3 = st.slider('Sensación de Deseo: ', 0, 5, 1)
        ej4 = st.slider('¿Que tan probable es que creyeras el contenido del correo?', 0, 5, 1)
        ej5 = st.slider('¿Piensas que esto podría ser peligroso en un futuro?', 0, 5, 1)
        ej6 = st.slider('How old are you?', 0, 130, 25)
        
        submit_button = st.form_submit_button(label="Submit ejemplos")
        
        if submit_button:
            #validar
            if not ej1 or not ej2:
                st.warning("Rellena los datos")
            else:
                #crear fila
                ejemplo_data = pd.DataFrame(
                    [
                        {
                            "Ejemplo1": ej1,
                            "Ejemplo2": ej2,
                            "Ejemplo3": ej3,
                            "Ejemplo4": ej4,
                            "Ejemplo5": ej5,
                            "Ejemplo6": ej6,                    
                        }
                    ]
                )
                updated_df = pd.concat([existing_data,ejemplo_data], ignore_index=True)
                #actualizar googlesheets
                conn.update(worksheet="datos", data=updated_df)
                st.success("Gracias!!")
