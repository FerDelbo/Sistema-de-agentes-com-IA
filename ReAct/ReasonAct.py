# Pegar a chave da API
import os
from dotenv import load_dotenv
# Meu modelo llm (Gemini)
from langchain_google_genai import ChatGoogleGenerativeAI
# Criação do ReAct
from langgraph.prebuilt import create_react_agent
from langchain_community.agent_toolkits.load_tools import load_tools

load_dotenv()
api_key = os.getenv("API_KEY")

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=api_key)
tools = load_tools(["wikipedia"])

agent = create_react_agent(llm, tools)

response = agent.invoke({
    "message": [("human", "Quantas pessoas vivem no Brasil?")]
})

print(response.content)