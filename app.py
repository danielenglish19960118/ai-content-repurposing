from __future__ import annotations

import os
import streamlit as st
from src.engine import run_enterprise_pipeline

st.set_page_config(
    page_title="InsightEngine Enterprise SaaS",
    page_icon="⚡",
    layout="wide"
)

def render_markdown_report(data) -> str:
    md = f"# Executive Summary\n\n{data.executive_summary}\n\n"
    md += "# Key Pain Points & Insights\n\n"
    for insight in data.key_insights:
        md += f"* {insight}\n"
    md += "\n# Action Items\n\n"
    md += "| Action Item | Owner | Deadline | Priority |\n| :--- | :--- | :--- | :--- |\n"
    for item in data.action_items:
        md += f"| **{item.task}** | {item.owner} | {item.deadline} | `{item.priority}` |\n"
    return md

def main():
    st.title("⚡ InsightEngine Enterprise Platform")
    st.caption("Production-Grade Unstructured-to-Structured BI Pipeline")

    with st.sidebar:
        st.header("⚙️ Tenant Settings")
        target_lang = st.selectbox("Output Language", ["English", "Traditional Chinese (繁體中文)", "Japanese (日本語)"])
        st.divider()
        api_key = st.text_input("Gemini API Key", type="password") or os.environ.get("GEMINI_API_KEY")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("📥 Input Raw Data")
        raw_input = st.text_area("Paste unstructured text / meeting notes:", height=300)

    with col2:
        st.subheader("📊 Structured Executive Intelligence")
        if st.button("🚀 Process Pipeline"):
            if not raw_input.strip() or not api_key:
                st.error("Please provide both input text and a valid API key.")
                return

            with st.spinner("Executing Pydantic Structured Data Extraction..."):
                try:
                    structured_data, latency, char_count = run_enterprise_pipeline(
                        raw_text=raw_input,
                        target_language=target_lang,
                        api_key=api_key
                    )
                    
                    st.success(f"Pipeline executed in {latency}s ({char_count} chars input)")
                    md_output = render_markdown_report(structured_data)
                    st.markdown(md_output)
                    st.download_button("📥 Export Markdown", md_output, file_name="report.md")
                except Exception as e:
                    st.error(f"Pipeline Error: {str(e)}")

if __name__ == "__main__":
    main()
