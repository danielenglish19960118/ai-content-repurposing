"""
Core AI Pipeline Engine for InsightEngine Enterprise
"""

from __future__ import annotations

import time
from google import genai
from google.genai import types
from src.schemas import TEMPLATES


def process_unstructured_data(
    raw_text: str,
    template_name: str,
    model_name: str,
    temperature: float,
    target_language: str,
    api_key: str
) -> tuple[str, float]:
    """Execute Gemini LLM processing pipeline with latency tracking."""
    if not raw_text or not raw_text.strip():
        raise ValueError("Raw input text cannot be empty.")
    if not api_key:
        raise ValueError("Gemini API Key is required.")

    start_time = time.time()
    
    client = genai.Client(api_key=api_key)
    template_prompt = TEMPLATES.get(template_name, TEMPLATES["Standard Executive Briefing"])
    
    system_instruction = f"""
{template_prompt}
STRICT CONSTRAINTS:
1. Do NOT invent facts, dates, owners, or metrics not explicitly present in the source text.
2. Translate and structure the final report strictly in **{target_language}**.
3. Output MUST be formatted in professional Markdown syntax only.
""".strip()

    prompt_content = f"--- RAW UNSTRUCTURED SOURCE TEXT ---\n{raw_text}\n--- END SOURCE TEXT ---"
    
    config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        temperature=temperature
    )
    
    response = client.models.generate_content(
        model=model_name,
        contents=prompt_content,
        config=config
    )
    
    latency = time.time() - start_time
    output_text = (response.text or "").strip()
    return output_text, latency
