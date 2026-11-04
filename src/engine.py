"""
Core Engine using Google GenAI SDK with Pydantic Structured Output
"""
from __future__ import annotations
import time
from typing import Tuple
from google import genai
from google.genai import types

from src.models import EnterpriseReportSchema

DEFAULT_MODEL = "gemini-3.6-flash"

def run_enterprise_pipeline(
    raw_text: str,
    target_language: str,
    api_key: str
) -> Tuple[EnterpriseReportSchema, float, int]:
    """
    Executes the unstructured-to-structured pipeline with guaranteed schema fulfillment.
    """
    if not raw_text or not raw_text.strip():
        raise ValueError("Source input text cannot be empty.")
    if not api_key:
        raise ValueError("Gemini API Key is missing or invalid.")

    client = genai.Client(api_key=api_key)
    
    system_instruction = f"""
    You are an enterprise management consultant.
    Parse the raw input text and extract structured business intelligence.
    STRICT RULES:
    1. Translate all extracted fields strictly into: {target_language}.
    2. Do NOT hallucinate facts, metrics, dates, or owners not present in the source text.
    """.strip()

    config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        response_mime_type="application/json",
        response_schema=EnterpriseReportSchema,
        temperature=0.1
    )

    start_time = time.time()
    response = client.models.generate_content(
        model=DEFAULT_MODEL,
        contents=f"--- SOURCE TEXT ---\n{raw_text}\n--- END SOURCE TEXT ---",
        config=config
    )
    latency = round(time.time() - start_time, 2)
    
    # Parse into validated Pydantic object
    structured_data = EnterpriseReportSchema.model_validate_json(response.text)
    
    return structured_data, latency, len(raw_text)
