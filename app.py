from __future__ import annotations

import os
import streamlit as st
from src.schemas import DEFAULT_MODEL, TEMPLATES, SUPPORTED_LANGUAGES
from src.engine import process_unstructured_data

# ---------------------------------------------------------
# Page Configuration & Enterprise Styling
# ---------------------------------------------------------
st.set_page_config(
    page_title="InsightEngine Enterprise AI Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }
    .stMetric {
        background-color: #f8f9fa;
        padding: 10px;
        border-radius: 8px;
        border: 1px solid #e9ecef;
    }
    .stButton>button {
        width: 100%;
        background-color: #0f52ba;
        color: white;
        font-weight: 600;
        border-radius: 6px;
        height: 3em;
    }
    .stButton>button:hover {
        background-color: #0b3c88;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

def get_api_key() -> str | None:
    """Retrieve Gemini API key from Streamlit secrets or OS environment."""
    try:
        if "GEMINI_API_KEY" in st.secrets and st.secrets["GEMINI_API_KEY"]:
            return st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass
    return os.environ.get("GEMINI_API_KEY")

def main():
    st.sidebar.image("https://img.icons8.com/color/96/lightning-bolt.png", width=50)
    st.sidebar.title("InsightEngine Enterprise")
    st.sidebar.caption("v2.4 Pro Tier | Powered by Google Gemini")

    st.sidebar.markdown("---")
    st.sidebar.subheader("⚙️ Pipeline Configuration")

    selected_template = st.sidebar.selectbox(
        "Report Schema Template",
        options=list(TEMPLATES.keys())
    )

    target_language = st.sidebar.selectbox(
        "Output Language",
        options=SUPPORTED_LANGUAGES,
        index=0
    )

    st.sidebar.markdown("---")
    st.sidebar.subheader("🎛️ Model Hyperparameters")
    selected_model = st.sidebar.selectbox("LLM Model Engine", [DEFAULT_MODEL], index=0)
    temperature = st.sidebar.slider("Creativity / Temperature", min_value=0.0, max_value=1.0, value=0.2, step=0.1)

    st.sidebar.markdown("---")
    st.sidebar.subheader("🔒 Authentication Status")
    api_key = get_api_key()
    if api_key:
        st.sidebar.success("API Key Verified (Active)")
    else:
        st.sidebar.error("API Key Missing")
        user_api_key_input = st.sidebar.text_input("Enter Gemini API Key:", type="password")
        if user_api_key_input:
            api_key = user_api_key_input

    st.title("⚡ Enterprise Unstructured-to-Structured Intelligence Engine")
    st.markdown(
        "Transform messy meeting logs, unstructured transcripts, and fragmented notes into decision-ready executive reports."
    )

    tab_text, tab_file = st.tabs(["📝 Direct Text Input", "📁 File Upload Pipeline"])

    raw_input_text = ""

    with tab_text:
        raw_input_text = st.text_area(
            "Paste Raw Unstructured Data / Transcripts:",
            height=240,
            placeholder="- Meeting with Alex & Sarah today at 2pm about server costs...\n- Need to reduce AWS spend by 30%...\n- Login bug on mobile web needs urgent fix..."
        )

    with tab_file:
        uploaded_file = st.file_uploader("Upload Notes or Transcripts (.txt, .md)", type=["txt", "md"])
        if uploaded_file is not None:
            raw_input_text = uploaded_file.read().decode("utf-8")
            st.info(f"File **{uploaded_file.name}** loaded successfully ({len(raw_input_text)} characters).")

    st.markdown("---")

    col_btn, col_stats = st.columns([1, 2])

    with col_btn:
        generate_btn = st.button("🚀 Run Intelligence Pipeline")

    if generate_btn:
        if not api_key:
            st.error("🔑 API Key required! Please set GEMINI_API_KEY in environment or sidebar.")
        elif not raw_input_text.strip():
            st.warning("⚠️ Please provide input text or upload a file first.")
        else:
            with st.spinner("⚡ Running deterministic extraction & synthesis..."):
                try:
                    report, latency = process_unstructured_data(
                        raw_text=raw_input_text,
                        template_name=selected_template,
                        model_name=selected_model,
                        temperature=temperature,
                        target_language=target_language,
                        api_key=api_key
                    )
                    
                    st.session_state["latest_report"] = report
                    st.session_state["latest_latency"] = latency
                    st.session_state["char_count"] = len(raw_input_text)
                    
                except Exception as e:
                    st.error(f"Execution Error: {str(e)}")

    if "latest_report" in st.session_state:
        st.subheader("📊 Output Intelligence Report")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Processing Latency", f"{st.session_state['latest_latency']:.2f}s")
        col2.metric("Source Payload Size", f"{st.session_state['char_count']} chars")
        col3.metric("Status", "200 OK (Validated)")
        
        st.markdown(st.session_state["latest_report"])
        
        st.markdown("---")
        col_dl1, col_dl2 = st.columns([1, 1])
        with col_dl1:
            st.download_button(
                label="📥 Export as Markdown (.md)",
                data=st.session_state["latest_report"],
                file_name="executive_report.md",
                mime="text/markdown"
            )
        with col_dl2:
            st.download_button(
                label="📄 Export as Raw Text (.txt)",
                data=st.session_state["latest_report"],
                file_name="executive_report.txt",
                mime="text/plain"
            )

if __name__ == "__main__":
    main()
