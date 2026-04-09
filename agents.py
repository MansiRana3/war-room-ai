# agents.py
import os
import json
from dotenv import load_dotenv
from groq import Groq
from tools import aggregate_metrics, detect_anomalies, analyse_sentiment, compare_trend

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# ── Helper: ask Groq ──────────────────────────────────────────────────────────
def ask_llm(system_prompt, user_message):
    print(f"\n  [Groq call] {system_prompt[:60]}...")
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_message}
        ],
        temperature=0.3
    )
    return response.choices[0].message.content
# ── Agent 1: Product Manager ──────────────────────────────────────────────────
# Job: define success criteria and give a go/no-go recommendation
# Tools used: aggregate_metrics, compare_trend

def pm_agent(data_dir="mock_data"):
    print("\n[Agent 1] PM Agent running...")

    # Call the tools to get data
    metrics = aggregate_metrics(data_dir)
    trends  = compare_trend(data_dir)

    system_prompt = """You are the Product Manager in a war room during a product launch crisis.
Your job is to:
- State the success criteria for this launch
- Assess whether the launch is meeting those criteria
- Give a clear go/no-go framing
- Identify which user segments are most impacted
Keep your response focused and under 300 words."""

    user_message = f"""We launched Dashboard 2.0 on 2026-03-08. Here is the current data:

POST-LAUNCH AVERAGES (last 3 days):
{json.dumps(metrics['post_launch_avg'], indent=2)}

PRE-LAUNCH AVERAGES (7 days before):
{json.dumps(metrics['pre_launch_avg'], indent=2)}

METRIC CHANGES:
{json.dumps(trends, indent=2)}

Based on this data, provide your PM assessment."""

    return ask_llm(system_prompt, user_message)


# ── Agent 2: Data Analyst ─────────────────────────────────────────────────────
# Job: deep dive into the numbers, spot anomalies, assess confidence
# Tools used: detect_anomalies, compare_trend

def data_analyst_agent(data_dir="mock_data"):
    print("\n[Agent 2] Data Analyst Agent running...")

    anomalies = detect_anomalies(data_dir)
    trends    = compare_trend(data_dir)

    system_prompt = """You are the Data Analyst in a war room during a product launch crisis.
Your job is to:
- Analyse the anomalies and metric trends
- Identify which metrics are most critical
- Assess the confidence level in this data
- Flag any patterns or correlations you notice
Be precise and reference specific numbers. Keep your response under 300 words."""

    user_message = f"""Anomaly detection results:
{json.dumps(anomalies, indent=2)}

Trend comparison (% change post-launch vs pre-launch):
{json.dumps(trends, indent=2)}

Provide your data analysis."""

    return ask_llm(system_prompt, user_message)


# ── Agent 3: Marketing / Comms ────────────────────────────────────────────────
# Job: assess customer perception and recommend communication actions
# Tools used: analyse_sentiment

def marketing_agent(data_dir="mock_data"):
    print("\n[Agent 3] Marketing/Comms Agent running...")

    sentiment = analyse_sentiment(data_dir)

    system_prompt = """You are the Marketing and Communications lead in a war room during a product launch crisis.
Your job is to:
- Assess current customer sentiment and perception
- Identify the biggest reputation risks
- Recommend immediate communication actions (internal and external)
- Suggest messaging for different audiences
Keep your response under 300 words."""

    user_message = f"""User feedback analysis from the last 3 days post-launch:
{json.dumps(sentiment, indent=2)}

Key themes in negative feedback:
- Crashes and freezing
- Slow performance and API timeouts  
- Payment failures
- Users cancelling and switching to competitors
- Support not responding fast enough

Provide your marketing and comms assessment."""

    return ask_llm(system_prompt, user_message)


# ── Agent 4: Risk / Critic ────────────────────────────────────────────────────
# Job: challenge assumptions, highlight risks, request more evidence
# Tools used: reads all previous agent outputs + release notes

def risk_agent(data_dir="mock_data", pm_output="", analyst_output="", marketing_output=""):
    print("\n[Agent 4] Risk/Critic Agent running...")

    # Read the release notes file directly
    notes_path = os.path.join(data_dir, "release_notes.md")
    with open(notes_path) as f:
        release_notes = f.read()

    system_prompt = """You are the Risk and Critic agent in a war room during a product launch crisis.
Your job is to:
- Challenge any weak assumptions made by other agents
- Highlight risks that haven't been mentioned yet
- Reference the known issues from the release notes
- Identify what evidence is still missing
- Build a risk register with severity ratings (High/Medium/Low)
Be skeptical and thorough. Keep your response under 350 words."""

    user_message = f"""RELEASE NOTES AND KNOWN ISSUES:
{release_notes}

PM AGENT SAID:
{pm_output}

DATA ANALYST SAID:
{analyst_output}

MARKETING AGENT SAID:
{marketing_output}

Challenge these assessments, highlight overlooked risks, and produce a risk register."""

    return ask_llm(system_prompt, user_message)


# ── Agent 5: Synthesizer ──────────────────────────────────────────────────────
# Job: read all agent outputs and produce the final structured JSON decision
# This is the orchestrator's final step

def synthesizer_agent(pm_output, analyst_output, marketing_output, risk_output):
    print("\n[Agent 5] Synthesizer Agent running...")

    system_prompt = """You are the Synthesizer in a war room. You have read all agent reports.
Your job is to produce the FINAL structured decision as valid JSON.

You must output ONLY a JSON object — no explanation, no markdown, no code block.
The JSON must contain exactly these keys:
- decision: one of "Proceed", "Pause", or "Roll Back"
- rationale: a string explaining the key drivers
- confidence_score: a number from 0 to 100
- confidence_boosters: a list of strings (what would increase confidence)
- risk_register: a list of objects with keys: risk, severity, mitigation
- action_plan_24_48h: a list of objects with keys: action, owner, deadline
- communication_plan: an object with keys: internal, external"""

    user_message = f"""PM AGENT:
{pm_output}

DATA ANALYST:
{analyst_output}

MARKETING/COMMS:
{marketing_output}

RISK/CRITIC:
{risk_output}

Synthesize all of the above into the final JSON decision."""

    return ask_llm(system_prompt, user_message)