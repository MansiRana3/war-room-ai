# War Room AI — Multi-Agent Launch Decision System

A multi-agent AI system that simulates a cross-functional war room during a product launch crisis. Five specialized agents analyze metrics, user feedback, and release notes to produce a structured launch decision: **Proceed / Pause / Roll Back**.

## System Architecture
mock_data/ → tools.py → agents.py → orchestrator.py → final JSON decision
Five agents run in sequence:
1. **PM Agent** — defines success criteria and go/no-go framing
2. **Data Analyst Agent** — detects anomalies and analyses trends
3. **Marketing/Comms Agent** — assesses sentiment and reputation risk
4. **Risk/Critic Agent** — challenges assumptions and builds risk register
5. **Synthesizer Agent** — produces the final structured JSON decision

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/MansiRana3/war-room-ai.git
cd war-room-ai
```

### 2. Install dependencies
```bash
pip install groq python-dotenv streamlit
```

### 3. Set up environment variables
Create a `.env` file in the root directory:
GROQ_API_KEY=your-groq-api-key-here
Get a free API key at: https://console.groq.com

## How to Run

### Option A: CLI
```bash
py main.py
```
Output is saved to `output/war_room_decision_[timestamp].json`

### Option B: Streamlit UI
```bash
py -m streamlit run app.py
```
Opens in browser at `http://localhost:8501`

## Example Output

```json
{
  "decision": "Roll Back",
  "confidence_score": 80,
  "rationale": "8/8 metrics in breach post-launch...",
  "risk_register": [...],
  "action_plan_24_48h": [...],
  "communication_plan": {...}
}
```

## Environment Variables

| Variable | Description | Required |
|---|---|---|
| `GROQ_API_KEY` | Groq API key for LLaMA 3.3 70B | Yes |

## Traceability

Console logs show every agent step and tool call when running `py main py`:
[Agent 1] PM Agent running...
[Groq call] You are the Product Manager...
[Agent 2] Data Analyst Agent running...
[Groq call] You are the Data Analyst...
## Tools Used

| Tool | Purpose | Called By |
|---|---|---|
| `aggregate_metrics` | Summarises CSV metrics pre/post launch | PM Agent |
| `detect_anomalies` | Finds metrics that changed dramatically | Data Analyst |
| `analyse_sentiment` | Counts themes in negative feedback | Marketing Agent |
| `compare_trend` | % change pre vs post launch | PM + Analyst |

## Tech Stack
- **Python** — core language
- **Groq + LLaMA 3.3 70B** — LLM for all agents
- **Streamlit** — web UI
- **python-dotenv** — environment variable management