import os
from dotenv import load_dotenv
# Meu modelo llm (Gemini)
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
# Para criar minha propria ferramenta 
from langchain_core.tools import tool
# Para a API do OpenWeather
import requests
import json

load_dotenv()
api_key = os.getenv("API_KEY")
key_open_weather = os.getenv("KEY_API_WEATHER")

@tool
def get_weather(city: str) -> str:
    """Obter a previsão do tempo para uma cidade específica."""
    link = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={key_open_weather}&lang=pt_br"
    request = requests.get(link)
    result = request.json()
    if result.get("cod") != "200":
        return f"Não foi possível obter a previsão do tempo para {city}. Verifique o nome da cidade."
    data = result['list']
    temp = data[0]['main']['temp'] - 273.15  # Converter de Kelvin para Celsius
    description = data[0]['weather'][0]['description']
    return f"Em {city}, a temperatura é de {temp:.2f}°C e o clima está {description}."

llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", temperature=0.7, google_api_key=api_key)

agent = create_react_agent(llm, [get_weather])
human_input = "Qual a previsão do tempo para hoje a noite em Campo Mourão?"
response = agent.invoke({"messages": human_input})

print(f"Usuario: {human_input}")
print(f"Agente: {response["messages"][-1].content}")