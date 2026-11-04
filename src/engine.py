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
from src.database import log_usage
from config import config

rate_limiter = TokenRateLimiter()

def run_enterprise_pipeline(
    raw_text: str,
    target_language: str,
    api_key: str,
    tenant_id: str = "default_tenant"
) -> Tuple[EnterpriseReportSchema, float, int, float]:
    if not raw_text or not raw_text.strip():
        raise ValueError("Source input text cannot be empty.")
    if not api_key:
        raise ValueError("Gemini API Key is missing or invalid.")

    allowed, est_tokens, est_cost = rate_limiter.check_and_track(raw_text)
    if not allowed:
        raise RuntimeError("Rate limit exceeded for current minute session. Please wait 60 seconds.")

    client = genai.Client(api_key=api_key)
    
    system_instruction = f"""
You are an elite enterprise management consultant and system architect.
Parse the raw input text and extract structured business intelligence.

STRICT CONSTRAINTS:
1. Translate all extracted fields strictly into: {target_language}.
2. Do NOT invent or hallucinate facts, metrics, dates, or owners not present in the source text.
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
    
    structured_data = EnterpriseReportSchema.model_validate_json(response.text)
    
    # 紀錄用量數據至 DB
    log_usage(tenant_id, len(raw_text), est_tokens, est_cost, latency)
    
    return structured_data, latency, est_tokens, est_cost
