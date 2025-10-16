import streamlit as st
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool
import requests

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
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

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7, google_api_key=api_key)
agent = create_react_agent(llm, [get_weather])

st.title("ChatBot do Tempo 🌦️")

if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.text_input("Digite sua pergunta:")

if st.button("Enviar") and user_input:
    with st.spinner("Aguarde, gerando resposta..."):
        response = agent.invoke({"messages": user_input})
    st.session_state.history.append(("Você", user_input))
    st.session_state.history.append(("Agente", response["messages"][-1].content))

for sender, msg in st.session_state.history:
    st.markdown(f"**{sender}:** {msg}")