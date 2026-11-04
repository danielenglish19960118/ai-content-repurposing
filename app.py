from __future__ import annotations

import os
import streamlit as st
from src.engine import run_enterprise_pipeline
from src.models import EnterpriseReportSchema
from config import config

st.set_page_config(
    page_title="InsightEngine Enterprise Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Enterprise CSS
st.markdown("""
<style>
    .main .block-container { padding-top: 2rem; padding-bottom: 3rem; }
    .stMetric { background-color: #f8f9fa; padding: 12px; border-radius: 8px; border: 1px solid #e9ecef; }
    .stButton>button { width: 100%; background-color: #0f52ba; color: white; font-weight: 600; border-radius: 6px; height: 3em; }
    .stButton>button:hover { background-color: #0b3c88; color: white; }
</style>
""", unsafe_allow_html=True)


def render_markdown_report(data: EnterpriseReportSchema) -> str:
    """Renders Pydantic schema into clean, formatted Markdown report."""
    md = f"# Executive Summary\n\n{data.executive_summary}\n\n"
    md += "# Key Pain Points & Insights\n\n"
    for insight in data.key_insights:
        md += f"* {insight}\n"
    md += "\n# Action Items\n\n"
    md += "| Action Item | Owner | Deadline | Priority |\n| :--- | :--- | :--- | :--- |\n"
    for item in data.action_items:
        md += f"| **{item.task}** | {item.owner} | {item.deadline} | `{item.priority}` |\n"
    return md


def get_api_key() -> str | None:
    try:
        if "GEMINI_API_KEY" in st.secrets and st.secrets["GEMINI_API_KEY"]:
            return st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass
    return os.environ.get("GEMINI_API_KEY")


def main():
    st.sidebar.image("https://img.icons8.com/color/96/lightning-bolt.png", width=50)
    st.sidebar.title("InsightEngine Enterprise")
    st.sidebar.caption("SaaS Tier v3.0 | Pydantic Schema Validated")

    st.sidebar.markdown("---")
    st.sidebar.subheader("⚙️ Tenant Configuration")
    target_lang = st.sidebar.selectbox("Target Output Language", config.SUPPORTED_LANGUAGES, index=0)

    st.sidebar.markdown("---")
    st.sidebar.subheader("🔒 Authentication & API Setup")
    api_key = get_api_key()
    if api_key:
        st.sidebar.success("API Key Active")
    else:
        st.sidebar.error("API Key Missing")
        user_key = st.sidebar.text_input("Enter Gemini API Key:", type="password")
        if user_key:
            api_key = user_key

    st.title("⚡ Enterprise Unstructured-to-Structured Intelligence Engine")
    st.caption("Powered by Gemini Structured Outputs & Pydantic Validation")

    tab_text, tab_file = st.tabs(["📝 Direct Input Pipeline", "📁 Batch File Upload"])

    raw_input_text = ""

    with tab_text:
        raw_input_text = st.text_area(
            "Paste Raw Unstructured Notes / Transcripts:",
            height=260,
            placeholder="- Meeting with Alex & Sarah today at 2pm about server costs...\n- Need to reduce AWS spend by 30%...\n- Login bug on mobile web needs urgent fix..."
        )

    with tab_file:
        uploaded_file = st.file_uploader("Upload document (.txt, .md)", type=["txt", "md"])
        if uploaded_file is not None:
            raw_input_text = uploaded_file.read().decode("utf-8")
            st.info(f"File **{uploaded_file.name}** loaded ({len(raw_input_text)} characters).")

    st.markdown("---")

    if st.button("🚀 Execute Enterprise Pipeline"):
        if not api_key:
            st.error("🔑 API Key required! Configure GEMINI_API_KEY in environment or sidebar.")
        elif not raw_input_text.strip():
            st.warning("⚠️ Please input text or upload a file.")
        else:
            with st.spinner("⚡ Running Pydantic Schema Extraction & Validation..."):
                try:
                    data, latency, est_tokens, est_cost = run_enterprise_pipeline(
                        raw_text=raw_input_text,
                        target_language=target_lang,
                        api_key=api_key
                    )
                    
                    st.session_state["report_data"] = data
                    st.session_state["latency"] = latency
                    st.session_state["tokens"] = est_tokens
                    st.session_state["cost"] = est_cost
                    st.session_state["chars"] = len(raw_input_text)
                except Exception as e:
                    st.error(f"Pipeline Error: {str(e)}")

    if "report_data" in st.session_state:
        st.subheader("📊 Validated Executive Report")
        
        # Operational Telemetry Metrics Bar
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Processing Latency", f"{st.session_state['latency']}s")
        m2.metric("Payload Size", f"{st.session_state['chars']} chars")
        m3.metric("Est. Token Payload", f"~{st.session_state['tokens']} tokens")
        m4.metric("Est. Execution Cost", f"${st.session_state['cost']:.5f} USD")

        md_output = render_markdown_report(st.session_state["report_data"])
        st.markdown(md_output)

        st.markdown("---")
        d1, d2 = st.columns(2)
        d1.download_button("📥 Download Markdown (.md)", md_output, file_name="executive_report.md", mime="text/markdown")
        d2.download_button("📥 Download JSON Schema (.json)", st.session_state["report_data"].model_dump_json(indent=2), file_name="schema_output.json", mime="application/json")


if __name__ == "__main__":
    main()
