from dotenv import load_dotenv
from ai6_vectordb import retriever_tool
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage, SystemMessage, ToolMessage, HumanMessage
from langgraph.graph import add_messages, StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI

system_prompt = SystemMessage(content="""
You are an intelligent AI assistant who answers questions about Miyamoto Musashi and his 5 rings based on the directory loaded into your knowledge base.
Use the retriever_tool available to answer questions about Musashi's Life and the 5 rings. You can make multiple calls if needed.
If you need to look up some information before asking a follow up question, you are allowed to do that!
Please always cite the specific parts of the documents you use in your answers.
""")

load_dotenv()

# Toolkit
toolkit = [retriever_tool]
tools_dict = {tool.name: tool for tool in toolkit}

# LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash").bind_tools(toolkit)

# State Schema
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]


def should_continue(state: AgentState) -> AgentState:
    """Check if the last message contains tool calls"""
    x = state["messages"][-1]
    return hasattr(x, 'tool_calls') and len(x.tool_calls) > 0


def call_llm(state: AgentState) -> AgentState:
    """ Function to call the LLM with current state """
    messages = list(state['messages'])
    messages = [system_prompt] + messages
    message = llm.invoke(messages)
    return {"messages": [message]}

# Retriever Agent
def take_action(state: AgentState) -> AgentState:
    """Execute tool calls from the LLM's response."""

    tool_calls = state['messages'][-1].tool_calls
    results = []
    for t in tool_calls:
        print(f"Calling Tool: {t['name']} with query: {t['args'].get('query', 'No query provided')}")
        
        if not t['name'] in tools_dict: # Checks if a valid tool is present
            print(f"\nTool: {t['name']} does not exist.")
            result = "Incorrect Tool Name, Please Retry and Select tool from List of Available tools."
        
        else:
            result = tools_dict[t['name']].invoke(t['args'].get('query', ''))
            print(f"Result length: {len(str(result))}")
            

        # Appends the Tool Message
        results.append(ToolMessage(tool_call_id=t['id'], name=t['name'], content=str(result)))

    print("Tools Execution Complete. Back to the model!")
    return {'messages': results}


graph = StateGraph(AgentState)
graph.add_node("llm", call_llm)
graph.add_node("retriever_agent", take_action)

graph.add_conditional_edges(
    "llm",
    should_continue,
    {
        True: "retriever_agent", 
        False: END
    }
)
graph.add_edge("retriever_agent", "llm")
graph.set_entry_point("llm")

rag_agent = graph.compile()


def running_agent():
    print("\n=== RAG AGENT===")
    
    while True:
        user_input = input("\nWhat is your question: ")
        if user_input.lower() in ['exit', 'quit']:
            break
            
        messages = [HumanMessage(content=user_input)] # converts back to a HumanMessage type

        result = rag_agent.invoke({"messages": messages})
        
        print("\n=== ANSWER ===")
        print(result['messages'][-1].content)


running_agent()