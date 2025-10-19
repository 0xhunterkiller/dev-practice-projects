# Import Dependencies
from dotenv import load_dotenv
from typing import TypedDict, List
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

# Load Environment Variables
load_dotenv()

# Define Agent State Schema to be a list of Human Messages
class AgentState(TypedDict):
    messages: List[HumanMessage]

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

def process(state: AgentState) -> AgentState:
    response = llm.invoke(state['messages'])
    print(f"\nAI: {response.content}")
    print("="*20)
    return state

graph = StateGraph(AgentState)
graph.add_node("process", process)
graph.add_edge(START, "process")
graph.add_edge("process",END)

agent = graph.compile()

user_input = input("Enter: ")
while True:
    agent.invoke({"messages": [HumanMessage(content=user_input)]})
    user_input = input("Enter: ")
    if user_input.lower().strip() == "q":
        print("Goodbye")
        break
