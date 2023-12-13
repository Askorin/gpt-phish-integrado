import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

#GSheets connection
conn = st.connection("gsheets", type=GSheetsConnection)

existing_data = conn.read(worksheet="datos",usecols=list(range(6),ttl=5))
existing_data = existing_data.dropna(how="all")
st.dataframe(existing_data)

with st.form(key="datos_form"):
        ej1=st.select_slider("EJEMPLO1",options=[1,2,3,4,5],value=(1,1))
        ej2=st.select_slider("EJEMPLO2",options=['1','2','3','4','5'],value=('1','1'))
        ej3=st.select_slider("EJEMPLO3",options=['1','2','3','4','5'],value=('1','1'))
        ej4=st.select_slider("EJEMPLO4",options=['1','2','3','4','5'],value=('1','1'))
        ej5=st.select_slider("EJEMPLO5",options=['1','2','3','4','5'],value=('1','1'))
        ej6=st.select_slider("EJEMPLO6",options=['1','2','3','4','5'],value=('1','1'))
        
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
