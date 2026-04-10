 
import json
from agents import (
    pm_agent,
    data_analyst_agent,
    marketing_agent,
    risk_agent,
    synthesizer_agent
) 

def create_initial_state(data_dir="mock_data"):
    return {
        "data_dir":         data_dir,   # where to find the mock data
        "pm_output":        None,       # filled in by Agent 1
        "analyst_output":   None,       # filled in by Agent 2
        "marketing_output": None,       # filled in by Agent 3
        "risk_output":      None,       # filled in by Agent 4
        "final_decision":   None,       # filled in by Agent 5
    }

 

def step_pm(state):
    print("\n" + "="*50)
    print("STEP 1: Product Manager Agent")
    print("="*50)
    state["pm_output"] = pm_agent(state["data_dir"])
    print("\n  PM output preview:")
    print("  " + state["pm_output"][:200] + "...")
    return state


def step_analyst(state):
    print("\n" + "="*50)
    print("STEP 2: Data Analyst Agent")
    print("="*50)
    state["analyst_output"] = data_analyst_agent(state["data_dir"])
    print("\n  Analyst output preview:")
    print("  " + state["analyst_output"][:200] + "...")
    return state


def step_marketing(state):
    print("\n" + "="*50)
    print("STEP 3: Marketing/Comms Agent")
    print("="*50)
    state["marketing_output"] = marketing_agent(state["data_dir"])
    print("\n  Marketing output preview:")
    print("  " + state["marketing_output"][:200] + "...")
    return state


def step_risk(state):
    print("\n" + "="*50)
    print("STEP 4: Risk/Critic Agent")
    print("="*50)
    # Notice: Risk agent receives ALL previous outputs
    state["risk_output"] = risk_agent(
        data_dir=        state["data_dir"],
        pm_output=       state["pm_output"],
        analyst_output=  state["analyst_output"],
        marketing_output=state["marketing_output"]
    )
    print("\n  Risk output preview:")
    print("  " + state["risk_output"][:200] + "...")
    return state


def step_synthesizer(state):
    print("\n" + "="*50)
    print("STEP 5: Synthesizer Agent — Final Decision")
    print("="*50)
    raw = synthesizer_agent(
        pm_output=       state["pm_output"],
        analyst_output=  state["analyst_output"],
        marketing_output=state["marketing_output"],
        risk_output=     state["risk_output"]
    )
 
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("```")[1]
        if cleaned.startswith("json"):
            cleaned = cleaned[4:]

    state["final_decision"] = json.loads(cleaned.strip())
    return state

 

def run_war_room(data_dir="mock_data"):
    print("\n" + "="*50)
    print("  WAR ROOM INITIATED")
    print("  PurpleMerit — Dashboard 2.0 Launch Review")
    print("="*50)
 
    state = create_initial_state(data_dir)
 
    state = step_pm(state)
    state = step_analyst(state)
    state = step_marketing(state)
    state = step_risk(state)
    state = step_synthesizer(state)

    print("\n" + "="*50)
    print("  WAR ROOM COMPLETE")
    print("="*50)

    return state
