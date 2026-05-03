from typing import TypedDict, Annotated, Sequence, Any
import operator
from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph, END
from .nodes import classifier_node, travel_plan_node, recommend_node, qa_node

# Define the state of the agent
class AgentState(TypedDict):
    # The list of messages in the conversation
    # Annotated with operator.add so that nodes can return a list 
    # of messages that will be appended to the existing state
    messages: Annotated[Sequence[BaseMessage], operator.add]
    # The classified intent of the user
    intent: str
    # Tools available to the agent for this turn
    tools: Sequence[Any]

def route_intent(state: AgentState):
    """
    Determines which node to route to based on the classified intent in the state.
    """
    intent = state.get("intent")
    if intent == "travel_plan":
        return "travel_plan"
    elif intent == "travel_recommend":
        return "travel_recommend"
    else:
        return "general_qa"

# Initialize the State Graph
workflow = StateGraph(AgentState)

# Add all the nodes we implemented
workflow.add_node("classifier", classifier_node)
workflow.add_node("travel_plan", travel_plan_node)
workflow.add_node("travel_recommend", recommend_node)
workflow.add_node("general_qa", qa_node)

# Set the starting point of the graph
workflow.set_entry_point("classifier")

# Define the conditional logic:
# After classification, go to the appropriate agent node
workflow.add_conditional_edges(
    "classifier",
    route_intent,
    {
        "travel_plan": "travel_plan",
        "travel_recommend": "travel_recommend",
        "general_qa": "general_qa"
    }
)

# Once an agent node has responded, the conversation flow ends for this turn
workflow.add_edge("travel_plan", END)
workflow.add_edge("travel_recommend", END)
workflow.add_edge("general_qa", END)

# Compile the graph into a runnable component
app_graph = workflow.compile()
