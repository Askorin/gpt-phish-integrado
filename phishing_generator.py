from enum import Enum
from pathlib import Path
import toml
from openai import ChatCompletion
from langchain import PromptTemplate
import hashlib
import tiktoken


root_dir = Path(__file__).resolve().parent

class Prompts(Enum):
    REACT_A = root_dir / "prompts" / "prompt_ReAct_A.toml"
    REACT_R = root_dir / "prompts" / "prompt_ReAct_R.toml"
    DIRECTO = root_dir / "prompts" / "prompt_directo.toml"
        
    def get_prompt_content(self):
        with open(self.value, "r") as prompt_file:
            return toml.load(prompt_file)


class Models(Enum):
    GPT3 = "gpt-3.5-turbo"
    GPT4 = "gpt-4"


class PhishingGenerator:
    def __init__(self, prompt):
        # Funciona por ahora
        # TODO(Askorin): Hacer que esto no sea asqueroso
        if isinstance(prompt, Prompts):
            self.prompt_content = prompt.get_prompt_content()
        elif isinstance(prompt, dict):
            self.prompt_content = prompt

    def __classic_generate(self, input: dict, model: Models, temperature: float = 0.5) -> dict:
        messages = self.prompt_content["mensajes"]

        messages.append({"role": "user", "content": digest_input(input)})

        response = ChatCompletion.create(
            model=model.value, temperature=temperature, messages=messages
        )

        return package(self.prompt_content, response, temperature, input)


    def __langchain_generate(self, input: dict, model: Models, temperature: float = 0.5) -> dict:
        # Aquí va código de Rodrigo
        prompt_template = PromptTemplate.from_template(self.prompt_content["template"])

        llm = OpenAI(model_name = model.value, temprature = temperature)

        # TODO: Seguir integrando aquí.
        return dict() 


    def generate(self, input: dict, model: Models, temperature: float = 0.5) -> dict:
        if (self.prompt_content["has_langchain_template"]):
            return self.__langchain_generate(input, model, temperature)
        else:
            return self.__classic_generate(input, model, temperature)
            


def digest_input(input: dict) -> str:
    """
    Converts data in the form of a dictionary into a string.

    Parameters:
    - input: The data to "digest".

    Returns:
    - str: The data, but in string format (keys and values included)
    """

    input_string = ""
    for llave, valor in input.items():
        input_string += llave + ": " + valor + "\n"
    return input_string


def package(prompt_dict: dict, response, temperature: float, input: dict) -> dict:
    """
    Packages gpt's output and the data used to generate it into a dictionary

    Parameters:
    - prompts: The prompts used.
    - response: GPT's response as is.
    - technique: Prompting technique used to generate the output.
    - temperature: Temperature used for the model.
    - input: The data that was fed into the model.

    Returns:
    - dict: A dictionary which contains input data and corresponding output, along with relevant
    metadata.
    """

    response_dict = {
        "id": "",
        "msg": [
            {
                "mensaje": "",
                "prompt": "",
                "set": [
                    "autoridad",
                    "urgencia",
                    "miedo",
                    "escasez",
                    "familiaridad",
                    "confianza",
                    "consenso",
                ],
                "llm": ["name", "temperature"],
                "tecnica": "",
                "idVictima": "",
                "totalTokens": 0,
                "observacion": "",
            }
        ],
        "tratamiento": [{}],
    }

    # Datos relacionados a la "victima".
    response_dict["msg"][0]["idVictima"] = input["correo"]
    response_dict["id"] = hashlib.md5(input["correo"].encode("utf-8")).hexdigest()

    # Datos de prompts / response.
    for msg in prompt_dict["mensajes"]:
        response_dict["msg"][0]["prompt"] += f"{msg['role']}: {msg['content']}\n"
    response_dict["msg"][0]["mensaje"] = response["choices"][0]["message"]["content"]

    # Datos del modelo.
    response_dict["msg"][0]["llm"][0] = response["model"]
    response_dict["msg"][0]["llm"][1] = temperature
    response_dict["msg"][0]["totalTokens"] = response["usage"]["total_tokens"]

    # Datos meta, técnica, etc... No relacionados al modelo, necesariamente.
    response_dict["msg"][0]["tecnica"] = prompt_dict["tecnica"]

    return response_dict


def get_token_count(model: str, text: str) -> int:
    """
    Returns the token count of a given string.

    Parameters:
    - model: The name or identifier of the gpt model to use.
    - text: String to analyze.

    Returns:
    - int: The token count of the analyzed text.
    """

    # TODO(Askorin): Using optional parameters should consume extra tokens, this is not yet
    # accounted for. Therefore, this will serve as an approximation.
    encoding = tiktoken.encoding_for_model(model)
    tokens = encoding.encode(text)
    return len(tokens)


def is_valid(model: str, messages: list[dict]) -> bool:
    """
    Identifies if the given message query is within the context window of a model.

    Parameters:
    - model: The name or identifier of the gpt model to use.
    - messages: List of messages that will be sent through the API to the model.

    Returns:
    - bool: True if total token count is below a certain threshold, false if it's above it.
    """
    context_windows = {Models.GPT3.value: 4096, Models.GPT4.value: 8192}

    num_tokens = 0

    for message in messages:
        num_tokens += get_token_count(model, message["content"])

    print(f"Number of input tokens: {num_tokens}")

    # TODO(Askorin): This limit should be adjustable in the future, for now we just assuming the worst case for output, which is that chatgpt's output turns out to be just as long as the input.

    return num_tokens < context_windows[model] / 2
