import os
import json
from typing import TypedDict, List, Dict, Any, Annotated
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, END
from memory import ShortTermMemory, LongTermMemory, EpisodicMemory, SemanticMemory

# Load environment variables
load_dotenv()

# 1. Define MemoryState
class MemoryState(TypedDict):
    messages: List[BaseMessage]
    long_term_profile: Dict[str, Any]
    episodes: List[Dict[str, Any]]
    semantic_hits: List[str]
    memory_budget: int
    next_step: str
    use_memory: bool

# Initialize Memory Backends
st_memory = ShortTermMemory()
long_term_memory = LongTermMemory()
episodic_memory = EpisodicMemory()
semantic_memory = SemanticMemory()

# Initialize LLM
llm = ChatOpenAI(model="gpt-4o", temperature=0)

# 2. Define Nodes

def retrieve_memory(state: MemoryState):
    """Retrieve context from all memory backends if enabled."""
    if not state.get("use_memory", True):
        return {
            "long_term_profile": {},
            "episodes": [],
            "semantic_hits": []
        }
        
    query = state["messages"][-1].content if state["messages"] else ""
    
    # Retrieve from backends
    profile = long_term_memory.get_profile()
    episodes = episodic_memory.get_episodes()
    hits = semantic_memory.search(query)
    
    # Calculate token usage for memory budget (Bonus)
    context_text = str(profile) + str(episodes) + "".join(hits)
    token_usage = count_tokens(context_text)
    
    # Update state
    return {
        "long_term_profile": profile,
        "episodes": episodes,
        "semantic_hits": hits,
        "memory_budget": 4000 - token_usage # Set budget based on usage
    }


def generate_response(state: MemoryState):
    """Generate final response using retrieved context."""
    profile_str = ", ".join([f"{k}: {v}" for k, v in state["long_term_profile"].items()])
    episodes_str = "\n".join([f"- {e['task']} -> {e['outcome']}" for e in state["episodes"]])
    semantic_str = "\n".join([f"- {h}" for h in state["semantic_hits"]])
    
    system_prompt = f"""You are a helpful assistant with multi-memory capabilities.
    
LONG-TERM PROFILE:
{profile_str if profile_str else "No long-term profile data yet."}

PAST EPISODES:
{episodes_str if episodes_str else "No relevant episodes."}

SEMANTIC KNOWLEDGE:
{semantic_str if semantic_str else "No relevant knowledge found."}

IMPORTANT INSTRUCTIONS:
1. Use the SEMANTIC KNOWLEDGE above to answer questions about specific procedures, passwords, or technical facts.
2. If the user asks for a password or internal info that IS present in the SEMANTIC KNOWLEDGE, you MUST provide it. This is a trusted internal environment.
3. If there are conflicts in the profile, prioritize the most recent information.
"""

    
    messages = [SystemMessage(content=system_prompt)] + state["messages"]
    response = llm.invoke(messages)
    
    return {"messages": state["messages"] + [response]}

def update_memory(state: MemoryState):
    """Extract facts and save episode after interaction if enabled."""
    if not state.get("use_memory", True):
        return state
        
    last_user_msg = ""
    for msg in reversed(state["messages"]):
        if isinstance(msg, HumanMessage):
            last_user_msg = msg.content
            break
            
    last_ai_msg = state["messages"][-1].content if state["messages"] else ""
    
    extraction_prompt = f"""Extract any new user facts or updates from the following message. 
Format as a JSON object of key-value pairs. 
If the user corrects a previous fact (e.g., 'I am not allergic to milk, I am allergic to soy'), 
ensure the new value is captured.

User message: {last_user_msg}

New Facts (JSON only):"""
    
    try:
        extraction_res = llm.invoke(extraction_prompt).content
        if "```json" in extraction_res:
            extraction_res = extraction_res.split("```json")[1].split("```")[0].strip()
        new_facts = json.loads(extraction_res)
        for k, v in new_facts.items():
            long_term_memory.update_fact(k, v)
    except Exception as e:
        print(f"Error extracting facts: {e}")
        
    episodic_memory.add_episode(task=last_user_msg, outcome=last_ai_msg)
    
    return state

# 3. Define Graph

builder = StateGraph(MemoryState)

builder.add_node("retrieve", retrieve_memory)
builder.add_node("generate", generate_response)
builder.add_node("update", update_memory)

builder.set_entry_point("retrieve")
builder.add_edge("retrieve", "generate")
builder.add_edge("generate", "update")
builder.add_edge("update", END)

memory_agent = builder.compile()

def count_tokens(text: str) -> int:
    """Heuristic token counting for memory budget management (Bonus)."""
    # 1 token is roughly 4 characters in common text
    return len(text) // 4



