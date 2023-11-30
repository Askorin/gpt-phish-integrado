import os
from langchain.llms import OpenAI
from langchain import OpenAI, Wikipedia
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.agents.react.base import DocstoreExplorer
import constants
#Definir PromptTemplate
from langchain import PromptTemplate
os.environ["OPENAI_API_KEY"] = constants.APIKEY

def phishing_generator(nomb, corr, direcc, nacimi, telefo, labor, inter):
    #Filtrar datos segun importancia
    nombrep=nomb
    correop=corr
    direccionp=direcc
    nacimientop=nacimi
    telefonop=telefo
    laborp=labor
    interesp=inter
    prompt_template = PromptTemplate.from_template( """
        Sabiendo los siguientes principios de ingenieria social:
        Autoridad:[La autoridad es una técnica eficaz porque la mayoría de las personas responden a la autoridad con obediencia. El truco consiste en convencer al objetivo de que el atacante es alguien con 
        autoridad interna o externa. Algunos agresores reivindican su autoridad verbalmente, y otros asumen su autoridad vistiendo un disfraz o uniforme.]

        Urgencia:[La urgencia suele encajar con la escasez, porque la necesidad de actuar con rapidez aumenta a medida que la escasez indica un mayor riesgo de perderse algo. La urgencia se utiliza a menudo 
        como método para obtener una respuesta rápida de un objetivo antes de que tengas tiempo de considerarlo detenidamente. Un ejemplo es un atacante que utiliza una estafa de facturas a través de un correo
        electrónico comercial comprometido para convencerle de que pague una factura inmediatamente por el corte de un servicio o que sera denunciado a una agencia de cobros.]

        Intimidación:[La intimidación puede considerarse a veces un derivado del principio de autoridad. La intimidación utiliza la autoridad, la confianza o incluso la amenaza de daño para motivar a alguien
        a seguir órdenes o instrucciones. A menudo, la intimidación se centra en explotar la incertidumbre en una situación en la que no está definida una directiva clara de funcionamiento o respuesta.
        Un ejemplo es la ampliación de un correo electrónico anterior del director general y del documento de RR.HH. para incluir una declaración en la que se afirma que los empleados se enfrentarán a una 
        sanción si no rellenan el formulario con prontitud. La sanción podría consistir por ejemplo en la pérdida del viernes informal, la exclusión del martes de tacos, una reducción del salario o incluso el despido.] 

        Y teniendo en cuenta los siguientes datos personales:[Nombre del objetivo: {nombre},Correo electrónico: {correo},Dirección domiciliaria: {direccion},Fecha de nacimiento: {nacimiento},Número de teléfono: {telefono},Experiencia laboral: {laboral},Intereses: {interes}]
                                                
        Responde que principios de ingenieria social presentados anteriormente es o son mas probables de ser utilizados (COMO MAXIMO USA SOLO 2) sobre los datos personales?  Tambien entrega cual de estos datos son de mayor utilidad para la aplicacion de tal principio.
        Responde siguiendo el siguiente ejemplo estructurado de respuesta:
        SET: [Escribir aca que principios de ingenieria social presentados anteriormente es o son mas probables de ser utilizados sobre los datos personales]                                                                          
        DATOS: [Escribir aca cuales de estos datos son de mayor utilidad para la aplicacion de tales principios]
        EXPLICACION: [Explica por que seleccionaste tales datos]                                                                                   
        
    """
    )
    

    llm = OpenAI(model_name="gpt-3.5-turbo",temperature=0.1)
    response1 = llm(prompt_template.format(nombre=nombrep, correo=correop, direccion=direccionp, nacimiento=nacimientop, telefono=telefonop, laboral=laborp, interes=interesp))
    #print(response1)
    #EJEMPLO
    #AUTORIDAD seghun la respuesta de arriba
    #question = "Como es posible generar un correo que aplique el principio de ingenieria social de AUTORIDAD usando los datos Nombre:Miguel Ángel Soto, Correo electrónico:miguel.soto@gmail.com, Dirección domiciliaria: Av. Colón 1234, Depto. 56, Talcahuano, Región del Biobío,Experiencia laboral:3 años trabajando como ingeniero civil industrialen una empresa de consultoría en proyectos de optimización de procesos llamada BestConsultoresCCP. Ha participado en diversos proyectos para clientes de distintos rubros, como minería, energía, salud y educación."
    template1 = PromptTemplate.from_template("{responsep}. Como es posible crear los correos que apliquen estos principios de ingenieria social usando los datos personales entregados?")
    question = template1.format(responsep=response1)
    #print("QUESTION ACA:")
    #print(question)
    #Aplicar una grupo[(pregunta,[(pensamiento,observacion)])] a cada SET
    manual_react = f"""Question: Como es posible crear un correo que use autoridad sobre otra presona usando sus datos personales? 
    Thought: Necesito saber que es la Autoridad, como hacer sentir a una persona que soy su superior y que tengo autoridad sobre el.
    Observation: Hacerme pasar por figuras con autoridad dentro de su circulo, ya sea trabajo o familia.
    Thought: Necesito aplicar la idea de autoridad en un dialogo por correo haciendome pasar por alguna figura de autoridad cercana.
    Observation: Escribe de forma articulada y precisa demostrando experiencia y conocimiento segun el tema a tratar en base a los datos entregados haciendote pasar por un superir dentro del area de trabajo.
    Thought: Redactar un correo que pueda generar autoridad sobre una persona en base a los datos entregados.

    Question: Como es posible crear un correo que haga sentir urgencia a otra presona usando sus datos personales?
    Thought: Necesito saber que es la Urgencia y que cosas despiertan la urgencia en las personas.
    Observation: Una urgencia es una situación que requiere atención inmediata. Puede ser una necesidad apremiante o una situación que requiere atención sin demoras. Las urgencias pueden referirse a infinidad de circunstancias en las que se ponen en juego la salud, la vida o el patrimonio de las personas.
    Thought: Necesito aplicar la idea de urgencia a un mensaje por correo donde use los datos personales de la persona
    Observation: Para comunicar urgencia en un correo electrónico, se recomienda redactar una línea de asunto que sea capaz de impulsar al destinatario a abrir el correo electrónico, utilizar un lenguaje urgente
    que promueva lo que se encontrará en el cuerpo del email, trabajar con palabras clave como «Por tiempo limitado», «Solo por hoy», «Edición limitada». Establecer una fecha límite, ser específico del día exacto
    en el que terminará la oferta. En el cuerpo del correo electrónico, indicar de manera clara y sucinta el propósito del correo electrónico y lo que se está solicitando. Asegurarse de enfatizar la urgencia del asunto. 
    Proporcionar detalles específicos sobre lo que se necesita, por qué se necesita con urgencia y cualquier fecha límite o restricción de tiempo relevante. Usando los datos personales crear una situacion donde se haga sentir urgencia.
    Thought: Redactar un correo que pueda generar urgencia en base a los datos personales entregados.

    Question: Como es posible crear un correo que intimide a otra presona usando sus datos personales?
    Thought: Necesito saber que es la Intimidacion y como puedo lograr intimidar a otra persona.
    Observation: Causar o infundir miedo de forma voluntaria se conoce como intimidación. La intimidación es una forma de infundir miedo para lograr que las otras personas hagan lo que quieran.
    Thought: Necesito aplicar la idea de intimidacion a un mensaje por correo usando datos personales.
    Observation: Para logarar la intimidacion por correo se puede hacer de muchas maneras, como chantaje.  
    Thought: Debo saber que es el chantaje y como aplicarlo a un dialogo por correo usando datos personales.
    Observation: Un chantaje es una extorsión, es decir, la amenaza de generar algún mal si no se realiza una determinada acción. La particularidad del chantaje es el hecho de que se funda en evitar hacer mal a alguien a cambio de algo. Un ejemplo típico de estos correos es el de los estafadores que afirman haber conseguido acceso a tu cuenta de correo e incluso a tu ordenador. 
    Thought: Redactar un correo que pueda generar intimidación en base a los datos personales entregados.


    Question:{question} """

    response2 = llm(manual_react)
    #print("ReACT ACA")
    #print(response2)
    template2 = PromptTemplate.from_template("{response2p}. Usa la estructura anterior para generar el correo.")
    generador = template2.format(response2p=response2)
    respuesta_final = llm(generador)
    #print("CORREO ACA:")
    #print(respuesta_final)
    return respuesta_final