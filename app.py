"""
Clean messy notes into a structured Markdown business report via Gemini.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
import streamlit as st

from google import genai

BASE_DIR = Path(__file__).resolve().parent
INPUT_PATH = BASE_DIR / "input.txt"
OUTPUT_PATH = BASE_DIR / "output.md"

MODEL_NAME = "gemini-3.6-flash"

SYSTEM_INSTRUCTIONS = """
You are an expert business analyst.
1. Clean up the raw source text: fix obvious typos, drop filler/hedging.
2. Do not invent facts, owners, dates, or metrics not in the source.
3. Return ONLY a Markdown report with these sections:
# Executive Summary
# Key Pain Points & Insights
# Action Items
""".strip()

def generate_report(raw_text: str) -> str:
    # 安全取得 API Key（優先讀取 Streamlit Secrets）
    api_key = None
    try:
        api_key = st.secrets.get("GEMINI_API_KEY")
    except Exception:
        pass
    
    if not api_key:
        api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        st.error("Error: GEMINI_API_KEY is not set in Streamlit secrets.")
        st.stop()

    client = genai.Client(api_key=api_key)
    interaction = client.interactions.create(
        model=MODEL_NAME,
        input=f"{SYSTEM_INSTRUCTIONS}\n\n--- RAW SOURCE TEXT ---\n{raw_text}\n--- END SOURCE TEXT ---",
    )
    return (interaction.output_text or "").strip()

st.title("AI Content Repurposing Tool")
user_text = st.text_area("Paste your raw notes or text here:")

if st.button("🚀 Generate Report"):
    if user_text:
        with st.spinner("Generating..."):
            result = generate_report(user_text)
            st.markdown(result)
            st.download_button("📥 Download Markdown", result, file_name="output.md")
    else:
        st.warning("Please enter some text first.")