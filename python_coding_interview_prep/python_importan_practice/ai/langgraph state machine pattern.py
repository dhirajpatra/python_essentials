from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    next_step: str

def planner(state: AgentState):
    # Determine next routing step
    return {"next_step": "executor"}

def executor(state: AgentState):
    # Execute pending tool calls
    return {"messages": ["Task executed."]}

builder = StateGraph(AgentState)
builder.add_node("planner", planner)
builder.add_node("executor", executor)
builder.set_entry_point("planner")
builder.add_edge("planner", "executor")
builder.add_edge("executor", END)
graph = builder.compile()