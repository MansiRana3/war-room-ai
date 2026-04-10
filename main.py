 
# Usage: py main.py

import json
import os
from datetime import datetime 
from orchestrator import run_war_room

def main(): 
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)    
    state = run_war_room(data_dir="mock_data")
 
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename  = f"war_room_decision_{timestamp}.json"
    filepath  = os.path.join(output_dir, filename)

    with open(filepath, "w") as f:
        json.dump(state["final_decision"], f, indent=2) 
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
