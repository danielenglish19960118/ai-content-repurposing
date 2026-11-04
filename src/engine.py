"""
Core Engine using Google GenAI SDK with Pydantic Structured Output
"""
from __future__ import annotations

import time
from typing import Tuple
from google import genai
from google.genai import types

from src.models import EnterpriseReportSchema
from src.rate_limiter import TokenRateLimiter
from config import config

rate_limiter = TokenRateLimiter()


def run_enterprise_pipeline(
    raw_text: str,
    target_language: str,
    api_key: str
) -> Tuple[EnterpriseReportSchema, float, int, float]:
    """
    Executes the unstructured-to-structured pipeline with guaranteed schema fulfillment.
    
    Returns:
        Tuple[EnterpriseReportSchema, latency_seconds, token_count, estimated_cost_usd]
    """
    if not raw_text or not raw_text.strip():
        raise ValueError("Source input text cannot be empty.")
    if not api_key:
        raise ValueError("Gemini API Key is missing or invalid.")

    # Rate Limiting & Token Telemetry Check
    allowed, est_tokens, est_cost = rate_limiter.check_and_track(raw_text)
    if not allowed:
        raise RuntimeError("Rate limit exceeded for current minute session. Please wait 60 seconds.")

    client = genai.Client(api_key=api_key)
    
    system_instruction = f"""
You are an elite enterprise management consultant and system architect.
Parse the raw input text and extract structured business intelligence.

STRICT CONSTRAINTS:
1. Translate all extracted fields strictly into: {target_language}.
2. Do NOT invent or hallucinate facts, metrics, dates, or owners not explicitly present in or derived from the source text.
3. Output MUST fulfill the EnterpriseReportSchema schema exactly.
""".strip()

    gen_config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        response_mime_type="application/json",
        response_schema=EnterpriseReportSchema,
        temperature=config.DEFAULT_TEMPERATURE
    )

    start_time = time.time()
    response = client.models.generate_content(
        model=config.DEFAULT_MODEL,
        contents=f"--- SOURCE TEXT ---\n{raw_text}\n--- END SOURCE TEXT ---",
        config=gen_config
    )
    latency = round(time.time() - start_time, 2)
    
    # Parse into validated Pydantic object
    structured_data = EnterpriseReportSchema.model_validate_json(response.text)
    
    return structured_data, latency, est_tokens, est_cost
