# Import Dependencies
from dotenv import load_dotenv
from typing import TypedDict, Annotated
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver

# Load Environment Variables
load_dotenv()

# Setup the Memory Saver
memory = MemorySaver() # in-memory checkpointer (it saves the conversation history in memory)

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

def process(state: AgentState) -> AgentState:
    """"This node will solve the request you input"""
    response = llm.invoke(state['messages'])
    print(f"\nAI: {response.content}")
    print("="*20)
    return state

graph = StateGraph(AgentState)
graph.add_node("process", process)
graph.add_edge(START, "process")
graph.add_edge("process",END)

app = graph.compile(checkpointer=memory)

user_input = input("Enter: ")
while True:
    config = {
        "configurable": {"thread_id": input("Enter ThreadID: ")}
    }
    result = app.invoke({"messages": [HumanMessage(content=user_input)]}, config=config)
    user_input = input("Enter: ")
    if user_input.lower().strip() == "q":
        print("Goodbye")
        break

# Memory works in different threads, so that we can simulate multiple users talking,
# Each thread maintains its own set of memories, that is exclusive of other threads
# Think of it like different conversations in ChatGPT, where ChatGPT cannot access memories from a different conversation