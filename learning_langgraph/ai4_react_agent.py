# Import Dependencies
from dotenv import load_dotenv
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

# Load Environment Variables
load_dotenv()

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages] # add_message makes sure the new data is appended and not replaced

@tool
def add(a: int, b: int) -> int:
    """A function that takes as input 2 integers a and b, and returns the sum of the two integers"""
    return a+b

@tool
def subtract(a: int, b: int) -> int:
    """A function that takes as input 2 integers a and b, and returns the difference of the two integers"""
    return a-b

@tool
def multiply(a: int, b: int) -> int:
    """A function that takes as input 2 integers a and b, and returns the product of the two integers"""
    return a*b

toolkit = [add, subtract, multiply] # a list of tools

# so that the llm knows what tools are available
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash").bind_tools(toolkit) 

def chatbot(state: AgentState) -> AgentState:
    """"This node will generate the response for the query you input"""
    system_prompt = SystemMessage(content="You are my AI assistant, your name is Barry")
    response = llm.invoke([system_prompt] + state['messages'])
    return {"messages": [response]} # auto appended to the old list since we use add_messages

def should_continue(state: AgentState) -> AgentState:
    if not state["messages"][-1].tool_calls:
        return "end" # all tool calls have been completed
    else:
        return "continue" # tool calls are left, go into ToolNode

def print_stream(stream):
    for s in stream:
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()
    print("="*80)
    print()
    print("="*80)

graph = StateGraph(AgentState)
graph.add_node("tools", ToolNode(toolkit))
graph.add_node("chatbot", chatbot)
graph.add_edge(START, "chatbot")
graph.add_conditional_edges(
    "chatbot",
    should_continue,
    {
        "end": END,
        "continue": "tools"
    }
)
graph.add_edge("tools", "chatbot") # definite edge, the only way to get out of the tool node
app = graph.compile()

user_input = input("Enter: ")
while True:
    payload = {"messages": [HumanMessage(content=user_input)]}
    result = app.stream(payload, stream_mode="values")
    print_stream(result)
    user_input = input("Enter: ")
    if user_input.lower().strip() == "q":
        print("Goodbye")
        break

# Memory works in different threads, so that we can simulate multiple users talking,
# Each thread maintains its own set of memories, that is exclusive of other threads
# Think of it like different conversations in ChatGPT, where ChatGPT cannot access memories from a different conversation