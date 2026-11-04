"""
Enterprise REST API Engine for InsightEngine Integration
"""
from fastapi import FastAPI, HTTPException, Header
from src.models import APITransformRequest, EnterpriseReportSchema
from src.engine import run_enterprise_pipeline
import os

app = FastAPI(
    title="InsightEngine Enterprise API",
    version="3.5.0",
    description="RESTful Gateway for Unstructured-to-Structured Intelligence Pipeline"
)

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "InsightEngine Core API"}

@app.post("/v1/transform", response_model=EnterpriseReportSchema)
def transform_unstructured_text(
    payload: APITransformRequest,
    x_api_key: str = Header(None, alias="X-API-Key")
):
    api_key = x_api_key or os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=401, detail="API Key required via X-API-Key header or environment.")

    try:
        report, latency, tokens, cost = run_enterprise_pipeline(
            raw_text=payload.raw_text,
            target_language=payload.target_language,
            api_key=api_key
        )
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
