"""
"""
Clean messy notes into a structured Markdown business report via Gemini.

Reads input.txt from this script's directory.
Writes output.md to the same directory.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
import streamlit as st

from google import genai

# Script directory so input/output work regardless of the current working directory.
BASE_DIR = Path(__file__).resolve().parent
INPUT_PATH = BASE_DIR / "input.txt"
OUTPUT_PATH = BASE_DIR / "output.md"

# Official Interactions API models - updated to the correct active model.
MODEL_NAME = "gemini-3.6-flash"

SYSTEM_INSTRUCTIONS = """
You are an expert business analyst.

Your job:
1. Clean up the raw source text: fix obvious typos, drop filler/hedging,
   and keep only information that matters for decision-making.
2. Do not invent facts, owners, dates, or metrics that are not in the source.
   If an owner or next step is not stated, write "Unspecified".
3. Return ONLY a Markdown report with exactly these top-level sections
   (use these headings, in this order):

# Executive Summary
# Key Pain Points & Insights
# Action Items

Formatting:
- Executive Summary: 1–3 short paragraphs.
- Key Pain Points & Insights: bullet list; group related points.
- Action Items: a Markdown table with columns
  | Action | Owner | Next step | Notes |
- No preamble, no closing remarks, no code fences around the whole report.
""".strip()


def load_input_text(path: Path) -> str:
    """Read the source file as UTF-8."""
    if not path.is_file():
        print(f"Input file not found: {path}", file=sys.stderr)
        sys.exit(1)

    text = path.read_text(encoding="utf-8").strip()
    if not text:
        print(f"Input file is empty: {path}", file=sys.stderr)
        sys.exit(1)
    return text


def build_prompt(raw_text: str) -> str:
    """Combine analyst instructions with the raw source text."""
    return (
        f"{SYSTEM_INSTRUCTIONS}\n\n"
        "--- RAW SOURCE TEXT ---\n"
        f"{raw_text}\n"
        "--- END SOURCE TEXT ---"
    )


def strip_wrapping_fences(markdown: str) -> str:
    """Remove a wrapping ```markdown ... ``` fence if the model adds one."""
    text = markdown.strip()
    if not text.startswith("```"):
        return text

    lines = text.splitlines()
    if lines and lines[0].startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].strip() == "```":
        lines = lines[:-1]
    return "\n".join(lines).strip()


def generate_report(raw_text: str) -> str:
    """Call Gemini API safely using Streamlit Secrets or environment variables."""
    # 安全取得 API Key（優先讀取 Streamlit Secrets，其次讀取系統環境變數）
    api_key = None
    try:
        api_key = st.secrets.get("GEMINI_API_KEY")
    except Exception:
        pass
    
    if not api_key:
        api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        print("Error: GEMINI_API_KEY is not set in Streamlit secrets or environment variables.", file=sys.stderr)
        sys.exit(1)

    client = genai.Client(api_key=api_key)

    interaction = client.interactions.create(
        model=MODEL_NAME,
        input=build_prompt(raw_text),
    )

    markdown = (interaction.output_text or "").strip()
    if not markdown:
        print("The model returned an empty response.", file=sys.stderr)
        sys.exit(1)

    return strip_wrapping_fences(markdown)


def main() -> None:
    raw_text = load_input_text(INPUT_PATH)

    print(f"Reading  {INPUT_PATH.name} ...")
    print(f"Calling  {MODEL_NAME} via client.interactions.create ...")

    markdown = generate_report(raw_text)
    OUTPUT_PATH.write_text(markdown + "\n", encoding="utf-8")

    print(f"Wrote    {OUTPUT_PATH}")


if __name__ == "__main__":
    main()