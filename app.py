 
# Run with: streamlit run app.py

import streamlit as st
import json
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
 
st.set_page_config(
    page_title="PurpleMerit War Room",
    page_icon="🚨",
    layout="wide"
)
 
st.markdown("""
<style>
    .main { background-color: #0f0f1a; }
    .decision-proceed {
        background: linear-gradient(135deg, #1a4a1a, #2d7a2d);
        border: 2px solid #4CAF50;
        border-radius: 16px;
        padding: 32px;
        text-align: center;
        margin: 16px 0;
    }
    .decision-pause {
        background: linear-gradient(135deg, #4a3a00, #7a6000);
        border: 2px solid #FFC107;
        border-radius: 16px;
        padding: 32px;
        text-align: center;
        margin: 16px 0;
    }
    .decision-rollback {
        background: linear-gradient(135deg, #4a0000, #7a1a1a);
        border: 2px solid #f44336;
        border-radius: 16px;
        padding: 32px;
        text-align: center;
        margin: 16px 0;
    }
    .agent-card {
        background: #1a1a2e;
        border: 1px solid #2d2d4e;
        border-radius: 12px;
        padding: 16px;
        margin: 8px 0;
    }
    .risk-high   { color: #f44336; font-weight: bold; }
    .risk-medium { color: #FFC107; font-weight: bold; }
    .risk-low    { color: #4CAF50; font-weight: bold; }
    .metric-card {
        background: #1a1a2e;
        border: 1px solid #2d2d4e;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True 
st.markdown("# 🚨 PurpleMerit War Room")
st.markdown("### Dashboard 2.0 Launch — Cross-Functional Decision System")
st.divider()
 
with st.sidebar:
    st.markdown("## ⚙️ Controls")
    st.markdown("**Data source:** `mock_data/`")
    st.markdown("**Model:** Groq LLaMA 3.3 70B")
    st.markdown("**Agents:** 5")
    st.divider()
 
    api_key = os.environ.get("GROQ_API_KEY")
    if api_key:
        st.success("✅ API key loaded")
    else:
        st.error("❌ GROQ_API_KEY not found in .env")

    st.divider()
    st.markdown("**How it works:**")
    st.markdown("1. PM Agent analyses goals")
    st.markdown("2. Data Analyst finds anomalies")
    st.markdown("3. Marketing assesses sentiment")
    st.markdown("4. Risk/Critic challenges assumptions")
    st.markdown("5. Synthesizer makes final decision")
 
st.markdown("### 📊 Live Metric Snapshot")

try:
    from tools import aggregate_metrics, detect_anomalies, analyse_sentiment
    metrics   = aggregate_metrics()
    anomalies = detect_anomalies()
    sentiment = analyse_sentiment()

    col1, col2, col3, col4, col5 = st.columns(5)
    pre  = metrics["pre_launch_avg"]
    post = metrics["post_launch_avg"]

    with col1:
        delta = round(post["crash_rate"] - pre["crash_rate"], 4)
        st.metric("Crash Rate", f"{post['crash_rate']:.3f}", f"+{delta:.3f}", delta_color="inverse")
    with col2:
        delta = round(post["api_latency_p95"] - pre["api_latency_p95"], 1)
        st.metric("API Latency p95", f"{post['api_latency_p95']}ms", f"+{delta}ms", delta_color="inverse")
    with col3:
        delta = round(post["payment_success_rate"] - pre["payment_success_rate"], 3)
        st.metric("Payment Success", f"{post['payment_success_rate']:.2%}", f"{delta:.3f}", delta_color="inverse")
    with col4:
        st.metric("Anomalies Found", anomalies["anomaly_count"], "all critical", delta_color="inverse")
    with col5:
        nps = sentiment["nps_proxy"]
        st.metric("NPS Proxy", f"{nps}", "very negative", delta_color="inverse")

except Exception as e:
    st.warning(f"Could not load metrics preview: {e}")

st.divider()

 st.markdown("### 🤖 Run the War Room")

if st.button("🚨 Convene War Room — Run All Agents", type="primary", use_container_width=True):
 
    from agents import pm_agent, data_analyst_agent, marketing_agent, risk_agent, synthesizer_agent

    state = {
        "data_dir":         "mock_data",
        "pm_output":        None,
        "analyst_output":   None,
        "marketing_output": None,
        "risk_output":      None,
        "final_decision":   None,
    }
 
    progress = st.progress(0, text="Starting war room...")

    # ── Agent 1: PM  
    with st.expander("🎯 Agent 1: Product Manager", expanded=True):
        with st.spinner("PM Agent analysing..."):
            state["pm_output"] = pm_agent(state["data_dir"])
        st.markdown(state["pm_output"])
    progress.progress(20, text="PM Agent complete...")

    # ── Agent 2: Data Analyst  
    with st.expander("📊 Agent 2: Data Analyst", expanded=True):
        with st.spinner("Data Analyst running anomaly detection..."):
            state["analyst_output"] = data_analyst_agent(state["data_dir"])
        st.markdown(state["analyst_output"])
    progress.progress(40, text="Data Analyst complete...")

    # ── Agent 3: Marketing  
    with st.expander("📣 Agent 3: Marketing / Comms", expanded=True):
        with st.spinner("Marketing Agent analysing sentiment..."):
            state["marketing_output"] = marketing_agent(state["data_dir"])
        st.markdown(state["marketing_output"])
    progress.progress(60, text="Marketing Agent complete...")

    # ── Agent 4: Risk 
    with st.expander("⚠️ Agent 4: Risk / Critic", expanded=True):
        with st.spinner("Risk Agent challenging assumptions..."):
            state["risk_output"] = risk_agent(
                data_dir=state["data_dir"],
                pm_output=state["pm_output"],
                analyst_output=state["analyst_output"],
                marketing_output=state["marketing_output"]
            )
        st.markdown(state["risk_output"])
    progress.progress(80, text="Risk Agent complete...")

    # ── Agent 5: Synthesizer 
    with st.spinner("🧠 Synthesizer making final decision..."):
        raw = synthesizer_agent(
            pm_output=state["pm_output"],
            analyst_output=state["analyst_output"],
            marketing_output=state["marketing_output"],
            risk_output=state["risk_output"]
        )
        cleaned = raw.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("```")[1]
            if cleaned.startswith("json"):
                cleaned = cleaned[4:]
        state["final_decision"] = json.loads(cleaned.strip())

    progress.progress(100, text="War room complete!")

    decision = state["final_decision"]
 
    os.makedirs("output", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath  = f"output/war_room_decision_{timestamp}.json"
    with open(filepath, "w") as f:
        json.dump(decision, f, indent=2)

    st.success(f"✅ Report saved to `{filepath}`")
    st.divider()
 
    d = decision.get("decision", "Unknown")
    if d == "Proceed":
        css_class = "decision-proceed"
        emoji = "✅"
    elif d == "Pause":
        css_class = "decision-pause"
        emoji = "⏸️"
    else:
        css_class = "decision-rollback"
        emoji = "🔴"

    st.markdown(f"""
    <div class="{css_class}">
        <h1 style="font-size: 3rem; margin: 0;">{emoji} {d}</h1>
        <p style="font-size: 1.2rem; margin-top: 8px; opacity: 0.9;">Final War Room Decision</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Confidence score ──────────────────────────────────────────────────────
    confidence = decision.get("confidence_score", 0)
    st.markdown(f"### 🎯 Confidence Score: {confidence}/100")
    st.progress(confidence / 100)

    # ── Confidence boosters ───────────────────────────────────────────────────
    boosters = decision.get("confidence_boosters", [])
    if boosters:
        st.markdown("**What would increase confidence:**")
        for b in boosters:
            st.markdown(f"- {b}")

    st.divider()

    # ── Rationale ─────────────────────────────────────────────────────────────
    st.markdown("### 📋 Rationale")
    st.info(decision.get("rationale", "No rationale provided."))

    st.divider()

    # ── Risk register + Action plan side by side ──────────────────────────────
    col_risk, col_action = st.columns(2)

    with col_risk:
        st.markdown("### ⚠️ Risk Register")
        for risk in decision.get("risk_register", []):
            severity = risk.get("severity", "Medium")
            color    = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}.get(severity, "🟡")
            with st.expander(f"{color} [{severity}] {risk.get('risk', '')}"):
                st.markdown(f"**Mitigation:** {risk.get('mitigation', 'N/A')}")

    with col_action:
        st.markdown("### ✅ Action Plan (24–48h)")
        for i, item in enumerate(decision.get("action_plan_24_48h", []), 1):
            with st.expander(f"Action {i}: {item.get('action', '')[:50]}..."):
                st.markdown(f"**Owner:** {item.get('owner', 'N/A')}")
                st.markdown(f"**Deadline:** {item.get('deadline', 'N/A')}")

    st.divider()

    # ── Communication plan ────────────────────────────────────────────────────
    st.markdown("### 📢 Communication Plan")
    comms = decision.get("communication_plan", {})
    col_int, col_ext = st.columns(2)

    with col_int:
        st.markdown("**🏢 Internal**")
        st.markdown(comms.get("internal", "No internal comms plan provided."))

    with col_ext:
        st.markdown("**🌍 External**")
        st.markdown(comms.get("external", "No external comms plan provided."))

    st.divider()

    # ── Raw JSON viewer ───────────────────────────────────────────────────────
    with st.expander("🔍 View Raw JSON Output"):
        st.json(decision)

# ── Footer ────────────────────────────────────────────────────────────────────
st.divider()
st.markdown(
    "<p style='text-align:center; opacity:0.5;'>PurpleMerit War Room · Built with Streamlit + Groq LLaMA 3.3</p>",
    unsafe_allow_html=True
)
