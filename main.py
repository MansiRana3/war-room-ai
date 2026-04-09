# main.py
# This is the entry point — the file you run to start everything.
# Usage: py main.py

import json
import os
from datetime import datetime
from orchestrator import run_war_room

def main():
    # ── Step 1: make sure the output folder exists ────────────────────────────
    # This is where the final JSON report will be saved
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)   
    # exist_ok=True means "don't crash if the folder already exists"

    # ── Step 2: run the war room ──────────────────────────────────────────────
    # This triggers all 5 agents in sequence
    state = run_war_room(data_dir="mock_data")

    # ── Step 3: save the final decision to a JSON file ────────────────────────
    # We put a timestamp in the filename so each run creates a new file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename  = f"war_room_decision_{timestamp}.json"
    filepath  = os.path.join(output_dir, filename)

    with open(filepath, "w") as f:
        json.dump(state["final_decision"], f, indent=2)

    # ── Step 4: print a summary to the terminal ───────────────────────────────
    decision = state["final_decision"]

    print(f"\n{'='*50}")
    print(f"  FINAL DECISION: {decision['decision']}")
    print(f"  CONFIDENCE:     {decision['confidence_score']}/100")
    print(f"{'='*50}")
    print(f"\n  Report saved to: {filepath}")
    print(f"\n  RATIONALE:")
    print(f"  {decision['rationale']}")

    print(f"\n  ACTION PLAN:")
    for item in decision.get("action_plan_24_48h", []):
        print(f"  - [{item['owner']}] {item['action']} by {item['deadline']}")

    print(f"\n  RISKS:")
    for risk in decision.get("risk_register", []):
        print(f"  - [{risk['severity']}] {risk['risk']}")

# This line means "only run main() if this file is run directly"
# (not if it's imported by another file)
if __name__ == "__main__":
    main()