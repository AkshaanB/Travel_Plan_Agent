from langchain_core.messages import SystemMessage, HumanMessage
from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field
from langgraph.prebuilt import create_react_agent

# Initialize the LLM
llm = ChatOllama(model="llama3.2:3b", temperature=0)

class IntentResult(BaseModel):
    intent: str = Field(description="The classified intent: travel_plan, travel_recommend, or general_qa")

def classifier_node(state: dict):
    """
    Classifies the user's intent based on the last message.
    """
    messages = state.get("messages", [])
    if not messages:
        return {"intent": "general_qa"}
    
    last_msg = messages[-1].content
    
    system_prompt = (
        "You are an expert intent classifier for a travel agency. "
        "Your task is to categorize the user request into one of the following:\n"
        "1. travel_plan: Specific itineraries, booking flights, hotels, or detailed trip logistics.\n"
        "2. travel_recommend: General destination suggestions, 'where should I go' type questions.\n"
        "3. general_qa: Facts about places, travel tips, or general conversation.\n"
        "Return ONLY the category name."
    )

    # Use simple prompt for llama3.2 robustness
    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Classify this request: {last_msg}")
    ])
    
    intent_str = response.content.strip().lower()
    
    # Logic to normalize the string
    if "plan" in intent_str:
        intent = "travel_plan"
    elif "recommend" in intent_str:
        intent = "travel_recommend"
    else:
        intent = "general_qa"
        
    return {"intent": intent}

# Placeholder nodes for future implementation
def qa_node(state: dict):
    """
    Agent node for general travel questions.
    """
    messages = state.get("messages", [])
    
    system_prompt = (
        "You are a helpful and knowledgeable travel assistant. Your goal is to provide "
        "accurate, concise, and useful information about any travel-related questions.\n\n"
        "Guidelines:\n"
        "1. Answer questions about geography, culture, logistics, or general travel tips.\n"
        "2. If you don't know the answer, politely say so.\n"
        "3. Provide practical advice (e.g., visa requirements, currency, weather).\n"
        "4. Be professional and informative."
    )
    
    response = llm.invoke([
        SystemMessage(content=system_prompt)
    ] + messages)
    
    return {"messages": [response]}

async def recommend_node(state: dict):
    """
    Agent node for travel recommendations.
    """
    messages = state.get("messages", [])
    tools = state.get("tools", [])
    
    system_prompt = (
        "You are a passionate travel recommender. Your goal is to suggest incredible "
        "destinations based on the user's preferences, interests, and budget.\n\n"
        "Guidelines:\n"
        "1. Provide diverse options (e.g., hidden gems vs. popular spots).\n"
        "2. Explain *why* you are recommending each place.\n"
        "3. Include details about the best time to visit and key attractions.\n"
        "4. Be vivid, enthusiastic, and helpful."
    )
    
    if tools:
        agent = create_react_agent(llm, tools, prompt=system_prompt)
        result = await agent.ainvoke({"messages": messages})
        new_messages = result["messages"][len(messages):]
        return {"messages": new_messages}
    else:
        response = await llm.ainvoke([SystemMessage(content=system_prompt)] + messages)
        return {"messages": [response]}

async def travel_plan_node(state: dict):
    """
    Agent node for detailed travel planning. 
    In a full implementation, this node would be bound to MCP tools.
    """
    messages = state.get("messages", [])
    tools = state.get("tools", [])
    
    system_prompt = (
        "You are a professional travel planner. Your goal is to create detailed, "
        "personalized itineraries that include flights, hotels, and daily activities.\n\n"
        "Guidelines:\n"
        "1. Be specific about locations, times, and costs.\n"
        "2. Structure the itinerary day-by-day.\n"
        "3. Always maintain a professional and enthusiastic tone.\n"
        "4. If the user asks for a specific trip, provide a full breakdown."
    )
    
    if tools:
        agent = create_react_agent(llm, tools, prompt=system_prompt)
        result = await agent.ainvoke({"messages": messages})
        new_messages = result["messages"][len(messages):]
        return {"messages": new_messages}
    else:
        response = await llm.ainvoke([SystemMessage(content=system_prompt)] + messages)
        return {"messages": [response]}
