import os
import constants
from phishing_generator import Prompts

# import time

# Definir PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from phishing_generator import Models
from phishing_generator import digest_input

os.environ["OPENAI_API_KEY"] = constants.APIKEY


def phishing_react(input: dict, model: Models):
    # Filtrar datos segun importancia

    # 2-Autoridad 2-Urgencia 2-Deseo 2-Urgencia y Autoridad 2-Urgencia y Deseo 2-Autoridad y Deseo
    llm = ChatOpenAI(model=model.value, temperature=0.4)

    input_format = """
    Genera un correo de phishing con los siguientes datos:
    {input}
    """
    input_template = PromptTemplate.from_template(input_format)

    prompt_dict = Prompts.REACT_R.getPrompt()
    react = prompt_dict["mensajes"][0]["content"]
    react_template = PromptTemplate.from_template(react)

    final_prompt = prompt_dict["mensajes"][1]["content"]
    final_prompt_template = PromptTemplate.from_template(final_prompt)

    output_parser = StrOutputParser()

    chain = (
        input_template
        | react_template
        | llm
        | output_parser
        | final_prompt_template
        | llm
        | output_parser
    )


    input_string = digest_input(input)
    # final_response = chain.invoke({"input": input_string})
    final_response = chain.invoke({"input": input_string})

    trait_template = PromptTemplate.from_template(
        "Sabiendo los siguientes rasgos Autoridad: Los datos de la victima pueden ser usados para falsificar una figura de autoridad. Urgencia: Los datos de la victima pueden ser usados para generar una sensación de urgencia que la presione a tomar acción. Deseo: Los datos de la víctima pueden ser usados para generar una sensación de deseo por algo. Bajo que rasgo clasificarias el siguiente correo:\n{input}?\nSolo responde con el rasgo que creas, nada más."
    )
    trait_chain = trait_template | llm | output_parser
    traitFinal = trait_chain.invoke({"input": final_response})
    return [final_response, traitFinal]
