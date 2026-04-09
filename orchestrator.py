# orchestrator.py
# This is the "manager" that runs all agents in order.
# It maintains a shared state dictionary and passes outputs between agents.

import json
from agents import (
    pm_agent,
    data_analyst_agent,
    marketing_agent,
    risk_agent,
    synthesizer_agent
)

# ── The shared state ──────────────────────────────────────────────────────────
# Think of this as the whiteboard in the war room.
# Every agent reads from it and writes their output back to it.

def create_initial_state(data_dir="mock_data"):
    return {
        "data_dir":         data_dir,   # where to find the mock data
        "pm_output":        None,       # filled in by Agent 1
        "analyst_output":   None,       # filled in by Agent 2
        "marketing_output": None,       # filled in by Agent 3
        "risk_output":      None,       # filled in by Agent 4
        "final_decision":   None,       # filled in by Agent 5
    }


# ── Individual steps (nodes in the graph) ────────────────────────────────────
# Each function below is one "step" in the workflow.
# It receives the full state, does its work, updates state, returns it.

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

    # The synthesizer returns a JSON string — we parse it into a dictionary
    # Strip markdown code fences if the model accidentally adds them
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("```")[1]
        if cleaned.startswith("json"):
            cleaned = cleaned[4:]

    state["final_decision"] = json.loads(cleaned.strip())
    return state


# ── The main workflow ─────────────────────────────────────────────────────────
# This function runs all 5 steps in order and returns the final state.
# Think of it as the meeting agenda — each step happens in sequence.

def run_war_room(data_dir="mock_data"):
    print("\n" + "="*50)
    print("  WAR ROOM INITIATED")
    print("  PurpleMerit — Dashboard 2.0 Launch Review")
    print("="*50)

    # Step 0: create the shared whiteboard
    state = create_initial_state(data_dir)

    # Steps 1–5: run each agent in order
    # Each step reads from state and writes back to it
    state = step_pm(state)
    state = step_analyst(state)
    state = step_marketing(state)
    state = step_risk(state)
    state = step_synthesizer(state)

    print("\n" + "="*50)
    print("  WAR ROOM COMPLETE")
    print("="*50)

    return state