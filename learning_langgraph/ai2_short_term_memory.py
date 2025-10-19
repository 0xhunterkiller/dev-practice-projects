# Import Dependencies
from dotenv import load_dotenv
from typing import TypedDict, List, Union
from langchain_core.messages import HumanMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

# Load Environment Variables
load_dotenv()

class AgentState(TypedDict):
    messages: List[Union[HumanMessage, AIMessage]]

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

def process(state: AgentState) -> AgentState:
    """"This node will solve the request you input"""
    response = llm.invoke(state['messages'])
    state["messages"].append(AIMessage(content=response.content))
    print(f"\nAI: {response.content}")
    print("="*20)
    return state

graph = StateGraph(AgentState)
graph.add_node("process", process)
graph.add_edge(START, "process")
graph.add_edge("process",END)

app = graph.compile()

conversation_history = [] # the conversation history is saved as a simple list

user_input = input("Enter: ")
while True:
    conversation_history.append(HumanMessage(content=user_input))
    result = app.invoke({"messages": conversation_history})
    conversation_history = result["messages"]
    user_input = input("Enter: ")
    if user_input.lower().strip() == "q":
        print("Goodbye")
        break

# This bot has memory, but doesn't remember after the while loop is terminated, because, the state is lost