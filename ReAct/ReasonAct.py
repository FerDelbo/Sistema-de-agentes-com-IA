# Pegar a chave da API
import os
from dotenv import load_dotenv
# Meu modelo llm (Gemini)
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
# Criação do ReAct
from langgraph.prebuilt import create_react_agent
from langchain_community.agent_toolkits.load_tools import load_tools

# Carregar a chave da API do arquivo .env
load_dotenv()
api_key = os.getenv("API_KEY")

# Configurar o modelo LLM (Gemini)
llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", temperature=0.7, google_api_key=api_key)
# Kit de ferramentas (ReAct)
tools = load_tools(["wikipedia"])
# Criar o agente ReAct
agent = create_react_agent(llm, tools)

# Requsição ao agente
response = agent.invoke({"messages":"Quem é o presidente do Brasil e qual a sua idade?"})
# Exibir a resposta
print(response["messages"][-1].content)