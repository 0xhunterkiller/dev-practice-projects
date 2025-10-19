# Import Dependencies
from dotenv import load_dotenv
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage, ToolMessage, SystemMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
import hashlib

# Load Environment Variables
load_dotenv()

# document content
document_content = ""

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages] # add_message makes sure the new data is appended and not replaced

@tool
def update_content(content: str) -> str:
    """
    Updates the document with the provided content.
    """
    global document_content
    document_content = content
    return f"Document has been successfully modified. Your changes were not saved."

@tool
def save_content(filename: str) -> str:
    """
    Saves the content of the current document and finishes the process

    Args:
        filename: Name for the text file
    """
    if not filename.endswith(".txt"):
        filename += ".txt"
    
    try:
        with open(filename, "w") as file:
            file.write(document_content)
        md5sum = hashlib.md5(open(filename, "rb").read()).hexdigest()
        return f"Document was successfully saved to '{filename}'. MD5SUM: {md5sum}"
    except Exception as e:
        return f"Error saving document: {str(e)}"

toolkit = [update_content, save_content]

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash").bind_tools(toolkit)

def agent(state: AgentState) -> AgentState:
    system_prompt = SystemMessage(content=f"""
    You are Drafter, a helpful writing assistant. You are going to help the user update and modify documents.

    - If the user wants to update or modify the content, use the 'update_content' tool with the complete updated content.
    - If the user wants to save and finish, you need to use the 'save' tool.
    - Make sure to always show the current document state after modifications.

    The current document content: {document_content}
    """)
    
    if not state["messages"]:
        user_input = input("What would you like to create? ")
        user_message = HumanMessage(content=user_input)
    else:
        user_input = input("\n What would you like to do with the document? ")
        user_message = HumanMessage(content=user_input)
    
    all_messages = [system_prompt] + list(state["messages"]) + [user_message]
    response = llm.invoke(all_messages)

    print(f"\n AI: {response.content}")
    if hasattr(response, "tool_calls") and response.tool_calls:
        print(f"   USING TOOLS: {[tc['name'] for tc in response.tool_calls]}")

    return {"messages": list(state["messages"]) + [user_message, response]}

def should_continue(state: AgentState) -> AgentState:
    """ Determine if we should continue or end the conversation """
    messages = state["messages"]
    
    print("===== CONTENT =====")
    print(document_content)
    print("===== CONTENT =====")

    if not messages:
        return "continue"

    for message in reversed(messages):
        if isinstance(message, ToolMessage) and "md5sum" in message.content.lower():
            return "end"
    
    return "continue"

graph = StateGraph(AgentState)

graph.add_node("agent", agent)
graph.add_node("tools", ToolNode(toolkit))
graph.set_entry_point("agent")
graph.add_edge("agent", "tools")
graph.add_conditional_edges(
    "tools",
    should_continue,
    {
        "continue": "agent",
        "end": END
    }
)

app = graph.compile()

def print_messages(messages):
    """ Function I made to print the messages in a more readable format """
    if not messages:
        return
    for message in messages[-3:]:
        if isinstance(message, ToolMessage):
            print(f"\n   TOOL RESULT: {message.content}")

def run_document_agent():
    print("\n ========== DRAFT STARTED ==========")
    state = {"messages": []}
    for step in app.stream(state, stream_mode="values"):
        if "messages" in step:
            print_messages(step["messages"])
    print("\n ========== DRAFT FINISHED ==========")

if __name__ == "__main__":
    run_document_agent()