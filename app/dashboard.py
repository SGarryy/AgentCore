import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.nlp.extractor import extract_intent
from app.ml.router import route_task
from app.agents.dispatcher import dispatch
from app.llm import generate_response

# --- Page Config ---
st.set_page_config(
    page_title="AgentCore",
    page_icon="🧠",
    layout="wide"
)

# --- Header ---
st.markdown("""
    <h1 style='text-align: center; color: #4F8BF9;'>🧠 AgentCore</h1>
    <p style='text-align: center; color: gray;'>Intelligent Agent Orchestration Engine</p>
    <hr/>
""", unsafe_allow_html=True)

# --- Sidebar ---
st.sidebar.title("⚙️ AgentCore Info")
st.sidebar.markdown("""
**Available Agents:**
- 👤 HR Onboarding Agent
- 💰 Finance Reconciliation Agent
- 🖥️ IT Support & Triage Agent
- 📈 Sales & Lead Routing Agent
- 🏭 Operations & Procurement Agent

**Stack:**
- NLP: spaCy
- ML: scikit-learn
- LLM: Mistral (local)
- Backend: FastAPI
- UI: Streamlit
""")

st.sidebar.markdown("---")
st.sidebar.markdown("**Try these examples:**")
examples = [
    "Onboard new employee Sarah to HR on Monday",
    "Reconcile duplicate invoices from last month",
    "Triage bug on login page crashing on mobile",
    "Generate leads from retail sector urgently",
    "Schedule vendor meeting for procurement",
]
for ex in examples:
    if st.sidebar.button(ex, use_container_width=True):
        st.session_state["input_text"] = ex

# --- Main Input ---
st.markdown("### 💬 Enter your task")

if "input_text" not in st.session_state:
    st.session_state["input_text"] = ""

user_input = st.text_area(
    label="Task Input",
    value=st.session_state["input_text"],
    placeholder="e.g. Onboard new employee Sarah to HR team on Monday...",
    height=100,
    label_visibility="collapsed"
)

run_button = st.button("🚀 Run AgentCore", type="primary", use_container_width=True)

if run_button and user_input.strip():
    st.markdown("---")

    with st.spinner("🧠 Processing your request..."):

        # Step 1: NLP
        nlp_result = extract_intent(user_input)

        # Step 2: ML Router
        ml_result = route_task(user_input)

        # Step 3: Agent
        agent_result = dispatch(ml_result["routed_to"], nlp_result)

        # Step 4: LLM
        llm_response = generate_response(agent_result, user_input)

    # --- Results ---
    st.markdown("## 📊 Results")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🎯 Detected Intent", nlp_result["intent"].replace("_", " ").title())
    with col2:
        st.metric("🤖 Routed To", ml_result["routed_to"].replace("_", " ").title())
    with col3:
        st.metric("📊 Confidence", f"{int(ml_result['confidence'] * 100)}%")

    st.markdown("---")

    # NLP Details
    with st.expander("🔍 NLP Extraction Details"):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**👤 Persons**")
            st.write(nlp_result["entities"]["persons"] or "None detected")
        with col2:
            st.markdown("**📅 Dates**")
            st.write(nlp_result["entities"]["dates"] or "None detected")
        with col3:
            st.markdown("**🏢 Organizations**")
            st.write(nlp_result["entities"]["orgs"] or "None detected")
        st.markdown("**🔑 Matched Keywords**")
        st.write(", ".join(nlp_result["matched_keywords"]) or "None")

    # ML Scores
    with st.expander("📈 ML Routing Scores"):
        import pandas as pd
        scores = ml_result["all_scores"]
        df = pd.DataFrame({
            "Agent": [k.replace("_", " ").title() for k in scores.keys()],
            "Confidence": list(scores.values())
        }).sort_values("Confidence", ascending=False)
        st.bar_chart(df.set_index("Agent"))

    # Agent Steps
    st.markdown("### ⚡ Agent Execution Steps")
    for step in agent_result["steps"]:
        st.markdown(f"{step}")

    # LLM Response
    st.markdown("### 🧠 AI Summary")
    st.info(llm_response)

    # Timestamp
    st.caption(f"⏱️ Processed at: {agent_result['timestamp']}")

elif run_button and not user_input.strip():
    st.warning("Please enter a task first!")